# Spam Detection Model API

A FastAPI-based web service for spam detection using machine learning. This application provides REST API endpoints to classify text messages as either SPAM or HAM (legitimate messages).

**Repository**: https://github.com/sachink2000/spam-detection-model.git

## Features

- Single message prediction endpoint
- Batch message prediction endpoint
- Docker containerization support
- Environment variable configuration
- Comprehensive logging
- Machine learning model integration using scikit-learn

## Visual Documentation

This repository includes visual demonstrations of the API functionality:

- vscode.jpg: Shows the development environment setup in Visual Studio Code, demonstrating the project structure and file organization
- single-execution.jpg: Demonstrates the single message prediction endpoint in action, showing how to test individual messages for spam detection
- batch-execution.jpg: Illustrates the batch prediction functionality, showing how multiple messages can be processed simultaneously

These images serve as visual guides to help users understand the API usage patterns and expected outputs when testing the spam detection functionality.

## Prerequisites

- Python 3.13 or higher
- Docker (optional, for containerized deployment)
- Machine learning model file (spam_model.pkl)

## Installation

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sachink2000/spam-detection-model.git
   cd spam-detection-model
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows: '.venv\Scripts\activate'
   - Linux/Mac: 'source .venv/bin/activate'

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Model Training

Before running the API, you need to train and save a spam detection model:

1. **Prepare your dataset**: Collect labeled spam/ham messages in a format suitable for training
2. **Train the model**: Use scikit-learn to create a text classification model
3. **Save the model**: Use joblib to save your trained model as `spam_model.pkl`

Example training script structure:
-----python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

# Create and train your model
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

# Train with your data
pipeline.fit(X_train, y_train)

# Save the model
joblib.dump(pipeline, 'model/spam_model.pkl')
----

4. **Place the model**: Ensure your trained model file is located at `model/spam_model.pkl` or set the `MODEL_PATH` environment variable

## Configuration

Create a `.env` file in the project root with the following variables:

-------
MODEL_PATH=model/spam_model.pkl
LOG_LEVEL=INFO
-------

## Running the Application

### Local Development

1. Start the FastAPI server:
  -----
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  -----

2. The API will be available at:
   - Local access: `http://localhost:8000`
   - Network access: `http://YOUR_IP_ADDRESS:8000`

### Docker Deployment

#### Building the Docker Image

1. Build the Docker image:
  -----
   docker build -t spam-detector .
  -----

#### Running the Docker Container

1. **Private Access** (localhost only):
  -----
   docker run -p 8000:8000 spam-detector
  -----
   Access at: `http://localhost:8000`

2. **Public Access** (accessible from other machines):
  -----
   docker run -p 0.0.0.0:8000:8000 spam-detector
  -----
   Access at: `http://YOUR_SERVER_IP:8000`

3. **With environment variables**:
  -----
   docker run -p 8000:8000 -e MODEL_PATH=model/spam_model.pkl -e LOG_LEVEL=DEBUG spam-detector
  -----

4. **With volume mounting** (to use external model file):
  -----
   docker run -p 8000:8000 -v /path/to/your/model:/app/model spam-detector
  -----

## API Endpoints

### Interactive Documentation

Once the server is running, access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Single Message Prediction

**Endpoint**: `POST /predict`

**Request Body**:
-----json
{
  "message": "Congratulations! You've won a free iPhone. Click here to claim!"
}
-----

**Response**:
-----json
{
  "prediction": "SPAM"
}
-----

### Batch Message Prediction

**Endpoint**: `POST /predict_batch`

**Request Body**:
-----json
{
  "messages": [
    "Congratulations! You've won a free iPhone. Click here to claim!",
    "Hey, are we still meeting for lunch today?",
    "URGENT: Your account will be suspended. Click here immediately!"
  ]
}
-----

**Response**:
-----json
{
  "predictions": ["SPAM", "HAM", "SPAM"]
}
-----

## Testing the API

The repository includes visual examples of API testing in the image files `single-execution.jpg` and `batch-execution.jpg` that demonstrate the expected behavior and responses.

### Using curl

1. **Single prediction**:
  -----bash
   curl -X POST "http://localhost:8000/predict" \
        -H "Content-Type: application/json" \
        -d '{"message": "Free money! Click now!"}'
  -----

2. **Batch prediction**:
  -----bash
   curl -X POST "http://localhost:8000/predict_batch" \
        -H "Content-Type: application/json" \
        -d '{"messages": ["Free money!", "Hello friend"]}'
  -----

### Using Python requests

-----python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={"message": "Free money! Click now!"}
)
print(response.json())

# Batch prediction
response = requests.post(
    "http://localhost:8000/predict_batch",
    json={"messages": ["Free money!", "Hello friend"]}
)
print(response.json())
-----

## Public vs Private Access

### Private Access (Local Network Only)

- **Local Development**: `uvicorn main:app --host 127.0.0.1 --port 8000`
- **Docker**: `docker run -p 127.0.0.1:8000:8000 spam-detector`
- Access: Only from the same machine (`localhost` or `127.0.0.1`)

### Public Access (Network Accessible)

- **Local Development**: `uvicorn main:app --host 0.0.0.0 --port 8000`
- **Docker**: `docker run -p 0.0.0.0:8000:8000 spam-detector`
- Access: From any machine that can reach your server's IP address

**Security Considerations for Public Access**:
- Implement authentication and authorization
- Use HTTPS in production
- Configure firewall rules appropriately
- Consider rate limiting
- Monitor for abuse

## Project Structure

## Project Structure

```
spam-detection-model/
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── dockerfile                # Docker configuration
├── README.md                 # Project documentation
├── .env                      # Environment variables (create this)
├── vscode.jpg                # VS Code development environment screenshot
├── single-execution.jpg      # Single message prediction demo
├── batch-execution.jpg       # Batch prediction demo
└── model/                    # Model directory (create this)
    └── spam_model.pkl        # Trained ML model
```

## Dependencies

The project uses the following main dependencies:

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **scikit-learn**: Machine learning library for model training and inference
- **joblib**: For model serialization and loading
- **python-dotenv**: For loading environment variables from .env files

## Troubleshooting

### Common Issues

1. **Model not found error**:
   - Ensure your model file exists at the specified path
   - Check the `MODEL_PATH` environment variable
   - Verify the model was saved correctly using joblib

2. **Port already in use**:
   - Change the port number: `--port 8001`
   - Kill existing processes using the port

3. **Docker build fails**:
   - Ensure all required files are present
   - Check Docker daemon is running
   - Verify requirements.txt contains all dependencies

4. **Prediction errors**:
   - Check that input text format matches training data
   - Verify model compatibility with current scikit-learn version
   - Review application logs for detailed error messages

## Contributing

1. Ensure your model is properly trained and tested
2. Update documentation for any API changes
3. Test both single and batch prediction endpoints
4. Verify Docker containerization works correctly

## License

This project is provided as-is for educational and development purposes.
