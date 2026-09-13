from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import numpy as np
from typing import List, Tuple

class TfIdfIntentClassifier:
    def __init__(self, max_features: int = 5000, random_seed: int = 42):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=max_features, ngram_range=(1, 2))),
            ('clf', LogisticRegression(class_weight='balanced', random_state=random_seed, max_iter=1000))
        ])
        
    def fit(self, X: List[str], y: List[str]):
        """Trains the TF-IDF + Logistic Regression model."""
        self.pipeline.fit(X, y)
        
    def predict(self, X: List[str]) -> List[str]:
        """Predicts the intent."""
        return self.pipeline.predict(X).tolist()
        
    def predict_proba(self, X: List[str]) -> np.ndarray:
        """Returns probability distribution over classes."""
        return self.pipeline.predict_proba(X)
        
    def predict_with_confidence(self, X: List[str]) -> List[Tuple[str, float]]:
        """Returns a list of (predicted_class, confidence_score) tuples."""
        probs = self.predict_proba(X)
        classes = self.pipeline.classes_
        
        results = []
        for prob in probs:
            max_idx = np.argmax(prob)
            results.append((classes[max_idx], float(prob[max_idx])))
        return results
