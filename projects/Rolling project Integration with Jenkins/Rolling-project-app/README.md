# Flask AWS Monitor -- CI/CD with Jenkins

This repository is part of the **Rolling Project -- CI/CD Integration
with Jenkins**.

It demonstrates a complete DevOps workflow that includes: - Source
control with GitHub - Continuous Integration with Jenkins - Code quality
checks (linting) - Security scanning - Docker image build - Automated
push to Docker Hub

------------------------------------------------------------------------

## 📦 Project Structure

    flask-aws-monitor/
    ├── Jenkinsfile
    ├── Dockerfile
    ├── app.py
    ├── requirements.txt
    ├── README.md
    └── .gitignore

------------------------------------------------------------------------

## 🚀 CI/CD Pipeline Overview

The Jenkins pipeline performs the following stages:

1.  **Checkout Repository**
    -   Clones the project from GitHub
2.  **Parallel Quality & Security Checks**
    -   Python linting (Flake8)
    -   Shell script linting (ShellCheck)
    -   Dockerfile linting (Hadolint)
    -   Python security scanning (Bandit)
    -   Filesystem security scanning (Trivy)
3.  **Build Docker Image**
    -   Builds a Docker container using the project's Dockerfile
    -   Tags the image with the Jenkins build number
4.  **Security Scan (Image Level)**
    -   Scans the built container image using Trivy
5.  **Push to Docker Hub**
    -   Authenticates using Jenkins credentials
    -   Pushes the image:
        -   `nixonp95/flask-aws-monitor:<build_number>`
        -   `nixonp95/flask-aws-monitor:latest`

------------------------------------------------------------------------

## 🐳 Docker Image

Docker Hub repository:

    nixonp95/flask-aws-monitor

After a successful Jenkins run, new tags will appear automatically.

------------------------------------------------------------------------

## ⚙️ Prerequisites

-   Docker installed
-   Jenkins running (via Docker Compose on Builder EC2)
-   Docker Hub account
-   Jenkins credentials configured:
    -   ID: `dockerhub-creds`
    -   Username: `nixonp95`
    -   Password: Docker Hub Access Token

------------------------------------------------------------------------

## 🧪 Running Locally (Optional)

Build image locally:

    docker build -t flask-aws-monitor .
    docker run -p 5000:5000 flask-aws-monitor

------------------------------------------------------------------------

## 📘 Educational Purpose

This project was built as part of a DevOps learning track and
demonstrates:

-   CI/CD automation
-   Infrastructure mindset
-   Secure container delivery
-   Parallel pipeline execution
-   Integration between GitHub, Jenkins, and Docker Hub

------------------------------------------------------------------------

## 👤 Author

**Docker Hub:** nixonp95\
**Project:** Rolling CI/CD Integration with Jenkins
