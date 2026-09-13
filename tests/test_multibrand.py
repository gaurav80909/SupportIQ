import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.pipeline.agent import SupportAgent
from src.intents.taxonomy import load_taxonomy, get_intent_list
from src.config import GOLDEN_DATA_DIR, EMBEDDINGS_DIR

def test_apple_taxonomy_loading():
    apple_tax = get_intent_list(GOLDEN_DATA_DIR / "taxonomy.json")
    assert len(apple_tax) == 11
    assert "software_update_os" in apple_tax
    assert "battery_power_performance" in apple_tax
    assert "delivery_delay_and_tracking" not in apple_tax

def test_amazon_taxonomy_loading():
    amazon_tax = get_intent_list(GOLDEN_DATA_DIR / "amazonhelp_taxonomy.json")
    assert len(amazon_tax) == 10
    assert "delivery_delay_and_tracking" in amazon_tax
    assert "prime_membership_and_benefits" in amazon_tax
    assert "returns_and_replacements" in amazon_tax
    assert "battery_power_performance" not in amazon_tax

@patch('src.pipeline.agent.LLMIntentClassifier')
@patch('src.pipeline.agent.Retriever')
@patch('src.pipeline.agent.ReplyGenerator')
def test_agent_brand_routing(MockGen, MockRet, MockClass):
    # Apple agent
    agent_apple = SupportAgent(brand="@AppleSupport")
    assert agent_apple.brand == "AppleSupport"
    assert "battery_power_performance" in agent_apple.taxonomy
    assert "delivery_delay_and_tracking" not in agent_apple.taxonomy

    # Amazon agent
    agent_amazon = SupportAgent(brand="@AmazonHelp")
    assert agent_amazon.brand == "AmazonHelp"
    assert "delivery_delay_and_tracking" in agent_amazon.taxonomy
    assert "battery_power_performance" not in agent_amazon.taxonomy
