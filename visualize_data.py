import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("dataset/heart.csv")

plt.figure(figsize=(6, 4))

pd.crosstab(df["Gender"], df["Heart_Disease"]).plot(
    kind="bar",
    figsize=(6, 4)
)

plt.title("Heart Disease by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Patients")
plt.xticks([0, 1], ["Female", "Male"], rotation=0)
plt.show()
plt.figure(figsize=(6, 4))

plt.figure(figsize=(7, 4))

pd.crosstab(df["CP"], df["Heart_Disease"]).plot(
    kind="bar",
    
    figsize=(7, 4)
)

plt.title("Heart Disease by Chest Pain Type")
plt.xlabel("Chest Pain Type")
plt.ylabel("Number of Patients")

plt.show()
plt.figure(figsize=(7, 4))

plt.hist(df["Cholesterol"], bins=15)

plt.title("Cholesterol Distribution")
plt.xlabel("Cholesterol")
plt.ylabel("Number of Patients")

plt.show()
plt.figure(figsize=(7, 4))

plt.hist(df["Max_HR"], bins=15)

plt.title("Maximum Heart Rate Distribution")
plt.xlabel("Maximum Heart Rate")
plt.ylabel("Number of Patients")

plt.show()
