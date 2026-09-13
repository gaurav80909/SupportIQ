import logging
import json
from openai import OpenAI
from src.schemas import LLMIntentPrediction
from src.intents.taxonomy import get_intent_list
from src.config import OPENAI_MODEL

logger = logging.getLogger(__name__)

class LLMIntentClassifier:
    def __init__(self, client: OpenAI = None, taxonomy: list[str] = None):
        self.client = client or OpenAI()
        self.taxonomy = taxonomy if taxonomy is not None else get_intent_list()
        
    def predict(self, text: str) -> LLMIntentPrediction:
        """Predicts intent using the LLM with structured output."""
        prompt = (
            f"Classify the following customer support message into one of these intents: {self.taxonomy}.\n\n"
            f"Message: {text}\n\n"
            "Respond in JSON format conforming to the expected schema."
        )
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a customer support intent classifier. Provide valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            result_json = json.loads(response.choices[0].message.content)
            prediction = LLMIntentPrediction(**result_json)
            
            if prediction.intent not in self.taxonomy:
                logger.warning(f"LLM hallucinated intent: {prediction.intent}. Falling back to 'other'.")
                prediction.intent = "other"
                prediction.confidence = 0.0
                
            return prediction
            
        except Exception as e:
            logger.error(f"LLM classification failed: {e}")
            # Safe fallback
            return LLMIntentPrediction(
                intent="other",
                confidence=0.0,
                reason="Error during classification or invalid schema."
            )
