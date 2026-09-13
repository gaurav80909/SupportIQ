import json
import logging
from openai import OpenAI
from src.schemas import ReplyGenerationResult
from src.generation.prompts import REPLY_GENERATION_PROMPT
from src.config import OPENAI_MODEL

logger = logging.getLogger(__name__)

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
            
        except Exception as e:
            logger.error(f"Reply generation failed: {e}")
            return ReplyGenerationResult(
                reply="I'm sorry, I cannot assist with this right now. Please wait for an agent.",
                grounded=False,
                evidence_ids=[]
            )
