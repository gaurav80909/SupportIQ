import numpy as np
from typing import List, Tuple

class MajorityBaselineClassifier:
    def __init__(self):
        self.majority_class = None
        self.classes_ = None

    def fit(self, X: List[str], y: List[str]):
        """Fits the classifier by finding the most frequent class."""
        unique_classes, counts = np.unique(y, return_counts=True)
        self.classes_ = unique_classes
        self.majority_class = unique_classes[np.argmax(counts)]

    def predict(self, X: List[str]) -> List[str]:
        """Always predicts the majority class."""
        if self.majority_class is None:
            raise ValueError("Classifier not fitted yet.")
        return [self.majority_class] * len(X)

    def predict_proba(self, X: List[str]) -> np.ndarray:
        """Returns 1.0 for majority class, 0.0 for others."""
        if self.classes_ is None:
            raise ValueError("Classifier not fitted yet.")
        probs = np.zeros((len(X), len(self.classes_)))
        majority_idx = np.where(self.classes_ == self.majority_class)[0][0]
        probs[:, majority_idx] = 1.0
        return probs
