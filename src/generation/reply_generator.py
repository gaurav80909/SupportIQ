import json
import logging
import openai
from openai import OpenAI
from src.schemas import ReplyGenerationResult
from src.generation.prompts import REPLY_GENERATION_PROMPT
from src.config import OPENAI_MODEL

logger = logging.getLogger(__name__)

class LLMGenerationError(Exception):
    """Raised when reply generation encounters an unrecoverable API or schema error."""
    pass

class ReplyGenerator:
    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI()
        
    def generate(self, customer_message: str, predicted_intent: str, retrieved_examples: list[dict]) -> ReplyGenerationResult:
        evidence_text = ""
        valid_ids = []
        for ex in retrieved_examples:
            valid_ids.append(ex['tweet_id'])
            evidence_text += f"ID: {ex['tweet_id']}\nCustomer: {ex['customer_message']}\nBrand: {ex['brand_response']}\n---\n"
            
        if not evidence_text:
            evidence_text = "No relevant historical evidence found."
            
        prompt = REPLY_GENERATION_PROMPT.format(
            customer_message=customer_message,
            predicted_intent=predicted_intent,
            evidence=evidence_text
        )
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a factual RAG customer support assistant. Output valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            result_json = json.loads(response.choices[0].message.content)
            result = ReplyGenerationResult(**result_json)
            
            # Filter evidence_ids to only those actually retrieved
            result.evidence_ids = [eid for eid in result.evidence_ids if eid in valid_ids]
            return result
            
        except (openai.AuthenticationError, openai.RateLimitError, openai.APIConnectionError, openai.APIStatusError) as e:
            err_msg = str(e)
            if "insufficient_quota" in err_msg or "credit_balance_exhausted" in err_msg or isinstance(e, openai.RateLimitError):
                logger.error(f"OpenAI API Quota Exhausted during reply generation: {e}")
                raise LLMGenerationError(
                    "OpenAI API quota exhausted (RateLimitError: 429) during reply generation. "
                    "Account has no remaining credits at https://platform.openai.com/settings/organization/billing."
                ) from e
            elif isinstance(e, openai.AuthenticationError):
                logger.error(f"OpenAI Authentication Failed during reply generation: {e}")
                raise LLMGenerationError(
                    "OpenAI API authentication failed (401) during reply generation. Please check OPENAI_API_KEY in .env."
                ) from e
            else:
                logger.error(f"OpenAI API Error during reply generation: {e}")
                raise LLMGenerationError(f"Reply generation API call failed: {e}") from e

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON returned by generator: {e}")
            raise LLMGenerationError(f"Reply generator returned malformed JSON: {e}") from e

        except Exception as e:
            logger.error(f"Reply generation unexpected error: {e}")
            raise LLMGenerationError(f"Reply generation failed: {e}") from e
