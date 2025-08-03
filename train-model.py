# train_model.py
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

# Create model directory if not exists
os.makedirs("model", exist_ok=True)

# Training data (very simple sample)
X = [
    "Free money now!!!",
    "Hi, how are you?",
    "Lowest prices on meds",
    "Are you coming to the meeting?",
    "Win cash fast!",
    "Let's meet tomorrow.",
    "Congratulations! You have won!"
]
y = [1, 0, 1, 0, 1, 0, 1]  # 1 = SPAM, 0 = HAM

# Build and train
model = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])
model.fit(X, y)

# Save model
joblib.dump(model, "model/spam_model.pkl")
print("Model saved to model/spam_model.pkl")
