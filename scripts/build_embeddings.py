import sys
import argparse
import pandas as pd
import logging
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import PROCESSED_DATA_DIR, GOLDEN_DATA_DIR, EMBEDDINGS_DIR, SELECTED_BRAND
from src.retrieval.embedder import MessageEmbedder
from src.retrieval.index import FaissIndex

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=str(PROCESSED_DATA_DIR / f"{SELECTED_BRAND}_conversations.csv"))
    parser.add_argument("--output_dir", type=str, default=str(EMBEDDINGS_DIR), help="Output directory for index.faiss and metadata.pkl")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit on number of conversations to index")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    df = pd.read_csv(args.input)
    
    # Exclude Golden Set if golden set exists for this dataset
    golden_path = GOLDEN_DATA_DIR / "golden_set.csv"
    if golden_path.exists():
        golden_df = pd.read_csv(golden_path)
        excluded_ids = set(golden_df['tweet_id'])
        initial_len = len(df)
        df = df[~df['tweet_id'].isin(excluded_ids)]
        if len(df) < initial_len:
            logger.info(f"Excluded {initial_len - len(df)} golden examples from indexing.")

    if args.limit and len(df) > args.limit:
        logger.info(f"Limiting dataset to {args.limit} rows (out of {len(df)})")
        df = df.head(args.limit)

    embedder = MessageEmbedder()
    # Ensure customer_message column is string and drop NaNs
    df = df.dropna(subset=['customer_message', 'brand_response'])
    texts = df['customer_message'].astype(str).tolist()
    
    logger.info(f"Generating embeddings for {len(texts)} conversations...")
    embeddings = embedder.embed(texts)
    
    metadata = df[['tweet_id', 'conversation_id', 'customer_message', 'brand_response']].to_dict(orient='records')
    
    logger.info("Building FAISS index...")
    # Get dimension from the embeddings
    dim = embeddings.shape[1]
    faiss_index = FaissIndex(dimension=dim)
    faiss_index.add(embeddings, metadata)
    
    out_dir.mkdir(parents=True, exist_ok=True)
    faiss_index.save(out_dir / "index.faiss", out_dir / "metadata.pkl")
    logger.info(f"Embeddings and index saved successfully to {out_dir}.")

if __name__ == "__main__":
    main()
