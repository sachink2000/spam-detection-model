import requests

# Single prediction
resp = requests.post("http://localhost:8000/predict", json={"message": "Congratulations, you won a prize!"})
print("Single Prediction:", resp.json())

# Batch prediction
batch_data = {
    "messages": [
        "Meeting at 10?",
        "Claim your free vacation now!",
        "Are we still on for dinner?"
    ]
}
resp = requests.post("http://localhost:8000/predict_batch", json=batch_data)
print("Batch Prediction:", resp.json())
