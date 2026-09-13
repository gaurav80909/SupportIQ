import json
import logging
from pathlib import Path
from src.config import GOLDEN_DATA_DIR

logger = logging.getLogger(__name__)

TAXONOMY_PATH = GOLDEN_DATA_DIR / "taxonomy.json"

def load_taxonomy(path: Path | str | None = None) -> dict:
    tax_path = Path(path) if path else TAXONOMY_PATH
    if not tax_path.exists():
        logger.warning(f"Taxonomy file not found at {tax_path}. Using fallback.")
        return {
            "intents": [
                "account_access",
                "technical_issue",
                "payment_issue",
                "subscription_billing",
                "product_information",
                "complaint",
                "security_or_fraud",
                "other"
            ]
        }
    with open(tax_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_intent_list(path: Path | str | None = None) -> list[str]:
    data = load_taxonomy(path)
    intents = data.get("intents", [])
    if intents and isinstance(intents[0], dict):
        return [i["intent"] for i in intents]
    return intents
