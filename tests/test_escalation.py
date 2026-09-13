import pytest
from src.escalation.policy import EscalationPolicy

def test_escalation_policy():
    policy = EscalationPolicy()
    
    # Low confidence
    dec = policy.evaluate("account_access", 0.4, [{}], True)
    assert dec.decision == "ESCALATE"
    
    # High risk
    dec = policy.evaluate("security_or_fraud", 0.9, [{}], True)
    assert dec.decision == "ESCALATE"
    
    # No retrieval
    dec = policy.evaluate("account_access", 0.9, [], True)
    assert dec.decision == "ESCALATE"
    
    # Ungrounded
    dec = policy.evaluate("account_access", 0.9, [{}], False)
    assert dec.decision == "ESCALATE"
    
    # Auto handle
    dec = policy.evaluate("account_access", 0.9, [{}], True)
    assert dec.decision == "AUTO_HANDLE"
