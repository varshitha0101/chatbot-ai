import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from services.training_data import training_sentences, training_labels

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")
MODEL_PATH = os.path.join(BASE_DIR, "emotion_model.pkl")

model_info = {}


# ---------------------------------
# Train and Evaluate Model
# ---------------------------------
def train_and_save_model():
    global model_info

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(training_sentences)
    y = training_labels

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\nModel Evaluation")
    print("Accuracy:", accuracy)
    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    model_info = {
        "accuracy": accuracy,
        "classes": list(model.classes_),
        "training_samples": len(training_sentences)
    }

    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    return vectorizer, model


# ---------------------------------
# Safe Load or Retrain
# ---------------------------------
def load_or_train():
    try:
        if os.path.exists(VECTORIZER_PATH) and os.path.exists(MODEL_PATH):
            with open(VECTORIZER_PATH, "rb") as f:
                vectorizer = pickle.load(f)

            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)

            return vectorizer, model
        else:
            return train_and_save_model()
    except Exception:
        return train_and_save_model()


vectorizer, model = load_or_train()


# ---------------------------------
# Emotion Detection with Confidence
# ---------------------------------
def detect_emotion(text, threshold=0.55):
    X = vectorizer.transform([text])

    probabilities = model.predict_proba(X)[0]
    classes = model.classes_

    max_index = probabilities.argmax()
    emotion = classes[max_index]
    confidence = float(probabilities[max_index])

    if confidence < threshold:
        emotion = "uncertain"

    intensity = detect_intensity(text)

    return emotion, intensity, round(confidence, 4)


# ---------------------------------
# Intensity Detection (Enhanced)
# ---------------------------------
def detect_intensity(text):
    text = text.lower()

    # Critical/crisis level indicators
    critical_words = [
        "suicidal", "suicide", "kill myself", "end it all",
        "can't go on", "want to die", "no point living"
    ]
    
    for word in critical_words:
        if word in text:
            return "critical"

    # High intensity indicators
    high_intensity_words = [
        "extremely", "very", "so much", "terribly", "overwhelmed",
        "panic", "cannot handle", "completely", "totally",
        "unbearable", "can't take it", "breaking down", "falling apart",
        "drowning", "crushing", "suffocating", "devastating",
        "can't cope", "too much", "can't breathe", "losing it",
        "going crazy", "out of control"
    ]

    # Count intensity markers
    intensity_score = 0
    for word in high_intensity_words:
        if word in text:
            intensity_score += 1
    
    # Multiple exclamation marks
    if text.count('!') >= 2:
        intensity_score += 1
    
    # All caps words (at least 4 chars)
    words = text.split()
    caps_count = sum(1 for w in words if len(w) >= 4 and w.isupper())
    if caps_count >= 2:
        intensity_score += 1

    if intensity_score >= 2:
        return "high"
    elif intensity_score == 1:
        return "medium"
    
    return "low"


# ---------------------------------
# Model Metrics
# ---------------------------------
def get_model_metrics():
    return model_info