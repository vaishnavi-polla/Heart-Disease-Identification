

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)
df=pd.read_csv("dataset/heart.csv")
X = df.drop("Heart_Disease", axis=1)
y = df["Heart_Disease"]
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
#LOGISTIC
logistic_model = LogisticRegression(max_iter=1000)
logistic_model.fit(X_train, y_train)
logistic_pred = logistic_model.predict(X_test)
logistic_accuracy = accuracy_score(y_test,logistic_pred)
print("\nLogistic Regression")
print("Accuracy:", accuracy_score(y_test, logistic_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, logistic_pred))

print("Classification Report:")
print(classification_report(y_test, logistic_pred))
#Precision answers:Of all the patients the model predicted as positive, how many were actually positive?
#DECISION TREE
tree_model = DecisionTreeClassifier(random_state=42)
tree_model.fit(X_train,y_train)
tree_pred=tree_model.predict(X_test)
tree_accuracy=accuracy_score(y_test,tree_pred)
print("\nDecision Tree")
print("Accuracy:", accuracy_score(y_test, tree_pred))

print("Confusion Matrix:")
print(confusion_matrix(y_test, tree_pred))

print("Classification Report:")
print(classification_report(y_test, tree_pred))#RANDOM FOREST
forest_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
forest_model.fit(X_train, y_train)
forest_pred = forest_model.predict(X_test)
print("\n==============================")
print("Random Forest")
print("==============================")

print("Accuracy:", accuracy_score(y_test, forest_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, forest_pred))

print("\nClassification Report:")
print(classification_report(y_test, forest_pred))
'''Model	Accuracy
Logistic Regression	91.67% 🥇
Random Forest	88.33% 🥈
Decision Tree	78.33% 🥉'''
# =========================
# StandardScaler
# =========================

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Logistic Regression with scaled data
scaled_model = LogisticRegression(max_iter=1000)

scaled_model.fit(X_train_scaled, y_train)

scaled_pred = scaled_model.predict(X_test_scaled)

scaled_accuracy = accuracy_score(y_test, scaled_pred)

print("\nScaled Logistic Regression Accuracy:", scaled_accuracy)
# =========================
# KNN
# =========================

from sklearn.neighbors import KNeighborsClassifier

knn_model = KNeighborsClassifier(n_neighbors=5)

knn_model.fit(X_train_scaled, y_train)

knn_pred = knn_model.predict(X_test_scaled)

knn_accuracy = accuracy_score(y_test, knn_pred)

print("\nKNN Accuracy:", knn_accuracy)
# =========================
# KNN - Test different K values
# =========================

from sklearn.neighbors import KNeighborsClassifier

for k in [3, 5, 7, 9, 11]:
    
    knn_model = KNeighborsClassifier(n_neighbors=k)
    
    knn_model.fit(X_train_scaled, y_train)
    
    knn_pred = knn_model.predict(X_test_scaled)
    
    knn_accuracy = accuracy_score(y_test, knn_pred)
    
    print("K =", k, "Accuracy =", knn_accuracy)



    from sklearn.metrics import precision_score, recall_score, f1_score
    print("\n===== MODEL COMPARISON =====")

print("\nLogistic Regression")
print("Accuracy:", accuracy_score(y_test, logistic_pred))
print("Precision:", precision_score(y_test, logistic_pred))
print("Recall:", recall_score(y_test, logistic_pred))
print("F1 Score:", f1_score(y_test, logistic_pred))


print("\nDecision Tree")
print("Accuracy:", accuracy_score(y_test, tree_pred))
print("Precision:", precision_score(y_test, tree_pred))
print("Recall:", recall_score(y_test, tree_pred))
print("F1 Score:", f1_score(y_test, tree_pred))


print("\nRandom Forest")
print("Accuracy:", accuracy_score(y_test, forest_pred))
print("Precision:", precision_score(y_test, forest_pred))
print("Recall:", recall_score(y_test, forest_pred))
print("F1 Score:", f1_score(y_test, forest_pred))


print("\nKNN")
print("Accuracy:", accuracy_score(y_test, knn_pred))
print("Precision:", precision_score(y_test, knn_pred))
print("Recall:", recall_score(y_test, knn_pred))
print("F1 Score:", f1_score(y_test, knn_pred))
'''Logistic Regression 🥇
91.67%
100%
82.14%
90.20%'''
# =========================
# Day 16 - Feature Importance
# =========================

feature_names = X.columns


# -------------------------
# Logistic Regression
# -------------------------

scaled_logistic_model = LogisticRegression(max_iter=1000)

scaled_logistic_model.fit(
    X_train_scaled,
    y_train
)

coefficients = pd.Series(
    scaled_logistic_model.coef_[0],
    index=feature_names
)

print("\nLogistic Regression Coefficients:")
print(coefficients.sort_values(ascending=False))


# -------------------------
# Decision Tree
# -------------------------

tree_importance = pd.Series(
    tree_model.feature_importances_,
    index=feature_names
)

print("\nDecision Tree Feature Importance:")
print(tree_importance.sort_values(ascending=False))


# -------------------------
# Random Forest
# -------------------------

forest_importance = pd.Series(
    forest_model.feature_importances_,
    index=feature_names
)

print("\nRandom Forest Feature Importance:")
print(forest_importance.sort_values(ascending=False))

