import pandas as pd
from sklearn.metrics import cohen_kappa_score
from scipy.stats import pearsonr
import logging

logger = logging.getLogger(__name__)

def calculate_agreement(df: pd.DataFrame):
    """
    Expects DataFrame with columns like:
    human_groundedness, judge_groundedness
    human_helpfulness, judge_helpfulness
    etc.
    """
    metrics = ['groundedness', 'helpfulness', 'correctness', 'brand_tone', 'safety']
    results = {}
    
    for m in metrics:
        h_col = f'human_{m}'
        j_col = f'judge_{m}'
        
        if h_col not in df.columns or j_col not in df.columns:
            logger.warning(f"Missing columns for {m} agreement.")
            continue
            
        # Drop NaNs
        valid = df.dropna(subset=[h_col, j_col])
        if len(valid) == 0:
            continue
            
        exact = (valid[h_col] == valid[j_col]).mean()
        kappa = cohen_kappa_score(valid[h_col], valid[j_col])
        
        # Pearson needs variance
        try:
            pearson, _ = pearsonr(valid[h_col], valid[j_col])
        except Exception:
            pearson = float('nan')
            
        results[m] = {
            "exact_agreement": exact,
            "cohens_kappa": kappa,
            "pearson": pearson
        }
        
    return results
