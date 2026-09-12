import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Load dataset
df = pd.read_csv("dataset/heart.csv")


# Separate features and target
X = df.drop("Heart_Disease", axis=1)
y = df["Heart_Disease"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create final pipeline
final_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])


# Train model
final_model.fit(X_train, y_train)


# Test model
final_pred = final_model.predict(X_test)

accuracy = accuracy_score(y_test, final_pred)

print("Final Model Accuracy:", accuracy)


# Save model
joblib.dump(final_model, "heart_model.pkl")

print("Model saved successfully!")