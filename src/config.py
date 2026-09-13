import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
GOLDEN_DATA_DIR = DATA_DIR / "golden"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"

# Domain Configuration
SELECTED_BRAND = "AppleSupport"
RANDOM_SEED = 42

# Data Processing Config
GOLDEN_SIZE = 200

# Retrieval Config
TOP_K = 5
MIN_RETRIEVAL_SIMILARITY = 0.35

# Classification Config
MIN_CLASSIFIER_CONFIDENCE = 0.60

# Model Config
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_raw_dataset_path(preferred_path: str | Path | None = None) -> Path:
    """
    Resolves the raw TWCS dataset path dynamically.
    Prefers preferred_path if given.
    Otherwise checks for twcs_sample.csv and twcs.csv.
    """
    if preferred_path:
        return Path(preferred_path)
    sample_path = RAW_DATA_DIR / "twcs_sample.csv"
    full_path = RAW_DATA_DIR / "twcs.csv"
    if sample_path.exists() and not full_path.exists():
        return sample_path
    if full_path.exists():
        return full_path
    return sample_path
