import pandas as pd
import logging

logger = logging.getLogger(__name__)

def sample_data(df: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    """Samples data deterministically."""
    logger.info(f"Sampling {n} rows using seed {seed}")
    if len(df) <= n:
        return df.copy()
    return df.sample(n=n, random_state=seed).copy()

def exclude_golden(df: pd.DataFrame, golden_ids: set) -> pd.DataFrame:
    """Excludes golden examples from a dataset."""
    filtered = df[~df['tweet_id'].isin(golden_ids)]
    logger.info(f"Excluded {len(df) - len(filtered)} golden rows.")
    return filtered.copy()
