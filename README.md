# 🛠 DevOps Infrastructure Provisioning & AWS Projects (Rolling Collection)

## 📌 Overview

This repository documents **four major infrastructure projects**, built
progressively during the DevOps learning path:

1.  **Infrastructure Provisioning & Configuration Automation** (Python +
    Bash simulator)\
2.  **AWS Resource Dashboard (Rolling project AWS)** --- Flask + boto3\
3.  **Terraform EC2 Builder** --- Infrastructure-as-Code deployment\
4.  **CI/CD Integration with Jenkins** --- Docker build pipeline with
    linting & security scans

All projects are **independent**, but share the same goal: demonstrating
**automation, IaC, CI/CD, and cloud provisioning** best practices.

------------------------------------------------------------------------

# 📦 Project A --- Infrastructure Provisioning & Configuration Automation

A **Python + Bash simulator** that walks through VM provisioning, input
validation, JSON persistence, and logging.

## ✨ Features

-   Modular Python OOP design (`machine.py`, `infra_simulator.py`)\
-   Bash-based service automation (e.g., Nginx installation)\
-   Logging and error handling (`logs/provisioning.log`)\
-   Configuration persistence using `configs/instances.json`

## 📁 Structure

``` text
infra-automation/
├─ scripts/
│  ├─ infra_simulator.py
│  └─ setup_nginx.sh
│
├─ configs/
│  └─ instances.json
│
├─ logs/
│  └─ provisioning.log
│
├─ src/
│  └─ machine.py
│
├─ requirements.txt
└─ README.md
```

------------------------------------------------------------------------

# ☁️ Project B --- AWS Resource Dashboard (Flask + boto3)

A **Flask web app** that runs locally and connects to your AWS account
to display live data for:

-   EC2 instances\
-   VPCs\
-   AMIs\
-   Load Balancers

Proof-of-concept screenshots are stored under `AWS/Screenshots/`.

## 📁 Structure

``` text
infra-automation/
├─ projects/
│   └─ Rolling project AWS/
│       ├─ Python/
│       │   ├─ app.py
│       │   ├─ requirements.txt
│       │   └─ venv/ (ignored)
│       │
│       └─ AWS/
│           └─ Screenshots/
│               ├─ localhost-5001-1.png
│               ├─ localhost-5001-2.png
│               └─ live-ec2-console.png
```

## 🚀 Run the AWS Dashboard

``` bash
cd projects/"Rolling project AWS"/Python
python -m venv venv

# Windows
venv\Scripts\Activate.ps1

# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt

# Provide AWS credentials
export AWS_ACCESS_KEY_ID="YOUR_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
export AWS_DEFAULT_REGION="us-east-2"

python app.py
```

Then visit:\
👉 http://localhost:5001/\
Health check: http://localhost:5001/healthz

------------------------------------------------------------------------

# 🌍 Project C --- Terraform EC2 Builder

## ☁️ Terraform EC2 Builder (Portfolio Version)

This Terraform configuration demonstrates **Infrastructure-as-Code
(IaC)** by provisioning a Docker-ready EC2 instance in AWS.

> 🔒 Sensitive IDs and IP addresses have been masked for security.

## 🧱 Resources Reference

-   **VPC ID:** `vpc-xxxxxxxxxxxxxxxxx`\
-   **Subnet ID:** `subnet-xxxxxxxxxxxxxxxxx`\
-   **Region:** `us-east-1`

## ⚙️ Overview

This configuration:

-   Generates a secure SSH key pair (local + AWS)\
-   Creates a security group allowing:
    -   SSH (22)
    -   App access (5001)\
-   Launches an **Ubuntu EC2 instance**\
-   Installs **Docker** automatically via `user_data`\
-   Outputs the instance's public IP for verification

## 🧩 Project Structure

``` text
Rolling project Terraform/
├── main.tf
├── variables.tf
├── providers.tf
├── versions.tf
├── outputs.tf
├── .gitignore
└── README.md
```

## 🚀 How to Run

``` bash
terraform init
terraform plan
terraform apply -auto-approve
```

Once created:

``` bash
terraform output -raw instance_public_ip
```

Connect via SSH:

``` bash
chmod 600 <your_key>.pem
ssh -i <your_key>.pem ubuntu@<public_ip>
```

## 🧾 Key Highlights

-   Written in **Terraform (HCL)** with version pinning\
-   Uses **data lookups** for Ubuntu AMIs\
-   Validates subnet/VPC match via a precondition\
-   Demonstrates modular IaC design and secure key management\
-   Installs Docker automatically with no manual setup required

## 📦 Tools Used

-   Terraform 1.5+\
-   AWS CLI 2.x\
-   Ubuntu 22.04 AMI\
-   Docker CE

------------------------------------------------------------------------

# 🚀 Project D --- CI/CD Integration with Jenkins (Docker Pipeline)

This project implements a full **CI/CD pipeline using Jenkins**,
integrating:

-   GitHub source control\
-   Parallel linting & security scans\
-   Docker image build\
-   Automated push to Docker Hub

This stage represents the transition from infrastructure provisioning
into **continuous integration and container delivery**.

## 🎯 Pipeline Capabilities

The Jenkins pipeline performs:

1.  Clone repository from GitHub (Dev branch)\
2.  Run parallel checks:
    -   Python linting (Flake8)
    -   Shell script linting (ShellCheck)
    -   Dockerfile linting (Hadolint)
3.  Run security scans:
    -   Bandit (Python security)
    -   Trivy (filesystem + container scan)
4.  Build Docker image
5.  Tag image using Jenkins build number
6.  Push image to Docker Hub

## 🐳 Docker Hub Repository

    nixonp95/flask-aws-monitor

Tags created automatically: - `latest` - `<jenkins-build-number>`

## 📁 Project Structure

``` text
projects/
└── Rolling project Integration with Jenkins/
    └── Rolling-project-app/
        ├── Jenkinsfile
        ├── Dockerfile
        ├── app.py
        ├── requirements.txt
        ├── README.md
        └── .gitignore
```

## ⚙️ Jenkins Setup Summary

Jenkins runs inside Docker (Builder EC2) and performs:

-   CI validation
-   Container build
-   Security verification
-   Docker Hub deployment

Credentials used: - DockerHub Access Token stored in Jenkins as:

    dockerhub-creds

------------------------------------------------------------------------

# 🧠 Skills Demonstrated Across Projects

-   Python automation
-   Bash scripting
-   Flask development
-   AWS SDK (boto3)
-   Infrastructure as Code (Terraform)
-   CI/CD pipeline design
-   Jenkins automation
-   Docker containerization
-   Security scanning (Trivy, Bandit)
-   Linting & code quality enforcement

------------------------------------------------------------------------

# 👤 Author

**Nikita Pozniak**\
DevOps Student -- Class 35690

Projects included: - Infrastructure Automation Simulator\
- AWS Monitoring Dashboard\
- Terraform EC2 Builder\
- Jenkins CI/CD Docker Pipeline

Portfolio Edition -- 2025
