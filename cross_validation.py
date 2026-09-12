import pandas as pd

from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier


# Load dataset
df = pd.read_csv("dataset/heart.csv")

# Separate features and target
X = df.drop("Heart_Disease", axis=1)
y = df["Heart_Disease"]
# Logistic Regression
logistic_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

logistic_scores = cross_val_score(
    logistic_pipeline,
    X,
    y,
    cv=5,
    scoring="accuracy"
)

print("\nLogistic Regression CV:")
print(logistic_scores)
print("Mean:", logistic_scores.mean())


# Decision Tree
tree_scores = cross_val_score(
    DecisionTreeClassifier(random_state=42),
    X,
    y,
    cv=5,
    scoring="accuracy"
)

print("\nDecision Tree CV:")
print(tree_scores)
print("Mean:", tree_scores.mean())


# Random Forest
forest_scores = cross_val_score(
    RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),
    X,
    y,
    cv=5,
    scoring="accuracy"
)

print("\nRandom Forest CV:")
print(forest_scores)
print("Mean:", forest_scores.mean())


# KNN
knn_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", KNeighborsClassifier(n_neighbors=5))
])

knn_scores = cross_val_score(
    knn_pipeline,
    X,
    y,
    cv=5,
    scoring="accuracy"
)

print("\nKNN CV:")
print(knn_scores)
print("Mean:", knn_scores.mean())
'''Test-set accuracy: 91.67%
and
5-fold cross-validation mean accuracy: 79.50%'''  