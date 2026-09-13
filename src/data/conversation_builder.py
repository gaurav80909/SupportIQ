import pandas as pd
import logging

logger = logging.getLogger(__name__)

def build_conversations(df: pd.DataFrame, brand_handle: str) -> pd.DataFrame:
    """
    Reconstructs conversation threads.
    Pairs a customer's inbound tweet with the brand's outbound response.
    """
    logger.info("Building conversations from replies...")
    
    # Brand responses
    brand_responses = df[df['author_id'] == brand_handle].copy()
    
    # Customer inbound messages
    customer_messages = df[df['author_id'] != brand_handle].copy()
    
    # Merge on brand_responses.in_response_to_tweet_id == customer_messages.tweet_id
    conversations = pd.merge(
        customer_messages,
        brand_responses,
        left_on='tweet_id',
        right_on='in_response_to_tweet_id',
        suffixes=('_customer', '_brand')
    )
    
    # Standardize output columns
    result = pd.DataFrame({
        'tweet_id': conversations['tweet_id_customer'], # the customer's tweet id
        'conversation_id': conversations['tweet_id_customer'], # use customer tweet as root
        'customer_message': conversations['text_clean_customer'],
        'brand_response': conversations['text_clean_brand']
    })
    
    # Remove any rows missing either message or response
    result = result.dropna(subset=['customer_message', 'brand_response'])
    
    logger.info(f"Reconstructed {len(result)} valid customer-brand turn pairs.")
    return result
