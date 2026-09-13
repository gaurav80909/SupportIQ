import pytest
import numpy as np
from src.intents.classifier_baseline import MajorityBaselineClassifier
from src.intents.classifier_tfidf import TfIdfIntentClassifier

def test_majority_baseline():
    clf = MajorityBaselineClassifier()
    X_train = ["msg1", "msg2", "msg3", "msg4"]
    y_train = ["A", "B", "B", "A"]
    # Tie break goes to first in sorted array ('A')
    clf.fit(X_train, ["A", "A", "A", "B"]) 
    assert clf.predict(["test"]) == ["A"]
    
def test_tfidf_classifier():
    clf = TfIdfIntentClassifier()
    X_train = ["hello I need refund", "how to reset password"]
    y_train = ["payment", "account"]
    clf.fit(X_train, y_train)
    preds = clf.predict(["I want refund"])
    assert len(preds) == 1
    assert preds[0] in ["payment", "account"]
