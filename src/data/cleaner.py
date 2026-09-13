import re
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Cleans tweet text by removing URLs, excess whitespace, etc."""
    if not isinstance(text, str):
        return ""
        
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove specific support handles @mention at the start or inline, but keeping user tags might be tricky.
    # For now, just normalize whitespace.
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Applies cleaning to the dataframe."""
    logger.info(f"Cleaning dataframe of size {len(df)}")
    
    df = df.drop_duplicates(subset=['tweet_id']).copy()
    
    # Apply text cleaning
    df['text_clean'] = df['text'].apply(clean_text)
    
    # Drop rows where text became empty
    df = df[df['text_clean'] != ""]
    
    logger.info(f"Cleaned dataframe size: {len(df)}")
    return df
