# DevSecOps Container Vulnerability Scanner 🛡️

An enterprise-grade DevSecOps platform built to scan Docker containers for security vulnerabilities, enforce Quality Gates, and visualize CVEs on a modern dashboard.

## 🌟 Features
- **Container Scanning:** Scans local and public Docker images using the Aqua Security Trivy engine.
- **Quality Gate Enforcement:** Automatically blocks and fails images if Critical or High vulnerabilities are detected.
- **Enterprise Dashboard:** Clean, responsive, Atlassian-style UI built with vanilla HTML/CSS/JS.
- **API Backend:** Python FastAPI backend to orchestrate the scanning and JSON parsing.
- **Dependency Patching Examples:** Includes a Dockerfile demonstrating how to transition from vulnerable base images (`slim`) to secure ones (`alpine`) and patch core Python dependencies.

## 🛠️ Tech Stack
- **Backend:** Python 3.11, FastAPI, Uvicorn
- **Security Engine:** Trivy, Docker
- **Frontend:** HTML5, CSS3 (Enterprise SaaS Theme), JavaScript (Vanilla)

## 🚀 How to Run Locally

### Prerequisites
1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure it is running.
2. Install [Python 3.11+](https://www.python.org/downloads/).

### 1. Start the Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 2. Open the Dashboard
Simply open the `frontend/index.html` file in your preferred web browser.

## 💡 How It Works
1. Enter the name of a Docker image (e.g., `nginx:latest`, `node:18` or a locally built image) in the scanner dashboard.
2. The FastAPI backend triggers a Docker container running Trivy via the Docker Socket.
3. Trivy updates from the official NVD/CVE database, scans the target image, and returns the vulnerabilities.
4. The backend parses the data and applies the Quality Gate logic (Fail if High/Critical > 0).
5. The frontend displays the results, highlighting the package name, CVE ID, and providing a direct link to the NVD database for further investigation.

## 📜 Disclaimer
This project is a Proof of Concept (PoC) demonstrating DevSecOps continuous security scanning principles, built from scratch to understand the underlying mechanics of commercial vulnerability scanners.
