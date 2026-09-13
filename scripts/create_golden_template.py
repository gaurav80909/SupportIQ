import sys
import argparse
import pandas as pd
import logging
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import PROCESSED_DATA_DIR, GOLDEN_DATA_DIR, SELECTED_BRAND, GOLDEN_SIZE, RANDOM_SEED
from src.data.sampler import sample_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=str(PROCESSED_DATA_DIR / f"{SELECTED_BRAND}_conversations.csv"))
    parser.add_argument("--output", type=str, default=str(GOLDEN_DATA_DIR / "golden_set.csv"))
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        logger.error(f"Input not found: {in_path}. Run build_dataset.py first.")
        return

    df = pd.read_csv(in_path)
    
    logger.info(f"Sampling {GOLDEN_SIZE} for golden set...")
    golden_df = sample_data(df, GOLDEN_SIZE, RANDOM_SEED)
    
    # Add manual labeling and evaluation columns
    golden_df['intent'] = ""
    golden_df['expected_action'] = ""
    golden_df['generated_reply'] = ""
    golden_df['notes'] = ""
    
    # Reorder columns
    cols = ['tweet_id', 'conversation_id', 'customer_message', 'brand_response', 'generated_reply', 'intent', 'expected_action', 'notes']
    golden_df = golden_df[[c for c in cols if c in golden_df.columns]]
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    golden_df.to_csv(out_path, index=False)
    
    logger.info(f"Golden template created at {out_path}.")
    logger.info("ACTION REQUIRED: Please manually label the 'intent' and 'expected_action' columns.")

if __name__ == "__main__":
    main()
