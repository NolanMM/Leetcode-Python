"""
K Nearest Neighbors Algorithm - NolanM - 2024-05-14
"""
import numpy as np
from collections import Counter


def euclidean_distance(x1, x2):
    return np.sqrt(np.sum(x1 - x2)**2)


class KNN:
    def __init__(self, k=3):
        self.k = k

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, x):
        predicted_labels = [self._predict(x) for x in x]
        return np.array(predicted_labels)

    def _predict(self,x):
        # Compute distances between x and all examples in the training set
        distances = [euclidean_distance(x_train, x) for x_train in self.X_train]
        # Sort by distance and return indices of the first k neighbors
        k_indices = np.argsort(distances)[:self.k]
        # Extract the labels of the k nearest neighbor training samples
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        # Return the most common class label
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

