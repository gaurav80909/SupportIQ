import argparse
import pandas as pd
import logging
from pathlib import Path

from src.pipeline.agent import SupportAgent
from src.intents.classifier_baseline import MajorityBaselineClassifier
from src.intents.classifier_tfidf import TfIdfIntentClassifier
from src.evaluation.metrics import calculate_intent_metrics, calculate_escalation_metrics, save_confusion_matrix
from src.evaluation.llm_judge import LLMJudge
from src.config import GOLDEN_DATA_DIR, PROCESSED_DATA_DIR
from src.intents.taxonomy import get_intent_list

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--golden", type=str, default=str(GOLDEN_DATA_DIR / "golden_set.csv"))
    parser.add_argument("--run-tfidf", action="store_true", help="Train and eval TF-IDF baseline")
    args = parser.parse_args()

    golden_path = Path(args.golden)
    if not golden_path.exists():
        logger.error(f"Golden set not found at {golden_path}. Please create and label it.")
        return

    df = pd.read_csv(golden_path)
    
    if 'intent' not in df.columns or df['intent'].isnull().all() or (df['intent'] == "").all():
        logger.error("Golden set 'intent' column is empty. Manual labeling is required before evaluation.")
        return
        
    df = df.dropna(subset=['intent']).copy()
    taxonomy = get_intent_list()
    
    logger.info(f"Evaluating on {len(df)} golden examples.")
    
    y_true_intent = df['intent'].tolist()
    
    # Baselines
    if args.run_tfidf:
        logger.info("Running TF-IDF and Majority Baselines...")
        # Load non-golden data for training
        train_path = PROCESSED_DATA_DIR / f"AppleSupport_conversations.csv" # Simplified
        if train_path.exists():
            train_df = pd.read_csv(train_path)
            train_df = train_df[~train_df['tweet_id'].isin(df['tweet_id'])].dropna(subset=['customer_message'])
            # We don't have true intents for the rest of the dataset, so TF-IDF can't really be trained on unlabelled data without active learning/weak supervision.
            # In a real scenario, we would partition the labelled data into train/test. 
            # For this assignment, we will skip training TF-IDF if there is no train set with labels.
            logger.warning("TF-IDF training requires labelled training data. Since only the golden set is labelled, we cannot do a clean train/test split without reducing golden size.")
            
    # Full Agent Evaluation
    agent = SupportAgent()
    judge = LLMJudge()
    
    y_pred_intent = []
    y_pred_esc = []
    y_true_esc = [] # We need expected_action labels too
    
    failures = []
    
    logger.info("Running Full Agent Pipeline on Golden Set...")
    for idx, row in df.iterrows():
        msg = row['customer_message']
        res = agent.handle(msg)
        
        y_pred_intent.append(res.intent)
        y_pred_esc.append(res.decision)
        
        expected_esc = row.get('expected_action', 'AUTO_HANDLE')
        y_true_esc.append(expected_esc)
        
        if res.intent != row['intent']:
            failures.append({
                'customer_message': msg,
                'gold_intent': row['intent'],
                'predicted_intent': res.intent,
                'confidence': res.confidence,
                'decision': res.decision
            })
            
    # Intent Metrics
    metrics = calculate_intent_metrics(y_true_intent, y_pred_intent, labels=taxonomy)
    logger.info(f"LLM Classifier Macro F1: {metrics['macro_f1']:.2f}")
    logger.info(f"LLM Classifier Accuracy: {metrics['accuracy']:.2f}")
    
    # Escalation Metrics
    esc_metrics = calculate_escalation_metrics(y_true_esc, y_pred_esc)
    logger.info(f"Escalation F1: {esc_metrics['f1']:.2f}")
    
    # Save Failures
    eval_dir = PROCESSED_DATA_DIR / "evaluation"
    eval_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(failures).to_csv(eval_dir / "failure_analysis.csv", index=False)
    
    save_confusion_matrix(y_true_intent, y_pred_intent, taxonomy, eval_dir / "confusion_matrix.png")
    logger.info("Evaluation complete. Results saved to data/processed/evaluation/")

if __name__ == "__main__":
    main()
