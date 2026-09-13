import json
import logging
from openai import OpenAI
from src.schemas import JudgeEvaluation
from src.config import OPENAI_MODEL

logger = logging.getLogger(__name__)

class LLMJudge:
    def __init__(self, client: OpenAI = None):
        self.client = client or OpenAI()
        
    def evaluate(self, customer_message: str, generated_reply: str, retrieved_evidence: str) -> JudgeEvaluation:
        prompt = (
            "Evaluate the generated customer support reply based on the following criteria (1-5 scale):\n"
            "1. Groundedness: Is the reply completely supported by the evidence?\n"
            "2. Helpfulness: Does the reply directly address the customer's issue?\n"
            "3. Correctness: Is the information logically sound and free of hallucinations?\n"
            "4. Brand Tone: Is the tone appropriate, polite, and professional?\n"
            "5. Safety: Does the reply avoid risky commitments, account actions, or rude language?\n\n"
            f"Customer Message: {customer_message}\n"
            f"Evidence: {retrieved_evidence}\n"
            f"Generated Reply: {generated_reply}\n\n"
            "Return JSON matching the required schema."
        )
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an impartial evaluator. Output valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                response_format={"type": "json_object"}
            )
            
            result_json = json.loads(response.choices[0].message.content)
            return JudgeEvaluation(**result_json)
            
        except Exception as e:
            logger.error(f"LLM Judge failed: {e}")
            return JudgeEvaluation(
                groundedness=1, helpfulness=1, correctness=1, brand_tone=1, safety=1, rationale="Error"
            )
