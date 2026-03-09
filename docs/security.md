# Security Architecture

Security is a central part of the TrainHub architecture and follows the AWS Shared Responsibility Model.

AWS is responsible for securing the cloud infrastructure while the system configuration and data protection are handled within the project. :contentReference[oaicite:3]{index=3}

The system is designed according to AWS Well-Architected security principles.

---

# Network Security

The infrastructure is deployed inside a dedicated VPC which separates public and private resources.

Private subnets host:

- AWS Lambda
- Amazon RDS

The database does not have a public IP and cannot be accessed directly from the internet.

Security groups act as virtual firewalls and allow only specific traffic.

Example rules:

RDS inbound rules
- MySQL port 3306 allowed only from Lambda security group

Lambda outbound rules
- Port 3306 to RDS
- HTTPS (443) to AWS services

This ensures that only authorized services can communicate with the database. :contentReference[oaicite:4]{index=4}

---

# Identity and Access Management

Access permissions are controlled through AWS IAM roles.

The Lambda function uses a dedicated IAM role with minimal permissions required to operate.

Permissions include:

- SecretsManager:GetSecretValue
- CloudWatch logging permissions
- VPC network interface access

This follows the principle of least privilege, which limits the impact of potential security incidents. :contentReference[oaicite:5]{index=5}

---

# Secret Management

Database credentials are stored in AWS Secrets Manager.

The Lambda function retrieves the credentials dynamically during execution.

This prevents sensitive information from being stored in:

- source code
- configuration files
- version control systems

Secrets are encrypted using AWS-managed encryption keys.

---

# Data Protection

Multiple layers of protection are used for data security.

Encryption in transit
- HTTPS for all API communication
- TLS connections to the database

Encryption at rest
- RDS storage encryption
- encrypted backups
- encrypted secrets

These controls ensure confidentiality and integrity of the application data.

---

# Monitoring and Alerts

System monitoring is implemented using Amazon CloudWatch.

The system tracks:

- Lambda errors
- API activity
- database availability

CloudWatch alarms trigger notifications through Amazon SNS to alert administrators of potential issues. :contentReference[oaicite:6]{index=6}
