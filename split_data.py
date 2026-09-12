import pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv("dataset/heart.csv")

print("Dataset shape:", df.shape)
print(df.head())
X = df.drop("Heart_Disease", axis=1)
y = df["Heart_Disease"]
print("X shape:", X.shape)
print("y shape:", y.shape)

print("\nX columns:")
print(X.columns)

print("\ny values:")
print(y.value_counts())


X_train, X_test, y_train, y_test = train_test_split( 
 X,
 y,
 test_size=0.2,
 random_state=42,
 stratify=y # split the data while keeping the class distribution of y approximately the same in train and test.
)
print("\nAfter splitting:")

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)
print("y_train:", y_train.shape)
print("y_test :", y_test.shape)