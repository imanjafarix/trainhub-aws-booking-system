# TrainHub – Serverless Booking System on AWS

TrainHub is a cloud-native booking system built using AWS serverless services.  
The project demonstrates a secure and scalable backend architecture using managed AWS services.

---

# Architecture

![Architecture](architecture/architecture-diagram.png)

System flow:

User → CloudFront → S3 → API Gateway → Lambda → RDS

---

# AWS Services Used

- AWS Lambda
- Amazon API Gateway
- Amazon RDS (MySQL)
- Amazon S3
- Amazon CloudFront
- AWS Secrets Manager
- Amazon VPC
- Amazon CloudWatch
- Amazon SNS
- AWS Budgets
- AWS CloudFormation

---

# Security

Key security features:

- Private VPC architecture
- RDS in private subnets
- IAM least privilege roles
- Secrets stored in AWS Secrets Manager
- No public database access
- TLS encryption

---

# Infrastructure as Code

The infrastructure is deployed using AWS CloudFormation.

Example:

aws cloudformation deploy \
--template-file template.yaml \
--stack-name trainhub-stack

---

# Documentation

Detailed documentation can be found in the **docs/** folder:

Architecture design  
Security report  
Technical implementation

---

# Future Improvements

- Add authentication with Amazon Cognito
- Protect API using AWS WAF
- Implement CI/CD pipeline
- Add automated tests

---

# Author

Iman Jafari
