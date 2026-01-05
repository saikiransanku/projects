import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
DATA_PATH = r"C:\\Users\\kiran\\Documents\\GitHub\\projects\\internship\\cognifyz_technologies\\Dataset .csv"
OUTPUT_DIR = "task2_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
df["Cuisines"] = df["Cuisines"].fillna("Unknown")
df["City"] = df["City"].fillna("Unknown")
df["Price range"] = df["Price range"].fillna(0)
df["Aggregate rating"] = df["Aggregate rating"].fillna(0)
df["profile_text"] = (
    df["Cuisines"].astype(str)
    + " | "
    + df["City"].astype(str)
    + " | price_"
    + df["Price range"].astype(str)
    + " | rating_"
    + df["Aggregate rating"].astype(str)
)

tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["profile_text"])
joblib.dump(tfidf, os.path.join(OUTPUT_DIR, "tfidf_vectorizer.joblib"))

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
joblib.dump(cosine_sim, os.path.join(OUTPUT_DIR, "cosine_sim_matrix.joblib"))

indices = pd.Series(df.index, index=df["Restaurant Name"]).drop_duplicates()
def get_recommendations(name, top_n=10):
    if name not in indices:
        print(f"Restaurant '{name}' not found! Returning top-rated instead.")
        return df.sort_values("Aggregate rating", ascending=False).head(top_n)

    idx = indices[name]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = scores[1: top_n + 1]

    restaurant_indices = [i[0] for i in scores]

    return df.iloc[restaurant_indices][[
        "Restaurant Name",
        "Cuisines",
        "City",
        "Aggregate rating"
    ]]
sample_name = df["Restaurant Name"].iloc[0]
print("\nSample input restaurant:", sample_name)

recommendations = get_recommendations(sample_name, top_n=5)
print("\nTop 5 Recommendations:\n", recommendations)

# Save metadata for later use
df.to_csv(os.path.join(OUTPUT_DIR, "restaurants_data.csv"), index=False)

print("\nRecommendation system built successfully!")
print("Outputs saved in:", OUTPUT_DIR)
