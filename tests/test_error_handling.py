import json
import pytest
from unittest.mock import MagicMock
import openai
from src.intents.classifier_llm import LLMIntentClassifier, LLMClassifierError
from src.generation.reply_generator import ReplyGenerator, LLMGenerationError
from src.schemas import LLMIntentPrediction, ReplyGenerationResult


def test_classifier_raises_on_ratelimit():
    """Verify LLMIntentClassifier raises LLMClassifierError on RateLimitError (e.g. 429 quota exhausted)."""
    mock_client = MagicMock()
    # Simulate OpenAI RateLimitError
    mock_client.chat.completions.create.side_effect = openai.RateLimitError(
        message="You exceeded your current quota, please check your plan and billing details.",
        response=MagicMock(status_code=429),
        body={"error": {"message": "credit_balance_exhausted", "type": "insufficient_quota", "code": "insufficient_quota"}}
    )
    
    classifier = LLMIntentClassifier(client=mock_client, taxonomy=["battery_issue", "audio_issue"])
    
    with pytest.raises(LLMClassifierError) as exc_info:
        classifier.predict("My battery is dying fast")
    
    assert "quota exhausted" in str(exc_info.value).lower() or "429" in str(exc_info.value)


def test_classifier_raises_on_auth_error():
    """Verify LLMIntentClassifier raises LLMClassifierError on AuthenticationError (401)."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = openai.AuthenticationError(
        message="Incorrect API key provided.",
        response=MagicMock(status_code=401),
        body={"error": {"message": "Incorrect API key provided."}}
    )
    
    classifier = LLMIntentClassifier(client=mock_client, taxonomy=["battery_issue", "audio_issue"])
    
    with pytest.raises(LLMClassifierError) as exc_info:
        classifier.predict("My battery is dying fast")
    
    assert "authentication failed" in str(exc_info.value).lower() or "401" in str(exc_info.value)


def test_classifier_handles_out_of_taxonomy_without_other():
    """Verify that unknown/hallucinated model intents are marked as unclassified_<intent> and NEVER 'other'."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=json.dumps({
            "intent": "hallucinated_intent",
            "confidence": 0.95,
            "reason": "Customer is talking about flights."
        })))
    ]
    mock_client.chat.completions.create.return_value = mock_response
    
    taxonomy = ["battery_issue", "audio_issue", "hardware_damage"]
    classifier = LLMIntentClassifier(client=mock_client, taxonomy=taxonomy)
    
    prediction = classifier.predict("I need flight info")
    assert prediction.intent != "other"
    assert prediction.intent == "unclassified_hallucinated_intent"
    assert prediction.confidence == 0.0
    assert "outside the active 3-intent taxonomy" in prediction.reason


def test_classifier_valid_taxonomy_match():
    """Verify normal valid taxonomy matching."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=json.dumps({
            "intent": "battery_issue",
            "confidence": 0.92,
            "reason": "Customer mentions battery life draining."
        })))
    ]
    mock_client.chat.completions.create.return_value = mock_response
    
    taxonomy = ["battery_issue", "audio_issue"]
    classifier = LLMIntentClassifier(client=mock_client, taxonomy=taxonomy)
    
    prediction = classifier.predict("My battery dies in an hour")
    assert prediction.intent == "battery_issue"
    assert prediction.confidence == 0.92


def test_generator_raises_on_ratelimit():
    """Verify ReplyGenerator raises LLMGenerationError on RateLimitError."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = openai.RateLimitError(
        message="Rate limit reached or quota exhausted.",
        response=MagicMock(status_code=429),
        body={"error": {"message": "insufficient_quota", "code": "insufficient_quota"}}
    )
    
    generator = ReplyGenerator(client=mock_client)
    
    with pytest.raises(LLMGenerationError) as exc_info:
        generator.generate(
            customer_message="My iPhone is frozen",
            predicted_intent="battery_issue",
            retrieved_examples=[{"tweet_id": "101", "customer_message": "Frozen", "brand_response": "Force restart"}]
        )
    
    assert "quota exhausted" in str(exc_info.value).lower() or "429" in str(exc_info.value)


def test_generator_raises_on_invalid_json():
    """Verify ReplyGenerator raises LLMGenerationError when LLM returns invalid JSON."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Not a JSON string"))]
    mock_client.chat.completions.create.return_value = mock_response
    
    generator = ReplyGenerator(client=mock_client)
    
    with pytest.raises(LLMGenerationError) as exc_info:
        generator.generate(
            customer_message="Help",
            predicted_intent="battery_issue",
            retrieved_examples=[]
        )
    
    assert "malformed json" in str(exc_info.value).lower()
