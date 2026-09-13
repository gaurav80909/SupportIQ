import sys
import argparse
import logging
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, SELECTED_BRAND
from src.data.loader import load_data, filter_brand
from src.data.cleaner import clean_dataframe
from src.data.conversation_builder import build_conversations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=str(RAW_DATA_DIR / "twcs.csv"))
    parser.add_argument("--brand", type=str, default=SELECTED_BRAND, help="Brand handle to extract")
    parser.add_argument("--output", type=str, default=None, help="Output destination path")
    args = parser.parse_args()

    brand = args.brand
    out_path = Path(args.output) if args.output else (PROCESSED_DATA_DIR / f"{brand}_conversations.csv")

    if not Path(args.input).exists():
        logger.error(f"Input file not found: {args.input}. Run download_data.py first.")
        return

    logger.info("Loading data...")
    df = load_data(Path(args.input))
    
    logger.info(f"Filtering for brand {brand}...")
    df_brand = filter_brand(df, brand)
    
    logger.info("Cleaning data...")
    df_clean = clean_dataframe(df_brand)
    
    logger.info(f"Building conversations for {brand}...")
    df_conv = build_conversations(df_clean, brand)
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_conv.to_csv(out_path, index=False)
    logger.info(f"Saved {len(df_conv)} conversations to {out_path}")

if __name__ == "__main__":
    main()
