import numpy as np
import pandas as pd

# -----------------------------------------
# 1. Sample Dataset: 5 Students, 5 Attributes
# -----------------------------------------
data = {
    "Student": ["S1", "S2", "S3", "S4", "S5"],
    "GPA": [9.2, 8.5, 7.0, 8.0, 6.5],                # 0-10 scale
    "Programming": [95, 80, 50, 70, 60],             # 1-100
    "Research": [9, 8, 5, 6, 4],                     # 1-10
    "Creativity": [7, 6, 8, 7, 9],                   # 1-10
    "Leadership": [6, 5, 7, 8, 9]                    # 1-10
}

df = pd.DataFrame(data)

# -----------------------------------------
# 2. Extract Features and Normalize
# -----------------------------------------
X = df.iloc[:, 1:].values  # Only numeric attributes

# Min-Max Normalization to [0,1]
X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))

# -----------------------------------------
# 3. SOFM Configuration
# -----------------------------------------
input_dim = X.shape[1]     # 5 attributes
output_neurons = 4         # 4 clusters (classes)
learning_rate = 0.5
epochs = 100

np.random.seed(42)

# Random weight initialization
weights = np.random.rand(output_neurons, input_dim)

# -----------------------------------------
# 4. Train SOFM
# -----------------------------------------
for epoch in range(epochs):
    for sample in X:
        distances = np.linalg.norm(weights - sample, axis=1)   # Euclidean distance
        bmu_index = np.argmin(distances)                        # Best Matching Unit
        weights[bmu_index] += learning_rate * (sample - weights[bmu_index])  # Update weights
    learning_rate *= 0.98  # Decay learning rate

# -----------------------------------------
# 5. Assign clusters to students
# -----------------------------------------
cluster_assignments = []

for sample in X:
    distances = np.linalg.norm(weights - sample, axis=1)
    bmu_index = np.argmin(distances)
    cluster_assignments.append(bmu_index)

df["Cluster"] = cluster_assignments

# -----------------------------------------
# 6. Show final cluster assignments
# -----------------------------------------
print("\nFinal Student Cluster Assignments:")
print(df)
