import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import pickle
import os

# 🔹 Step 1: Create dataset (we'll improve later)
data = {
    "text": [
        "python machine learning data science pandas numpy",
        "deep learning pytorch computer vision ai",
        "sql data analysis excel dashboard",
        "java spring boot backend microservices",
        "html css javascript react frontend",
        "python data science machine learning projects",
        "c++ embedded systems robotics",
        "tensorflow neural networks ai deep learning"
    ],
    "score": [90, 95, 80, 75, 70, 92, 65, 94]
}

df = pd.DataFrame(data)

# 🔹 Step 2: Convert text → features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])

# 🔹 Step 3: Train model
model = LinearRegression()
model.fit(X, df["score"])

# 🔹 Step 4: Save model
os.makedirs("model", exist_ok=True)

pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

print("✅ Model trained and saved successfully!")