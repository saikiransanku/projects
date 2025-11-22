import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
DATA_PATH =DATA_PATH = r"C:\Users\Admin\Documents\cognoz\Dataset .csv"
  # change if needed
OUTPUT_DIR = "task1_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
target = "Aggregate rating"

numeric_features = [
    "Votes",
    "Price range",
    "Restaurant ID",
    "Country Code"
]

categorical_features = [
    "Has Online delivery",
    "Is delivering now",
    "Switch to order menu",
    "City"
]

df = df[df[target].notna()]

df[target] = pd.to_numeric(df[target], errors="coerce")
df = df[df[target].notna()]

X = df[numeric_features + categorical_features]
y = df[target]

for col in numeric_features:
    X.loc[:, col] = pd.to_numeric(X[col], errors='coerce')
    X.loc[:, col] = X[col].fillna(X[col].median())


# categorical
X.loc[:,categorical_features] = X[categorical_features].fillna("Unknown")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

numeric_transform = "passthrough"
categorical_transform = OneHotEncoder(handle_unknown="ignore", sparse_output=False)


preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transform, numeric_features),
        ("cat", categorical_transform, categorical_features)
    ]
)

# LINEAR REGRESSION MODEL
linear_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", LinearRegression())
])

print("Training Linear Regression...")
linear_model.fit(X_train, y_train)
pred_lr = linear_model.predict(X_test)

mse_lr = mean_squared_error(y_test, pred_lr)
r2_lr  = r2_score(y_test, pred_lr)
print("Linear Regression → MSE:", mse_lr, " R2:", r2_lr)

joblib.dump(linear_model, os.path.join(OUTPUT_DIR, "linear_model.joblib"))

# RANDOM FOREST MODEL
rf_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ))
])

print("Training Random Forest...")
rf_model.fit(X_train, y_train)
pred_rf = rf_model.predict(X_test)

mse_rf = mean_squared_error(y_test, pred_rf)
r2_rf  = r2_score(y_test, pred_rf)
print("Random Forest → MSE:", mse_rf, " R2:", r2_rf)

joblib.dump(rf_model, os.path.join(OUTPUT_DIR, "random_forest_model.joblib"))

results = pd.DataFrame({
    "Model": ["Linear Regression", "Random Forest"],
    "MSE": [mse_lr, mse_rf],
    "R2 Score": [r2_lr, r2_rf]
})

results.to_csv(os.path.join(OUTPUT_DIR, "regression_results.csv"), index=False)

print("All results saved in:", OUTPUT_DIR)
