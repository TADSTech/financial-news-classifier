# Deployment Guide

Deploy Financial News Classifier to various environments.

---

## Overview

This guide covers deployment options:
- Local development
- Docker containers
- Cloud platforms (AWS, GCP, Azure)
- Production setup
- Scaling considerations

---

## Local Development

### Single Machine Setup

**Requirements:**
- Python 3.10+
- 4GB RAM minimum
- 2GB disk space

**Steps:**
```bash
# Clone and setup
git clone https://github.com/TADSTech/financial-news-classifier.git
cd financial-news-classifier

# Create environment
python -m venv .venv
source .venv/bin/activate

# Install package
pip install .

# Run CLI
fnc --help

# Launch GUI
fnc gui
```

### GPU Setup (Optional)

**NVIDIA GPU Requirements:**
- CUDA 11.8+
- cuDNN 8.0+
- 2GB VRAM minimum

**Installation:**
```bash
# Install CUDA-enabled PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Verify GPU
fnc info
```

---

## Docker Deployment

### Basic Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir .

# Expose GUI port
EXPOSE 7860

# Default command
CMD ["fnc", "gui"]
```

### Build and Run

```bash
# Build image
docker build -t financial-classifier .

# Run with GPU support
docker run --gpus all -p 7860:7860 financial-classifier

# Run CPU-only
docker run -p 7860:7860 financial-classifier

# Run with file mounting
docker run -v /path/to/data:/data -p 7860:7860 financial-classifier
```

### Docker Compose

```yaml
version: '3.8'

services:
  classifier:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./data:/data
    environment:
      - DEVICE=auto
      - BATCH_SIZE=32
    # GPU support
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]
```

**Start service:**
```bash
docker-compose up -d
```

---

## Production Setup

### Systemd Service (Linux)

Create `/etc/systemd/system/financial-classifier.service`:

```ini
[Unit]
Description=Financial News Classifier
After=network.target

[Service]
Type=simple
User=classifier
WorkingDirectory=/opt/financial-classifier
ExecStart=/opt/financial-classifier/.venv/bin/fnc gui
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable financial-classifier
sudo systemctl start financial-classifier
sudo systemctl status financial-classifier
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name classifier.example.com;

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Enable:**
```bash
sudo ln -s /etc/nginx/sites-available/classifier /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Cloud Platforms

### AWS Deployment

#### Option 1: EC2 Instance

```bash
# Launch Ubuntu 22.04 instance
# SSH into instance

# Install dependencies
sudo apt update && sudo apt install -y python3.10 python3-pip

# Clone and setup
git clone https://github.com/TADSTech/financial-news-classifier.git
cd financial-news-classifier

python3 -m venv .venv
source .venv/bin/activate
pip install .

# Run with nohup (background)
nohup fnc gui --host 0.0.0.0 &
```

#### Option 2: ECS Container

Create `task-definition.json`:
```json
{
  "family": "financial-classifier",
  "containerDefinitions": [
    {
      "name": "classifier",
      "image": "financial-classifier:latest",
      "portMappings": [{"containerPort": 7860}],
      "memory": 2048,
      "cpu": 512
    }
  ]
}
```

Register and run:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster default --service-name classifier --task-definition financial-classifier
```

### Google Cloud

#### Cloud Run

```bash
# Create Dockerfile.cloudrun
# Add entrypoint for Cloud Run

gcloud run deploy financial-classifier \
  --source . \
  --platform managed \
  --memory 2Gi \
  --port 7860 \
  --region us-central1
```

#### Compute Engine

```bash
gcloud compute instances create financial-classifier \
  --image-family ubuntu-2204-lts \
  --image-project ubuntu-os-cloud \
  --machine-type n1-standard-2

# SSH and install
gcloud compute ssh financial-classifier

# Installation steps (same as AWS EC2)
```

### Azure

#### App Service

```bash
# Create resource group
az group create -n classifier-rg -l eastus

# Create app service plan
az appservice plan create -n classifier-plan -g classifier-rg --sku B2

# Create web app
az webapp create -n financial-classifier -g classifier-rg -p classifier-plan
```

#### Container Instances

```bash
az container create \
  --resource-group classifier-rg \
  --name financial-classifier \
  --image financial-classifier:latest \
  --cpu 2 --memory 2 \
  --port 7860 \
  --dns-name-label financial-classifier
```

---

## Scaling Considerations

### Load Balancing

Use Docker Swarm or Kubernetes:

```yaml
# docker-compose.yml for swarm
version: '3.8'
services:
  classifier:
    image: financial-classifier:latest
    deploy:
      replicas: 3  # Run 3 instances
      placement:
        constraints: [node.role == worker]
```

**Deploy to swarm:**
```bash
docker stack deploy -c docker-compose.yml classifier
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: financial-classifier
spec:
  replicas: 3
  selector:
    matchLabels:
      app: classifier
  template:
    metadata:
      labels:
        app: classifier
    spec:
      containers:
      - name: classifier
        image: financial-classifier:latest
        ports:
        - containerPort: 7860
        resources:
          limits:
            memory: "2Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: classifier-service
spec:
  selector:
    app: classifier
  ports:
  - port: 80
    targetPort: 7860
  type: LoadBalancer
```

**Deploy:**
```bash
kubectl apply -f deployment.yaml
```

---

## API Server for Batch Processing

Create `api_server.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from core.infer import predict_batch
import logging

app = FastAPI(title="Financial Classifier API")

class PredictionRequest(BaseModel):
    texts: list[str]
    batch_size: int = 32

class PredictionResponse(BaseModel):
    results: list[dict]

@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(request: PredictionRequest):
    """Batch prediction endpoint"""
    results = predict_batch(request.texts, batch_size=request.batch_size)
    return PredictionResponse(results=results)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Install dependencies:**
```bash
pip install fastapi uvicorn
```

**Run server:**
```bash
python api_server.py
```

**Usage:**
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"texts": ["Text 1", "Text 2"], "batch_size": 32}
)
results = response.json()["results"]
```

---

## Monitoring and Logging

### Application Logging

Create `logging_config.yaml`:

```yaml
version: 1
handlers:
  file:
    class: logging.FileHandler
    filename: classifier.log
    level: INFO
  
  console:
    class: logging.StreamHandler
    level: DEBUG

root:
  level: INFO
  handlers: [file, console]
```

### Resource Monitoring

```bash
# CPU and Memory
watch -n 1 'ps aux | grep fnc'

# Docker stats
docker stats financial-classifier

# System monitoring
htop
```

---

## Environment Configuration

### Production .env File

```bash
# Device and performance
DEVICE=cuda
BATCH_SIZE=64
LOG_LEVEL=INFO

# GUI settings
GUI_HOST=0.0.0.0
GUI_PORT=7860

# Security
ALLOWED_HOSTS=classifier.example.com

# Model settings
MODEL_CACHE_DIR=/opt/models
```

### Load from .env

```python
from dotenv import load_dotenv
import os

load_dotenv()

device = os.getenv("DEVICE", "auto")
batch_size = int(os.getenv("BATCH_SIZE", 32))
```

---

## Performance Tuning

### Database Caching

Store predictions in cache:

```python
import redis
from core.infer import predict

r = redis.Redis(host='localhost', port=6379, db=0)

def predict_with_cache(text):
    # Check cache
    cached = r.get(text)
    if cached:
        return json.loads(cached)
    
    # Predict
    result = predict(text)
    
    # Cache for 1 hour
    r.setex(text, 3600, json.dumps(result))
    
    return result
```

### Batch Processing Optimization

```python
# Pre-load model once
from core.infer import ModelLoader
loader = ModelLoader()
loader.load_model()

# Process many batches
def process_multiple_files(file_list):
    for file_path in file_list:
        texts = load_file(file_path)
        results = predict_batch(texts, batch_size=128)
        save_results(results, f"output_{file_path}")
```

---

## Security

### API Authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/predict")
async def predict_endpoint(
    request: PredictionRequest,
    credentials = Depends(security)
):
    # Validate token
    token = credentials.credentials
    if not validate_token(token):
        raise HTTPException(status_code=401)
    
    # Process request
    return predict_batch(request.texts)

def validate_token(token: str) -> bool:
    # Implement token validation
    return token == os.getenv("API_TOKEN")
```

### SSL/TLS

```bash
# Generate self-signed cert
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Use with Nginx
ssl_certificate /etc/nginx/certs/cert.pem;
ssl_certificate_key /etc/nginx/certs/key.pem;
```

---

## Backup and Recovery

### Model Backup

```bash
# Backup local model
tar -czf finbert_backup.tar.gz src/model/saved/finbert/

# Restore
tar -xzf finbert_backup.tar.gz
```

### Database Backup

```bash
# Redis dump
redis-cli --rdb /backups/dump.rdb

# MySQL
mysqldump -u user -p database > backup.sql
```

---

## Troubleshooting Deployment

### Out of Memory

```bash
# Check memory usage
free -h

# Reduce batch size
fnc batch data.csv --batch-size 8

# Enable swap (temporary)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### GPU Issues

```bash
# Check CUDA
nvidia-smi

# Force CPU
fnc classify "text" --device cpu
```

### Port Already in Use

```bash
# Find process using port 7860
sudo lsof -i :7860

# Kill process
kill -9 <PID>

# Use different port
fnc gui --port 8080
```

---

## Maintenance

### Regular Updates

```bash
# Check for updates
git pull

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl restart financial-classifier
```

### Clean Up Cache

```bash
# Clear Hugging Face cache
rm -rf ~/.cache/huggingface/

# Clear Docker images
docker image prune -a

# Clear Docker containers
docker container prune
```

---

## Quick Deploy Scripts

### Auto-Deploy Script

```bash
#!/bin/bash
set -e

echo "Deploying Financial News Classifier..."

# Update code
cd /opt/financial-classifier
git pull

# Install dependencies
source .venv/bin/activate
pip install --upgrade .

# Restart service
sudo systemctl restart financial-classifier

echo "✓ Deployment complete"
```

### Backup and Deploy

```bash
#!/bin/bash
BACKUP_DIR="/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup current state
cp -r /opt/financial-classifier "$BACKUP_DIR/"

# Deploy
cd /opt/financial-classifier
git pull
pip install --upgrade .

# Restart
sudo systemctl restart financial-classifier

echo "✓ Backed up to: $BACKUP_DIR"
```

---

## Cost Optimization

### AWS Cost Reduction

- Use spot instances for development/testing
- Auto-scaling based on demand
- Use EBS-optimized instances
- Enable CloudFront caching

### Resource Allocation

- CPU: 1-2 cores per instance
- Memory: 2-4GB per instance
- Disk: 20-50GB (for model cache)

---

## Related Documents

- [README.md](README.md) - Quick start guide
- [CLI_REFERENCE.md](CLI_REFERENCE.md) - CLI commands
- [API.md](API.md) - Python API reference
- [LOCAL_MODEL_SETUP.md](LOCAL_MODEL_SETUP.md) - Offline setup
