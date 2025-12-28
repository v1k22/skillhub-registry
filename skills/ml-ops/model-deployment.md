---
metadata:
  name: "model-deployment"
  version: "1.0.0"
  description: "Deploy ML model as REST API using FastAPI with Docker containerization"
  category: "ml-ops"
  tags: ["mlops", "deployment", "fastapi", "docker", "ml"]
  author: "skillhub"
  created: "2024-01-15"
  updated: "2024-01-15"

requirements:
  os: ["linux", "macos", "windows"]
  python: ">=3.9"
  packages:
    - fastapi>=0.104.0
    - uvicorn>=0.24.0
    - pydantic>=2.0.0
    - scikit-learn>=1.3.0
    - joblib
  hardware:
    - ram: ">=4GB"
    - disk_space: ">=2GB"

estimated_time: "30-40 minutes"
difficulty: "intermediate"
---

# ML Model Deployment

## Overview
This skill deploys a machine learning model as a production-ready REST API using FastAPI, with Docker containerization for easy deployment. Includes model versioning, input validation, logging, and health checks.

## Task Description
Complete ML deployment workflow:
1. Train and save a sample ML model
2. Create FastAPI application with prediction endpoints
3. Add input validation and error handling
4. Implement health checks and monitoring
5. Create Dockerfile for containerization
6. Build and test Docker container
7. Deploy and test the API

## Prerequisites
- Python 3.9+ installed
- Docker installed (for containerization)
- Basic ML and API understanding
- Trained ML model (we'll create a sample)

## Steps

### 1. Environment Setup
```bash
# Create project directory
mkdir ml_api
cd ml_api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pydantic scikit-learn joblib pandas
```

### 2. Create Project Structure
```bash
# Create directories
mkdir -p {models,app,tests}

# Create requirements file
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
scikit-learn==1.3.2
joblib==1.3.2
pandas==2.1.3
numpy==1.26.2
python-multipart==0.0.6
EOF
```

### 3. Train Sample Model
```python
# train_model.py
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json

def train_model():
    """Train a sample iris classification model."""
    print("Loading data...")
    iris = load_iris()
    X, y = iris.data, iris.target

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    print("Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=iris.target_names))

    # Save model
    joblib.dump(model, 'models/iris_model.joblib')
    print("\nModel saved to models/iris_model.joblib")

    # Save metadata
    metadata = {
        'model_type': 'RandomForestClassifier',
        'accuracy': accuracy,
        'features': iris.feature_names,
        'target_names': iris.target_names.tolist(),
        'version': '1.0.0'
    }

    with open('models/model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    print("Metadata saved to models/model_metadata.json")

    return model, metadata

if __name__ == '__main__':
    train_model()
```

```bash
# Run training
python train_model.py
```

### 4. Create Pydantic Models
```python
# app/schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import List

class PredictionInput(BaseModel):
    """Input schema for predictions."""
    sepal_length: float = Field(..., ge=0, le=10, description="Sepal length in cm")
    sepal_width: float = Field(..., ge=0, le=10, description="Sepal width in cm")
    petal_length: float = Field(..., ge=0, le=10, description="Petal length in cm")
    petal_width: float = Field(..., ge=0, le=10, description="Petal width in cm")

    @field_validator('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
    @classmethod
    def check_positive(cls, v):
        if v < 0:
            raise ValueError('Value must be positive')
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2
                }
            ]
        }
    }

class PredictionOutput(BaseModel):
    """Output schema for predictions."""
    prediction: str
    confidence: float
    probabilities: dict
    model_version: str

class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    version: str
```

### 5. Create FastAPI Application
```python
# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import json
import numpy as np
from pathlib import Path
import logging
from app.schemas import PredictionInput, PredictionOutput, HealthCheck

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Iris Classification API",
    description="ML model API for iris flower classification",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
model = None
metadata = None

@app.on_event("startup")
async def load_model():
    """Load model on startup."""
    global model, metadata

    try:
        logger.info("Loading model...")
        model = joblib.load('models/iris_model.joblib')

        logger.info("Loading metadata...")
        with open('models/model_metadata.json', 'r') as f:
            metadata = json.load(f)

        logger.info("Model loaded successfully!")

    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise

@app.get("/", tags=["General"])
async def root():
    """Root endpoint."""
    return {
        "message": "Iris Classification API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthCheck, tags=["General"])
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        version=metadata.get('version', 'unknown') if metadata else 'unknown'
    )

@app.get("/model/info", tags=["Model"])
async def model_info():
    """Get model information."""
    if metadata is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return metadata

@app.post("/predict", response_model=PredictionOutput, tags=["Predictions"])
async def predict(input_data: PredictionInput):
    """Make a prediction."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Prepare input
        features = np.array([[
            input_data.sepal_length,
            input_data.sepal_width,
            input_data.petal_length,
            input_data.petal_width
        ]])

        # Make prediction
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]

        # Get class name
        class_name = metadata['target_names'][prediction]

        # Prepare response
        return PredictionOutput(
            prediction=class_name,
            confidence=float(max(probabilities)),
            probabilities={
                name: float(prob)
                for name, prob in zip(metadata['target_names'], probabilities)
            },
            model_version=metadata['version']
        )

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch", tags=["Predictions"])
async def predict_batch(inputs: List[PredictionInput]):
    """Make batch predictions."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        results = []

        for input_data in inputs:
            features = np.array([[
                input_data.sepal_length,
                input_data.sepal_width,
                input_data.petal_length,
                input_data.petal_width
            ]])

            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]

            results.append({
                "prediction": metadata['target_names'][prediction],
                "confidence": float(max(probabilities))
            })

        return {"predictions": results, "count": len(results)}

    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 6. Create Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 7. Create Docker Compose (Optional)
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    environment:
      - LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 8. Build and Run

**Option A: Run with Python**
```bash
# Run directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Visit http://localhost:8000/docs for API documentation
```

**Option B: Run with Docker**
```bash
# Build Docker image
docker build -t iris-api:latest .

# Run container
docker run -p 8000:8000 iris-api:latest

# Or use Docker Compose
docker-compose up -d
```

### 9. Test the API
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'

# Get model info
curl http://localhost:8000/model/info
```

### 10. Test with Python Script
```python
# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health Check: {response.json()}")

def test_prediction():
    """Test prediction endpoint."""
    data = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"\nPrediction: {json.dumps(response.json(), indent=2)}")

def test_model_info():
    """Test model info endpoint."""
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"\nModel Info: {json.dumps(response.json(), indent=2)}")

if __name__ == '__main__':
    test_health()
    test_prediction()
    test_model_info()
```

```bash
# Run tests
python test_api.py
```

## Expected Output
- FastAPI server running on http://localhost:8000
- Interactive API docs at http://localhost:8000/docs
- Health check endpoint returning status
- Prediction endpoint returning class and confidence
- Docker container running successfully
- All API tests passing

## Troubleshooting

### Model Not Found Error
```bash
# Ensure model is trained first
python train_model.py

# Check model exists
ls -lh models/
```

### Port Already in Use
```bash
# Use different port
uvicorn app.main:app --port 8001

# Or in Dockerfile, change EXPOSE and CMD
```

### Docker Build Fails
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t iris-api:latest .
```

### Import Errors
```bash
# Ensure app/__init__.py exists
touch app/__init__.py

# Run from project root
cd ml_api
uvicorn app.main:app
```

## Success Criteria
- [x] Model trained and saved successfully
- [x] FastAPI server starts without errors
- [x] Health check endpoint returns 200 OK
- [x] Prediction endpoint returns correct results
- [x] API documentation accessible at /docs
- [x] Docker container builds successfully
- [x] Docker container runs and responds to requests
- [x] All test requests complete successfully

## Next Steps
- Add authentication (JWT tokens)
- Implement rate limiting
- Add model monitoring and drift detection
- Set up CI/CD pipeline
- Deploy to cloud (AWS, GCP, Azure)
- Add A/B testing for model versions
- Implement caching for predictions
- Add Prometheus metrics

## Related Skills
- `setup-kubernetes-deployment`
- `add-api-authentication`
- `model-monitoring`
- `cicd-ml-pipeline`

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Scikit-learn Model Persistence](https://scikit-learn.org/stable/model_persistence.html)
- [MLOps Best Practices](https://ml-ops.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
