# 🚀 Rolling Project -- Section 5

## CI/CD Integration with Jenkins (Docker + Security + Linting)

------------------------------------------------------------------------

## 📌 Overview

This project demonstrates a complete **CI/CD pipeline implementation
using Jenkins** as part of the Rolling Project.

The pipeline integrates:

-   GitHub (Dev branch)
-   Parallel linting and security checks
-   Docker image build
-   Docker Hub push
-   Image tagging using Jenkins build number

This section proves the ability to automate application delivery from
source code to container registry.

------------------------------------------------------------------------

## 🧱 Technologies Used

-   Jenkins (Pipeline from SCM)
-   Docker
-   Docker Hub
-   Python (Flask app)
-   Flake8 (linting)
-   Bandit (security scan)
-   Trivy (image scan -- optional/mock)
-   Git & GitHub

------------------------------------------------------------------------

## 📁 Project Structure

    infra-automation/
    └── projects/
        └── Rolling project Integration with Jenkins/
            └── Rolling-project-app/
                ├── Jenkinsfile
                ├── Dockerfile
                ├── app.py
                ├── requirements.txt
                ├── README.md
                └── Screenshots/
                    ├── Pipeline Steps 1.png
                    ├── Pipeline Steps 2.png
                    ├── Pipeline Steps 3.png
                    ├── Docker Hub Repositories.png
                    ├── Docker Hub Images.png
                    └── Console Output.png

------------------------------------------------------------------------

## ⚙️ Pipeline Capabilities

The Jenkins pipeline performs the following steps:

### 1️⃣ Checkout

-   Clones the GitHub repository from the **Dev branch**

### 2️⃣ Parallel Checks

Runs simultaneously:

**Linting** - Flake8 (Python) - ShellCheck (mock) - Hadolint (mock)

**Security** - Bandit (Python security scan) - Trivy filesystem scan
(mock)

### 3️⃣ Docker Build

-   Builds image from project Dockerfile

### 4️⃣ Image Tagging

-   Tags image with:
    -   Jenkins build number
    -   `latest`

### 5️⃣ Docker Push

-   Pushes image to Docker Hub repository

------------------------------------------------------------------------

## 🐳 Docker Hub Repository

Images pushed automatically to:

    nixonp95/flask-aws-monitor

Tags created: - `latest` - `<build-number>`

Example:

    nixonp95/flask-aws-monitor:5
    nixonp95/flask-aws-monitor:latest

------------------------------------------------------------------------

## 🔐 Jenkins Credentials

The pipeline uses stored Docker Hub credentials:

    ID: dockerhub-creds
    Type: Username + Password / Access Token

Used for secure authentication during image push.

------------------------------------------------------------------------

## 📸 Pipeline Execution Proof (Section 5)

Below are screenshots demonstrating a successful CI/CD run using
Jenkins.

### 1️⃣ Pipeline Execution -- All Stages Green

These screenshots show the pipeline stages completing successfully:

![Pipeline Step 1](Screenshots/Pipeline%20Steps%201.png)\
![Pipeline Step 2](Screenshots/Pipeline%20Steps%202.png)\
![Pipeline Step 3](Screenshots/Pipeline%20Steps%203.png)

------------------------------------------------------------------------

### 2️⃣ Console Output -- Image Push Confirmation

Proof that the Docker image was built and pushed successfully:

![Console Output](Screenshots/Console%20Output.png)

------------------------------------------------------------------------

### 3️⃣ Docker Hub Repository -- Image Verification

Repository and image tags created by Jenkins:

![Docker Hub Repositories](Screenshots/Docker%20Hub%20Repositories.png)\
![Docker Hub Images](Screenshots/Docker%20Hub%20Images.png)

Repository: https://hub.docker.com/r/nixonp95/flask-aws-monitor

------------------------------------------------------------------------

## 🧪 How to Run Locally

Pull and run the image:

``` bash
docker pull nixonp95/flask-aws-monitor:latest
docker run -p 5000:5000 nixonp95/flask-aws-monitor:latest
```

Then open:

    http://localhost:5000

------------------------------------------------------------------------

## 🎯 Learning Outcomes

This section demonstrates the ability to:

-   Design a Jenkins CI/CD pipeline
-   Use parallel stages
-   Integrate linting and security scanning
-   Build Docker images automatically
-   Authenticate securely with Docker Hub
-   Push versioned container images
-   Debug real CI failures
-   Maintain reproducible builds

------------------------------------------------------------------------

## 👤 Author

**Nikita Pozniak**\
DevOps Student -- Class 35690

Rolling Project -- Section 5\
CI/CD Integration with Jenkins
