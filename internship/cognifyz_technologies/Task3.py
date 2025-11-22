import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
DATA_PATH = r"C:\Users\Admin\Documents\cognoz\Dataset .csv"
OUTPUT_DIR = "task3_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

df["Cuisines"] = df["Cuisines"].fillna("Unknown")

df["primary_cuisine"] = df["Cuisines"].apply(lambda x: str(x).split(",")[0].strip().lower())

counts = df["primary_cuisine"].value_counts()
valid_labels = counts[counts >= 50].index.tolist()

df = df[df["primary_cuisine"].isin(valid_labels)].copy()

print("Classes:", df["primary_cuisine"].unique())
print("Total classes:", len(df["primary_cuisine"].unique()))

df["text_data"] = df["Cuisines"].astype(str) + " | " + df["City"].astype(str)

X_text = df["text_data"]
y = df["primary_cuisine"]

vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X = vectorizer.fit_transform(X_text)

joblib.dump(vectorizer, os.path.join(OUTPUT_DIR, "tfidf_vectorizer.joblib"))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
log_reg = LogisticRegression(max_iter=2000)
log_reg.fit(X_train, y_train)

pred_lr = log_reg.predict(X_test)

print("\nLogistic Regression Accuracy:", accuracy_score(y_test, pred_lr))
print("\nLogistic Regression Report:\n")
print(classification_report(y_test, pred_lr))

joblib.dump(log_reg, os.path.join(OUTPUT_DIR, "logistic_model.joblib"))

rf = RandomForestClassifier(n_estimators=250, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

pred_rf = rf.predict(X_test)

print("\nRandom Forest Accuracy:", accuracy_score(y_test, pred_rf))
print("\nRandom Forest Report:\n")
print(classification_report(y_test, pred_rf))

joblib.dump(rf, os.path.join(OUTPUT_DIR, "random_forest_model.joblib"))
pd.DataFrame({"labels": df["primary_cuisine"].unique()}).to_csv(
    os.path.join(OUTPUT_DIR, "cuisine_labels.csv"), index=False
)

print("\nTask 3 completed successfully!")
print("Outputs saved in:", OUTPUT_DIR)
