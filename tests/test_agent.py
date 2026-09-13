import pytest
from unittest.mock import MagicMock, patch
from src.pipeline.agent import SupportAgent
from src.schemas import LLMIntentPrediction, ReplyGenerationResult
from pathlib import Path

@patch('src.pipeline.agent.LLMIntentClassifier')
@patch('src.pipeline.agent.Retriever')
@patch('src.pipeline.agent.ReplyGenerator')
def test_agent_handle(MockGenerator, MockRetriever, MockClassifier):
    # Mock implementations
    mock_classifier = MockClassifier.return_value
    mock_classifier.predict.return_value = LLMIntentPrediction(
        intent="account_access", confidence=0.85, reason="Mock reason"
    )
    
    mock_retriever = MockRetriever.return_value
    mock_retriever.retrieve.return_value = [{"tweet_id": "1", "similarity": 0.9, "customer_message": "...", "brand_response": "..."}]
    
    mock_generator = MockGenerator.return_value
    mock_generator.generate.return_value = ReplyGenerationResult(
        reply="Here is your mock response.", grounded=True, evidence_ids=["1"]
    )
    
    agent = SupportAgent(index_path=Path("dummy"), metadata_path=Path("dummy"))
    agent.classifier = mock_classifier
    agent.retriever = mock_retriever
    agent.generator = mock_generator
    
    response = agent.handle("I lost my password")
    
    assert response.intent == "account_access"
    assert response.decision == "AUTO_HANDLE"
    assert response.reply == "Here is your mock response."
