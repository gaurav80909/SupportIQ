import sys
import argparse
import logging
from pathlib import Path
import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import RAW_DATA_DIR, RANDOM_SEED

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def create_sample(
    input_path: Path,
    output_path: Path,
    sample_size: int = 100000,
    seed: int = RANDOM_SEED,
    uniform: bool = False
) -> pd.DataFrame:
    """
    Creates a deterministic subsample from the raw TWCS dataset.
    
    By default, preserves complete customer-support conversation turn pairs
    so downstream conversation extraction and RAG retrieval function properly.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input raw dataset not found at: {input_path}")
    
    logger.info(f"Loading raw dataset from {input_path}...")
    # Load raw TWCS CSV
    df = pd.read_csv(input_path, low_memory=False)
    total_rows = len(df)
    logger.info(f"Loaded {total_rows:,} rows from {input_path}")
    
    if total_rows <= sample_size:
        logger.info(f"Dataset has {total_rows:,} rows, which is <= requested sample size ({sample_size:,}). Saving copy.")
        sample_df = df.copy()
    elif uniform:
        logger.info(f"Sampling {sample_size:,} rows uniformly at random (seed={seed})...")
        sample_df = df.sample(n=sample_size, random_state=seed).sort_index()
    else:
        logger.info(f"Sampling conversation-paired rows to reach target size {sample_size:,} (seed={seed})...")
        # Find outbound support turns with valid parent customer tweets
        outbound = df[df['inbound'] == False].dropna(subset=['in_response_to_tweet_id'])
        
        # Target roughly half outbound and half parent inbound turns
        target_pairs = sample_size // 2
        sampled_outbound = outbound.sample(n=min(target_pairs, len(outbound)), random_state=seed)
        
        # Fetch parent customer tweets
        parent_ids = set(sampled_outbound['in_response_to_tweet_id'].astype(sampled_outbound['in_response_to_tweet_id'].dtype))
        sampled_inbound = df[df['tweet_id'].isin(parent_ids)]
        
        paired = pd.concat([sampled_outbound, sampled_inbound]).drop_duplicates(subset=['tweet_id'])
        
        if len(paired) < sample_size:
            # Fill remainder with additional deterministic samples
            needed = sample_size - len(paired)
            remaining_pool = df[~df['tweet_id'].isin(set(paired['tweet_id']))]
            filler = remaining_pool.sample(n=min(needed, len(remaining_pool)), random_state=seed)
            sample_df = pd.concat([paired, filler]).drop_duplicates(subset=['tweet_id'])
        elif len(paired) > sample_size:
            sample_df = paired.sample(n=sample_size, random_state=seed)
        else:
            sample_df = paired
            
        sample_df = sample_df.sort_values(by='tweet_id')

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sample_df.to_csv(output_path, index=False)
    logger.info(f"Saved deterministic sample of {len(sample_df):,} rows to {output_path}")
    return sample_df

def main():
    parser = argparse.ArgumentParser(description="Create a deterministic, reviewer-friendly subsample from TWCS dataset.")
    parser.add_argument("--input", type=str, default=str(RAW_DATA_DIR / "twcs.csv"), help="Path to full raw TWCS CSV")
    parser.add_argument("--output", type=str, default=str(RAW_DATA_DIR / "twcs_sample.csv"), help="Output path for sampled CSV")
    parser.add_argument("--sample-size", type=int, default=100000, help="Number of rows to sample (default: 100,000)")
    parser.add_argument("--seed", type=int, default=RANDOM_SEED, help="Random seed for reproducibility (default: 42)")
    parser.add_argument("--uniform", action="store_true", help="Perform uniform row sampling instead of conversation-paired sampling")
    args = parser.parse_args()

    create_sample(
        input_path=Path(args.input),
        output_path=Path(args.output),
        sample_size=args.sample_size,
        seed=args.seed,
        uniform=args.uniform
    )

if __name__ == "__main__":
    main()
