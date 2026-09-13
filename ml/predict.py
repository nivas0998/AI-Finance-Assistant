import os
import joblib


MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "expense_category_model.joblib"
)


if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "ML model not found. Run train_model.py first."
    )


model = joblib.load(MODEL_PATH)


def predict_category(description):
    description = str(description).strip()

    if not description:
        return {
            "category": "Other",
            "confidence": 0
        }

    prediction = model.predict([description])[0]

    probabilities = model.predict_proba([description])[0]

    confidence = max(probabilities) * 100

    return {
        "category": prediction,
        "confidence": round(float(confidence), 2)
    }