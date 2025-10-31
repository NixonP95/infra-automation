# 🛠 DevOps Infrastructure Provisioning & AWS Projects (Rolling Collection)

## 📌 Overview
This repository documents **three major infrastructure projects**, built progressively during the DevOps learning path:

1. **Infrastructure Provisioning & Configuration Automation** (Python + Bash simulator).  
2. **AWS Resource Dashboard (Rolling project AWS)** — a Flask + boto3 web dashboard.  
3. **Terraform EC2 Builder** — a full Infrastructure-as-Code deployment on AWS using Terraform.

All three projects are **independent**, but share the same goal: demonstrating **automation, IaC, and cloud provisioning** best practices.

---

## 📦 Project A — Infrastructure Provisioning & Configuration Automation

A **Python + Bash simulator** that walks through VM provisioning, input validation, JSON persistence, and logging.

### ✨ Features
- Modular Python OOP design (`machine.py`, `infra_simulator.py`)  
- Bash-based service automation (e.g., Nginx installation)  
- Logging and error handling (`logs/provisioning.log`)  
- Configuration persistence using `configs/instances.json`

### 📁 Structure
```text
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

---

## ☁️ Project B — AWS Resource Dashboard (Flask + boto3)

A **Flask web app** that runs locally and connects to your AWS account to display live data for EC2 instances, VPCs, AMIs, and Load Balancers.  
Proof-of-concept screenshots are stored under `AWS/Screenshots/`.

### 📁 Structure
```text
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

### 🚀 Run the AWS Dashboard
```bash
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

Then visit:  
👉 `http://localhost:5001/`  
Health check: `http://localhost:5001/healthz`

---

## 🌍 Project C — Terraform EC2 Builder 

# ☁️ Terraform EC2 Builder (Portfolio Version)

This Terraform configuration demonstrates **Infrastructure-as-Code (IaC)** principles by provisioning a Docker-ready EC2 instance in AWS.

> 🔒 Sensitive IDs and IP addresses have been masked for security.

---

## 🧱 Resources Reference
- **VPC ID:** `vpc-xxxxxxxxxxxxxxxxx`
- **Subnet ID:** `subnet-xxxxxxxxxxxxxxxxx`
- **Region:** `us-east-1`

---

## ⚙️ Overview
This configuration:
- Generates a secure SSH key pair (local + AWS)
- Creates a security group allowing:
  - SSH (22) and App (5001) access from your IP
- Launches an **Ubuntu EC2 instance**
- Installs **Docker** automatically via `user_data`
- Outputs the instance’s public IP for verification

---

## 🧩 Project Structure
```text
Rolling project Terraform/
├── main.tf
├── variables.tf
├── providers.tf
├── versions.tf
├── outputs.tf
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

```bash
terraform init
terraform plan
terraform apply -auto-approve
```

Once created:

```bash
terraform output -raw instance_public_ip
```

Connect via SSH:

```bash
chmod 600 <your_key>.pem
ssh -i <your_key>.pem ubuntu@<public_ip>
```

---

## 🧾 Key Highlights
- Written in **Terraform (HCL)** with version pinning  
- Uses **data lookups** for Ubuntu AMIs  
- Validates subnet/VPC match via a precondition  
- Demonstrates modular IaC design and secure key management  
- Installs Docker automatically with no manual setup required

---

## 📦 Tools Used
- Terraform 1.5+
- AWS CLI 2.x
- Ubuntu 22.04 AMI
- Docker CE

---

## 👤 Author
**Nikita Pozniak**  
DevOps Student – Class 35690  
Project: *Terraform EC2 Builder*  
Public Portfolio Edition – 2025
