import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def load_data(file_path: Path, chunksize: int = 100000) -> pd.DataFrame:
    """Loads CSV efficiently using chunks."""
    logger.info(f"Loading data from {file_path}")
    chunks = []
    try:
        for chunk in pd.read_csv(file_path, chunksize=chunksize):
            chunks.append(chunk)
        return pd.concat(chunks, ignore_index=True)
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        raise

def filter_brand(df: pd.DataFrame, brand_handle: str) -> pd.DataFrame:
    """Filters dataset for a specific brand."""
    # Assuming standard kaggle columns: tweet_id, author_id, inbound, created_at, text, response_tweet_id, in_response_to_tweet_id
    available_brands = df[df['inbound'] == False]['author_id'].value_counts()
    
    if brand_handle not in available_brands:
        logger.error(f"Brand {brand_handle} not found. Available top brands:\n{available_brands.head(10)}")
        raise ValueError(f"Brand '{brand_handle}' does not exist in dataset.")
        
    logger.info(f"Filtered to brand {brand_handle} with {available_brands[brand_handle]} tweets.")
    
    # We want tweets either from the brand, or sent TO the brand.
    brand_tweets = df[df['author_id'] == brand_handle]
    
    # We also need inbound tweets that the brand responded to.
    # A simple way to get a slice is to grab tweets from brand, and tweets that are parents of brand tweets.
    parent_ids = brand_tweets['in_response_to_tweet_id'].dropna().unique()
    inbound_tweets = df[df['tweet_id'].isin(parent_ids)]
    
    combined = pd.concat([brand_tweets, inbound_tweets]).drop_duplicates(subset=['tweet_id'])
    return combined
