# 🛠 DevOps Infrastructure Provisioning & AWS Dashboard (Rolling Project)

## 📌 Overview
This repository now documents **two related projects**:

1. **Infrastructure Provisioning & Configuration Automation** (the original project in this repo).  
2. **AWS Resource Dashboard (Rolling project AWS – Nikita)** – a new project kept under `projects/` with its own code and screenshots.

Both projects are independent so history stays clean and nothing breaks.

---

## 📌 Project A — Infrastructure Provisioning & Configuration Automation (existing)

A Python + Bash simulator that walks through VM provisioning, input validation, JSON persistence, and logging.

### Features
- Python modular design with classes  
- Input validation (e.g., via `jsonschema`)  
- Service automation with Bash (e.g., Nginx install)  
- Logging and error handling  

### Structure
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

## 📌 Project B — AWS Resource Dashboard (new)

A **Flask + boto3** app that runs on your **local machine** and shows live data from your AWS account (EC2, VPCs, ELB, AMIs).  
**Proof-of-concept screenshots** are stored under `AWS/Screenshots/`.

### Structure
```text
infra-automation/
├─ projects/
│   └─ Rolling project AWS - Nikita/
│       ├─ Python/                      # Application source for the AWS dashboard
│       │   ├─ app.py                   # Flask app
│       │   ├─ requirements.txt         # Flask & boto3 deps
│       │   └─ venv/                    # Local venv (ignored)
│       │
│       └─ AWS/                         # Proof of concept (screenshots only)
│           └─ Screenshots/
│               ├─ local host 5001-1.png
│               ├─ local host 5001-2.png
│               └─ Live EC2 from AWS Console-1.png
```

> Note: The **code** is under `Python/`. The **AWS/Screenshots/** folder contains proof-of-concept images.

---

## 🚀 Run AWS Dashboard

```bash
cd projects/"Rolling project AWS - Nikita"/Python
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt

# Provide AWS creds (env vars)
export AWS_ACCESS_KEY_ID="YOUR_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
export AWS_DEFAULT_REGION="us-east-2"

python app.py
```

Visit:  
👉 `http://localhost:5001/`  
👉 Health check: `http://localhost:5001/healthz`

---

## 🖼 Proof of Concept
Screenshots under:
```
projects/Rolling project AWS - Nikita/AWS/Screenshots/
```
- `local host 5001-1.png` – Dashboard view  
- `local host 5001-2.png` – Extended view  
- `Live EC2 from AWS Console-1.png` – AWS console verification  

---

## 🚫 .gitignore (root of repo)

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.egg-info/
*.egg
*.log

# Virtual environments
venv/
.venv/
env/
ENV/

# OS / editor noise
.DS_Store
Thumbs.db
*.swp
*.swo
*.orig

# Env / secrets
*.env
.env

# Project A (infra-automation)
logs/
configs/instances.json

# Project B (AWS Dashboard)
projects/Rolling project AWS - Nikita/Python/venv/
projects/Rolling project AWS - Nikita/Python/__pycache__/
projects/Rolling project AWS - Nikita/Python/*.pyc
projects/Rolling project AWS - Nikita/Python/.env

# Node / build artifacts
node_modules/
dist/
build/
```
