import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


training_data = [
    # Food
    ("lunch", "Food"),
    ("dinner", "Food"),
    ("breakfast", "Food"),
    ("restaurant", "Food"),
    ("food", "Food"),
    ("pizza", "Food"),
    ("burger", "Food"),
    ("biryani", "Food"),
    ("coffee", "Food"),
    ("swiggy", "Food"),
    ("zomato", "Food"),
    ("canteen", "Food"),
    ("snacks", "Food"),
    ("grocery food", "Food"),

    # Transport
    ("bus ticket", "Transport"),
    ("bus", "Transport"),
    ("uber", "Transport"),
    ("ola", "Transport"),
    ("cab", "Transport"),
    ("taxi", "Transport"),
    ("auto", "Transport"),
    ("petrol", "Transport"),
    ("diesel", "Transport"),
    ("fuel", "Transport"),
    ("train ticket", "Transport"),
    ("metro", "Transport"),
    ("transport", "Transport"),

    # Shopping
    ("shopping", "Shopping"),
    ("clothes", "Shopping"),
    ("shirt", "Shopping"),
    ("shoes", "Shopping"),
    ("amazon", "Shopping"),
    ("flipkart", "Shopping"),
    ("online shopping", "Shopping"),
    ("dress", "Shopping"),
    ("watch", "Shopping"),
    ("accessories", "Shopping"),
    ("mall", "Shopping"),

    # Bills
    ("electricity bill", "Bills"),
    ("water bill", "Bills"),
    ("internet bill", "Bills"),
    ("phone bill", "Bills"),
    ("mobile recharge", "Bills"),
    ("recharge", "Bills"),
    ("rent", "Bills"),
    ("wifi bill", "Bills"),
    ("gas bill", "Bills"),
    ("utility bill", "Bills"),

    # Entertainment
    ("movie", "Entertainment"),
    ("cinema", "Entertainment"),
    ("netflix", "Entertainment"),
    ("spotify", "Entertainment"),
    ("game", "Entertainment"),
    ("gaming", "Entertainment"),
    ("concert", "Entertainment"),
    ("youtube premium", "Entertainment"),
    ("entertainment", "Entertainment"),

    # Health
    ("doctor", "Health"),
    ("hospital", "Health"),
    ("medicine", "Health"),
    ("medical", "Health"),
    ("pharmacy", "Health"),
    ("health checkup", "Health"),
    ("clinic", "Health"),
    ("tablet medicine", "Health"),

    # Education
    ("college fee", "Education"),
    ("school fee", "Education"),
    ("course", "Education"),
    ("books", "Education"),
    ("textbook", "Education"),
    ("online course", "Education"),
    ("udemy", "Education"),
    ("exam fee", "Education"),
    ("education", "Education"),
    ("tuition", "Education"),

    # Other
    ("gift", "Other"),
    ("donation", "Other"),
    ("miscellaneous", "Other"),
    ("other expense", "Other"),
    ("unknown expense", "Other"),
]


descriptions = [item[0] for item in training_data]
categories = [item[1] for item in training_data]


model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


model.fit(descriptions, categories)


os.makedirs("ml", exist_ok=True)

model_path = os.path.join("ml", "expense_category_model.joblib")

joblib.dump(model, model_path)

print("Model trained successfully.")
print(f"Model saved at: {model_path}")
print("Categories:", sorted(set(categories)))