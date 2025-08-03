from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import joblib
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH", "model/spam_model.pkl")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("spam-detector")

# Load model
try:
    model = joblib.load(MODEL_PATH)
    logger.info(f"Model loaded from {MODEL_PATH}")
except Exception as e:
    logger.exception("Failed to load model")
    raise RuntimeError(f"Could not load model: {e}")

# Pydantic models
class TextInput(BaseModel):
    message: str

class BatchTextInput(BaseModel):
    messages: List[str]

# FastAPI app
app = FastAPI()

@app.post("/predict")
def predict(input: TextInput):
    try:
        prediction = model.predict([input.message])[0]
        result = "SPAM" if prediction == 1 else "HAM"
        logger.info(f"Predicted {result} for input: {input.message}")
        return {"prediction": result}
    except Exception as e:
        logger.exception("Error during prediction")
        raise HTTPException(status_code=500, detail="Prediction failed")

@app.post("/predict_batch")
def predict_batch(batch: BatchTextInput):
    try:
        predictions = model.predict(batch.messages)
        results = ["SPAM" if p == 1 else "HAM" for p in predictions]
        logger.info(f"Batch prediction results: {results}")
        return {"predictions": results}
    except Exception as e:
        logger.exception("Batch prediction failed")
        raise HTTPException(status_code=500, detail="Batch prediction failed")
