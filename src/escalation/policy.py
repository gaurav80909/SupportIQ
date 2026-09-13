from src.schemas import EscalationDecision
from src.config import MIN_CLASSIFIER_CONFIDENCE
import logging

logger = logging.getLogger(__name__)

class EscalationPolicy:
    def __init__(self):
        self.high_risk_intents = {"security_or_fraud", "payment_issue", "legal"}
        
    def evaluate(self, 
                 predicted_intent: str, 
                 confidence: float, 
                 retrieved_examples: list[dict], 
                 grounded: bool) -> EscalationDecision:
        
        if confidence < MIN_CLASSIFIER_CONFIDENCE:
            return EscalationDecision(decision="ESCALATE", reason="Low classifier confidence.")
            
        if predicted_intent in self.high_risk_intents:
            return EscalationDecision(decision="ESCALATE", reason=f"High-risk intent: {predicted_intent}.")
            
        if not retrieved_examples:
            return EscalationDecision(decision="ESCALATE", reason="Insufficient retrieval similarity.")
            
        if not grounded:
            return EscalationDecision(decision="ESCALATE", reason="Ungrounded generated reply.")
            
        return EscalationDecision(decision="AUTO_HANDLE", reason="FAQ-style issue with strong historical evidence.")
