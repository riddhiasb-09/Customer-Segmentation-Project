import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("Data/Mall_Customers.csv")
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df.duplicated().sum())

plt.figure(figsize=(8,5))
sns.histplot(df["Age"], bins=20)
plt.title("Age Distribution")
plt.show()

plt.figure(figsize=(6,4))
sns.countplot(x="Gender", data=df)
plt.title("Gender Distribution")
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df["Annual_Income_(k$)"], bins=20)
plt.title("Annual Income Distribution")
plt.show()

plt.figure(figsize=(8,5))
sns.histplot(df["Spending_Score"], bins=20)
plt.title("Spending Score Distribution")
plt.show()

plt.figure(figsize=(8,6))
sns.scatterplot(
    x="Annual_Income_(k$)",
    y="Spending_Score",
    data=df
)
plt.title("Income vs Spending Score")
plt.show()

X = df[["Annual_Income_(k$)", "Spending_Score"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
wcss = []

for i in range(1, 11):
    model = KMeans(n_clusters=i, random_state=42)
    model.fit(X_scaled)
    wcss.append(model.inertia_)

plt.figure(figsize=(8,5))
plt.plot(range(1,11), wcss, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.show()

kmeans = KMeans(n_clusters=5, random_state=42)
df["Cluster"] = kmeans.fit_predict(X_scaled)
plt.figure(figsize=(10,6))
sns.scatterplot(
    x="Annual_Income_(k$)",
    y="Spending_Score",
    hue="Cluster",
    palette="Set2",
    data=df,
    s=100
)
plt.title("Customer Segmentation")
plt.show()

cluster_summary = df.groupby("Cluster").mean(numeric_only=True)
print(cluster_summary)
df.to_csv("Customer_Segments.csv", index=False)