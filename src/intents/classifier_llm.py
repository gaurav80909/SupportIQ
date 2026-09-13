import logging
import json
import openai
from openai import OpenAI
from src.schemas import LLMIntentPrediction
from src.intents.taxonomy import get_intent_list
from src.config import OPENAI_MODEL

logger = logging.getLogger(__name__)

class LLMClassifierError(Exception):
    """Raised when the LLM classifier encounters an unrecoverable API or schema error."""
    pass

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
            
            # Validate against the active taxonomy
            tax_lookup = {t.lower().strip(): t for t in self.taxonomy}
            raw_intent = prediction.intent.strip()
            
            if raw_intent.lower() in tax_lookup:
                prediction.intent = tax_lookup[raw_intent.lower()]
            else:
                logger.warning(
                    f"LLM returned intent '{prediction.intent}' which is not in active taxonomy: {self.taxonomy}"
                )
                # Explicitly record unclassified intent; never fake 'other'
                prediction.reason = f"Intent '{prediction.intent}' is outside the active {len(self.taxonomy)}-intent taxonomy."
                prediction.intent = f"unclassified_{prediction.intent}"
                prediction.confidence = 0.0
                
            return prediction

        except (openai.AuthenticationError, openai.RateLimitError, openai.APIConnectionError, openai.APIStatusError) as e:
            err_msg = str(e)
            if "insufficient_quota" in err_msg or "credit_balance_exhausted" in err_msg or isinstance(e, openai.RateLimitError):
                logger.error(f"OpenAI API Quota Exhausted: {e}")
                raise LLMClassifierError(
                    "OpenAI API quota exhausted (RateLimitError: 429). The configured account has no remaining credits. "
                    "Please check billing or add credits at https://platform.openai.com/settings/organization/billing."
                ) from e
            elif isinstance(e, openai.AuthenticationError):
                logger.error(f"OpenAI API Authentication Failed: {e}")
                raise LLMClassifierError(
                    "OpenAI API authentication failed (401). Please verify that your OPENAI_API_KEY in .env is valid."
                ) from e
            else:
                logger.error(f"OpenAI API Status Error: {e}")
                raise LLMClassifierError(f"OpenAI API call failed: {e}") from e

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise LLMClassifierError(f"LLM returned invalid JSON output: {e}") from e

        except Exception as e:
            logger.error(f"LLM classification unexpected error: {e}")
            raise LLMClassifierError(f"Classification failed: {e}") from e
