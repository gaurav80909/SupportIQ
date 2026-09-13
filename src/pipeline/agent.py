import logging
from typing import Optional
from pathlib import Path

from src.schemas import AgentResponse
from src.intents.classifier_llm import LLMIntentClassifier
from src.retrieval.retriever import Retriever
from src.generation.reply_generator import ReplyGenerator
from src.escalation.policy import EscalationPolicy
from src.config import EMBEDDINGS_DIR, GOLDEN_DATA_DIR
from src.intents.taxonomy import get_intent_list

logger = logging.getLogger(__name__)

class SupportAgent:
    def __init__(
        self,
        brand: str = "AppleSupport",
        index_path: Optional[Path] = None,
        metadata_path: Optional[Path] = None,
        taxonomy_path: Optional[Path] = None
    ):
        clean_brand = brand.lstrip("@")
        self.brand = clean_brand
        
        if clean_brand.lower() == "amazonhelp":
            index_p = index_path or (EMBEDDINGS_DIR / "amazonhelp" / "index.faiss")
            meta_p = metadata_path or (EMBEDDINGS_DIR / "amazonhelp" / "metadata.pkl")
            tax_p = taxonomy_path or (GOLDEN_DATA_DIR / "amazonhelp_taxonomy.json")
        else:  # Default to AppleSupport
            index_p = index_path or (EMBEDDINGS_DIR / "index.faiss")
            meta_p = metadata_path or (EMBEDDINGS_DIR / "metadata.pkl")
            tax_p = taxonomy_path or (GOLDEN_DATA_DIR / "taxonomy.json")
            
        self.taxonomy = get_intent_list(tax_p)
        self.classifier = LLMIntentClassifier(taxonomy=self.taxonomy)
        self.retriever = Retriever(index_p, meta_p)
        self.generator = ReplyGenerator()
        self.policy = EscalationPolicy()
        
    def handle(self, message: str) -> AgentResponse:
        logger.info(f"Handling message: {message[:50]}...")
        
        # 1. Intent Classification
        prediction = self.classifier.predict(message)
        logger.info(f"Predicted intent: {prediction.intent} ({prediction.confidence})")
        
        # 2. Historical Retrieval
        retrieved_examples = self.retriever.retrieve(message)
        logger.info(f"Retrieved {len(retrieved_examples)} examples")
        
        # 3. RAG Reply Generation
        generation_result = self.generator.generate(
            customer_message=message,
            predicted_intent=prediction.intent,
            retrieved_examples=retrieved_examples
        )
        logger.info(f"Generated reply (Grounded: {generation_result.grounded})")
        
        # 4. Escalation Policy
        decision = self.policy.evaluate(
            predicted_intent=prediction.intent,
            confidence=prediction.confidence,
            retrieved_examples=retrieved_examples,
            grounded=generation_result.grounded
        )
        logger.info(f"Decision: {decision.decision} - {decision.reason}")
        
        return AgentResponse(
            intent=prediction.intent,
            confidence=prediction.confidence,
            reply=generation_result.reply,
            decision=decision.decision,
            reason=decision.reason,
            retrieved_examples=retrieved_examples
        )
