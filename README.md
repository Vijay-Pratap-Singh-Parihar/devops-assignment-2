# DevOps Assignment 2 - End-to-End CI/CD Pipeline

## Project Overview

This project provides a production-oriented CI/CD reference for a Flask-based microservice, `ACEest_Fitness`, including:

- A modular Flask API with health and mock business endpoints
- Unit testing with pytest
- Containerization with Docker
- Jenkins declarative pipeline for CI/CD automation
- SonarQube static analysis integration
- Kubernetes deployment manifests with multiple rollout strategies

## Tools and Technologies

- Python 3.9, Flask, Gunicorn
- Pytest
- Docker
- Jenkins
- SonarQube + SonarScanner
- Kubernetes (Minikube-compatible)

## Project Structure

```text
devops-assignment-2/
├── app/
│   ├── __init__.py
│   └── ACEest_Fitness.py
├── tests/
│   └── test_app.py
├── k8s/
│   ├── ab-testing.yaml
│   ├── blue-green.yaml
│   ├── canary.yaml
│   └── shadow.yaml
├── Dockerfile
├── Jenkinsfile
├── deployment.yaml
├── requirements.txt
├── service.yaml
├── sonar-project.properties
└── README.md
```

## Application Architecture

- `ACEest_Fitness.py` uses an application factory (`create_app`) for clean testability and deployment readiness.
- API endpoints:
  - `GET /health` - service health check
  - `GET /members` - mock gym member dataset
  - `GET /plans` - mock subscription plans
- Error handling:
  - Handles HTTP exceptions with structured JSON responses
  - Handles unexpected exceptions with safe `500` response payloads

## Local Setup and Run

### 1) Create virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows PowerShell
pip install -r requirements.txt
```

### 2) Run Flask app locally

```bash
python app/ACEest_Fitness.py
```

Service runs at `http://localhost:5000`.

Quick checks:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/members
curl http://localhost:5000/plans
```

### 3) Run tests

```bash
pytest -v
```

## Docker Usage

### Build image

```bash
docker build -t docker.io/library/devops-assignment-2:latest .
```

### Run container

```bash
docker run -d -p 5000:5000 --name aceest-fitness docker.io/library/devops-assignment-2:latest
```

## Kubernetes Deployment (Minikube)

### Prerequisites

- Minikube and kubectl installed
- Docker image available to cluster (via Docker Hub or local Minikube Docker daemon)

### Deploy default rolling update setup

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods,svc
```

Access service:

```bash
minikube service aceest-fitness-service --url
```

## Deployment Strategies Included

- **Rolling Update**: `deployment.yaml` + `service.yaml`
- **Blue-Green**: `k8s/blue-green.yaml` (switch service selector from `track: blue` to `track: green`)
- **Canary**: `k8s/canary.yaml` (stable and canary replicas for weighted rollout approximation)
- **A/B Testing**: `k8s/ab-testing.yaml` (version-based labels for controlled routing)
- **Shadow Deployment**: `k8s/shadow.yaml` (secondary deployment not exposed via primary service)

Apply any strategy:

```bash
kubectl apply -f k8s/<strategy-file>.yaml
```

## CI/CD Pipeline (Jenkins)

`Jenkinsfile` defines a declarative pipeline with these stages:

1. Clone repository (`checkout scm`)
2. Install dependencies in isolated virtual environment
3. Run pytest test suite
4. Trigger SonarQube scan
5. Build Docker image
6. Push image to Docker Hub (credentials via Jenkins credential store)

### Required Jenkins Configuration

- SonarQube server configured with name: `SonarQubeServer`
- Docker Hub credentials configured with ID: `dockerhub-credentials`
- Agent with Python 3, Docker, and SonarScanner available

## SonarQube Configuration

`sonar-project.properties` includes:

- Python source scanning (`app/`)
- Test path configuration (`tests/`)
- UTF-8 encoding and Python version settings

## Best Practices Applied

- Modular app factory design for scalability and testability
- Explicit dependency pinning in `requirements.txt`
- Structured JSON responses and safe error handling
- Health/readiness-oriented endpoint for orchestration checks
- Kubernetes liveness/readiness probes
- Clean CI/CD stages with separated responsibilities