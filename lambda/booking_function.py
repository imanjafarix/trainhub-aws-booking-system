 import json
          import os
          import boto3
          import pymysql
          from botocore.exceptions import ClientError
          
          def get_db_connection():
              """Hämta DB credentials och skapa connection"""
              secrets_client = boto3.client('secretsmanager', region_name=os.environ['REGION'])
              
              try:
                  response = secrets_client.get_secret_value(
                      SecretId=os.environ['DB_SECRET_ARN']
                  )
                  secret = json.loads(response['SecretString'])
                  
                  connection = pymysql.connect(
                      host=os.environ['DB_ENDPOINT'],
                      user=secret['username'],
                      password=secret['password'],
                      database=os.environ['DB_NAME'],
                      connect_timeout=5,
                      cursorclass=pymysql.cursors.DictCursor
                  )
                  return connection
                  
              except (ClientError, pymysql.Error) as e:
                  raise Exception(f"Database connection error: {e}")
          
          def lambda_handler(event, context):
              http_method = event.get('httpMethod', 'GET')
              
              # GET /bookings/{member_id} - Hämta alla bokningar för en medlem
              if http_method == 'GET' and 'member_id' in event.get('pathParameters', {}):
                  member_id = event['pathParameters']['member_id']
                  
                  try:
                      connection = get_db_connection()
                      
                      with connection.cursor() as cursor:
                          cursor.callproc('GetMemberBookings', (int(member_id),))
                          results = cursor.fetchall()
                      
                      connection.close()
                      
                      return {
                          'statusCode': 200,
                          'headers': {
                              'Content-Type': 'application/json',
                              'Access-Control-Allow-Origin': '*'
                          },
                          'body': json.dumps({
                              'member_id': member_id,
                              'bookings': results
                          })
                      }
                      
                  except Exception as e:
                      return {
                          'statusCode': 500,
                          'headers': {'Content-Type': 'application/json'},
                          'body': json.dumps({'error': str(e)})
                      }
              
              # POST /bookings - Skapa ny bokning (använder stored procedure)
              elif http_method == 'POST':
                  try:
                      body = json.loads(event.get('body', '{}'))
                      member_id = body.get('member_id')
                      pass_id = body.get('pass_id')
                      
                      if not member_id or not pass_id:
                          return {
                              'statusCode': 400,
                              'headers': {'Content-Type': 'application/json'},
                              'body': json.dumps({'error': 'Missing member_id or pass_id'})
                          }
                      
                      connection = get_db_connection()
                      
                      with connection.cursor() as cursor:
                          # Anropa stored procedure med output-parametrar
                          cursor.callproc('CreateBooking', (
                              int(member_id), 
                              int(pass_id),
                          ))
                          
                          # Hämta resultatet från stored proceduren
                          results = cursor.fetchall()
                          if results:
                              result = results[0]
                              
                              if result.get('p_status') == 'SUCCESS':
                                  return {
                                      'statusCode': 201,
                                      'headers': {
                                          'Content-Type': 'application/json',
                                          'Access-Control-Allow-Origin': '*'
                                      },
                                      'body': json.dumps({
                                          'message': 'Booking created successfully',
                                          'booking_id': result.get('p_booking_id'),
                                          'member_id': member_id,
                                          'pass_id': pass_id,
                                          'booking_date': str(result.get('p_booking_date')),
                                          'status': 'active'
                                      })
                                  }
                              else:
                                  return {
                                      'statusCode': 400,
                                      'headers': {'Content-Type': 'application/json'},
                                      'body': json.dumps({
                                          'error': result.get('p_error_message', 'Booking failed')
                                      })
                                  }
                          else:
                              # Fallback om stored procedure inte returnerar förväntat resultat
                              cursor.execute("""
                                  INSERT INTO bookings (member_id, pass_id) 
                                  VALUES (%s, %s)
                              """, (member_id, pass_id))
                              
                              booking_id = cursor.lastrowid
                              connection.commit()
                              
                              cursor.execute("""
                                  SELECT * FROM bookings WHERE booking_id = %s
                              """, (booking_id,))
                              booking = cursor.fetchone()
                              
                              return {
                                  'statusCode': 201,
                                  'headers': {
                                      'Content-Type': 'application/json',
                                      'Access-Control-Allow-Origin': '*'
                                  },
                                  'body': json.dumps({
                                      'message': 'Booking created (using direct insert)',
                                      'booking_id': booking_id,
                                      'member_id': member_id,
                                      'pass_id': pass_id,
                                      'booking_date': str(booking['booking_date']) if booking else None
                                  })
                              }
                      
                  except json.JSONDecodeError:
                      return {
                          'statusCode': 400,
                          'headers': {'Content-Type': 'application/json'},
                          'body': json.dumps({'error': 'Invalid JSON format'})
                      }
                  except Exception as e:
                      return {
                          'statusCode': 500,
                          'headers': {'Content-Type': 'application/json'},
                          'body': json.dumps({'error': str(e)})
                      }
                  finally:
                      if 'connection' in locals():
                          connection.close()
              
              # OPTIONS (CORS preflight)
              elif http_method == 'OPTIONS':
                  return {
                      'statusCode': 200,
                      'headers': {
                          'Access-Control-Allow-Origin': '*',
                          'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                          'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
                      },
                      'body': ''
                  }
              
              else:
                  return {
                      'statusCode': 404,
                      'headers': {'Content-Type': 'application/json'},
                      'body': json.dumps({'error': 'Endpoint not found'})
                  }
