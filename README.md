# SupportIQ

## Problem
This project implements the Hiver SDE Intern take-home assignment. The objective is to build an evaluation-first, production-quality AI customer support system capable of classifying incoming tweets, generating replies grounded in historical data (RAG), and safely escalating ambiguous or high-risk issues based on a hybrid policy. 

## What Good Means
For the selected brand (configured to `AppleSupport` by default), a "good" system must:
1. **Intent Accuracy:** Accurately classify issues into a concise, brand-specific taxonomy.
2. **Safe Escalation:** Recognize when it doesn't know the answer or when an issue is sensitive, safely falling back to human agents.
3. **Grounded Replies:** Never invent policies, fabricate order statuses, or hallucinate guarantees.
4. **Useful Evidence:** Use historical conversations to maintain brand tone and policy consistency.

## What We Chose Not To Build
- **No autonomous account changes:** The agent cannot issue refunds or modify state.
- **No fake data lookup:** We do not simulate API calls for order status. 
- **No unrestricted agent actions:** Tool calling is omitted in favor of safe RAG.
- **No fine-tuning:** Zero-shot/Few-shot RAG provides better safety and explainability than fine-tuning for this scope.

## Architecture

```text
Customer Tweet 
      │
      ▼
┌──────────────┐     ┌──────────────┐
│ Intent LLM   │────▶│ RAG Retriever│ (FAISS)
│ Classifier   │     └──────────────┘
└──────────────┘            │
      │                     ▼
      │              ┌──────────────┐
      └─────────────▶│ RAG Generator│
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Escalation  │
                     │    Policy    │
                     └──────────────┘
                            │
                  ┌─────────┴─────────┐
                  ▼                   ▼
            AUTO_HANDLE            ESCALATE
```

## Dataset
Uses the "Customer Support on Twitter" Kaggle dataset. 
- Brand selected: `AppleSupport` (Configurable).
- Cleansed to remove URLs, whitespace, and orphaned tweets.
- Thread conversations reconstructed sequentially.

## Intent Taxonomy
The taxonomy is discovered through data exploration (see `notebooks/exploration.ipynb`). It consists of 8-12 core classes representing the bulk of the brand's support volume. The exact mapping is stored in `data/golden/taxonomy.json`.

## Golden Set
200 samples are randomly extracted across various thread lengths and intent types, intentionally including edge cases. These are **manually labeled** to establish a ground truth. 
*CRITICAL:* Golden examples are strictly excluded from TF-IDF training and FAISS indexing to prevent data leakage.

## Models
1. **Majority Baseline:** Predicts the single most common class.
2. **TF-IDF + LR Baseline:** Fast, explainable baseline for intent classification using sparse text features.
3. **LLM Classifier:** GPT-4o-mini powered zero-shot classification constrained via Pydantic schemas.

## Retrieval
Uses `all-MiniLM-L6-v2` via SentenceTransformers to embed historical customer messages. FAISS is used for fast inner-product similarity search to retrieve the Top-K (default 5) historically similar conversations.

## Generation
Uses OpenAI to draft responses. The prompt strictly enforces grounding—the LLM must base its response purely on the retrieved Top-K evidence and is instructed to return `grounded: false` if evidence is insufficient.

## Escalation
A deterministic policy layer that triggers `ESCALATE` if:
- Classifier confidence is below a threshold.
- Intent is high-risk (e.g., security/fraud).
- Retrieval similarity is too low.
- LLM flags the generation as ungrounded.

## Evaluation
- **Intent Metrics:** Macro F1, Accuracy, Per-class metrics, and Confusion Matrix.
- **Escalation Metrics:** Precision, Recall, F1 for the ESCALATE class.
- **LLM Judge:** Evaluates generated replies on Groundedness, Helpfulness, Correctness, Brand Tone, and Safety.
- **Human Agreement:** Correlates LLM Judge scores with human labels using Pearson/Cohen's Kappa.

## What Is Misleading About My Headline Number?
Headline metrics (like "85% Accuracy") do not guarantee production performance because:
- **Small Golden Set:** 200 examples is a tiny statistical sample; high variance is expected.
- **Sampling Bias:** The golden set might over-represent short, easy tweets if not carefully stratified.
- **Judge Bias:** The LLM-as-judge may exhibit leniency bias, inflating "Helpfulness" scores artificially.
- **Dataset Drift:** Twitter data from 2017 does not perfectly reflect 2024 customer behavior. 
- **Retrieval Quality:** High similarity scores in FAISS do not always mean the *solution* is similar, just the *problem description*.

## Results
*Pending manual labeling and evaluation execution.*

- Accuracy: XX
- Macro F1: XX
- Escalation F1: XX
- LLM Judge Score: XX
- Human Agreement: XX

## Installation

```bash
pip install -r requirements.txt
```

## Environment
Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.

## Reproduction

```bash
# 1. Download data (requires kaggle CLI and credentials)
python scripts/download_data.py

# 2. Build dataset and filter brand
python scripts/build_dataset.py

# 3. Create golden template (requires manual labeling afterwards!)
python scripts/create_golden_template.py

# 4. Build FAISS embeddings
python scripts/build_embeddings.py

# 5. Run Evaluation pipeline
python scripts/run_evaluation.py
```

## Testing
```bash
pytest -q
```
