# SupportIQ

## Problem
This project implements the Hiver SDE Intern take-home assignment. The objective is to build an evaluation-first, production-quality AI customer support system capable of classifying incoming tweets, generating replies grounded in historical data (RAG), and safely escalating ambiguous or high-risk issues based on a hybrid policy. 


# SupportIQ — AI Customer Support Agent

> An AI-powered customer support agent that classifies customer issues, retrieves similar historical conversations, drafts grounded responses, and decides whether a request should be automatically handled or escalated.

## 🚀 Overview

SupportIQ is an AI customer-support system built for the Hiver SDE Intern Take-Home Assignment.

The system uses the **Customer Support on Twitter (TWCS)** dataset to build a brand-specific support agent. For the current implementation, **@AppleSupport** is the selected production/demo brand.

Given a new customer message, SupportIQ:

1. Classifies the customer's issue into a data-driven support intent.
2. Retrieves similar historical customer-support conversations.
3. Generates a response grounded in those historical examples.
4. Decides whether the request should be `AUTO_HANDLE` or `ESCALATE`.
5. Provides the reasoning behind the escalation decision.

The system is designed to be **reproducible, explainable, and evaluation-driven** rather than relying only on subjective LLM output.

---

## ✨ Key Features

### Intent Classification
Classifies incoming customer messages into **11 AppleSupport-specific intents** discovered from the dataset.

### Historical Conversation Retrieval
Uses semantic embeddings and **FAISS vector search** to retrieve relevant historical support conversations.

### Grounded Reply Generation
Generates a support reply using retrieved historical conversations as context.

### Escalation Decision
Routes each request to:

- `AUTO_HANDLE`
- `ESCALATE`

with an explicit reason for escalation.

### Interactive Demo
A Streamlit interface allows reviewers to enter a customer message and inspect the complete AI pipeline.

### Evaluation-First Design
A separate **200-example golden evaluation set** is maintained for measuring system performance.

---

## 🏗️ Architecture

```text
                    Customer Message
                           │
                           ▼
                ┌─────────────────────┐
                │ Intent Classification│
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Semantic Retrieval  │
                │      FAISS          │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Reply Generation    │
                │      LLM            │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Escalation Policy   │
                └──────────┬──────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
            AUTO_HANDLE           ESCALATE
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
Copy `.env.example` to `.env` and set `OPENAI_API_KEY`:
```bash
cp .env.example .env
```

---

## ⚡ Quick Reproduction Guide (< 15 Minutes)

> [!IMPORTANT]
> **The full 500 MB TWCS dataset is NOT required for reproduction.**
> Reviewers can reproduce the entire end-to-end pipeline (subsampling, conversation dataset generation, FAISS vector indexing, and the interactive SaaS UI) in **under 2 minutes** using the deterministic 100,000-row subsample workflow.

Run the following commands in sequence:

```bash
# 1. Create a deterministic 100,000-row subsample with linked conversation turn pairs (~15s)
python scripts/create_sample.py --sample-size 100000 --seed 42

# 2. Extract brand conversation turn pairs from the subsample (~1s)
# Note: --input automatically auto-resolves to data/raw/twcs_sample.csv if twcs.csv is absent
python scripts/build_dataset.py --input data/raw/twcs_sample.csv --brand AppleSupport

# 3. Build the FAISS vector retrieval index on the sample conversations (~25s)
python scripts/build_embeddings.py --input data/processed/AppleSupport_conversations.csv

# 4. Launch the professional SaaS dark-mode dashboard
streamlit run app.py
```

### Subsample CLI Options
- `scripts/create_sample.py`:
  - `--input`: Path to raw TWCS CSV (default: `data/raw/twcs.csv`)
  - `--output`: Destination path (default: `data/raw/twcs_sample.csv`)
  - `--sample-size`: Number of rows to sample (default: `100000`)
  - `--seed`: Random seed for strict reproducibility (default: `42`)
  - `--uniform`: Perform pure uniform row sampling instead of conversation-pair preserving sampling

- `scripts/build_dataset.py`:
  - `--input`: Path to raw or subsampled CSV (auto-resolves `twcs_sample.csv` or `twcs.csv`)
  - `--brand`: Brand handle to extract (e.g. `AppleSupport`, `AmazonHelp`)
  - `--output`: Destination path for processed conversations CSV

---

## Full-Scale Reproduction (Optional)
If you wish to process the complete 2.8-million-turn TWCS dataset:

```bash
# 1. Download full TWCS dataset (requires Kaggle API credentials)
python scripts/download_data.py

# 2. Build full conversation pairs for AppleSupport or AmazonHelp
python scripts/build_dataset.py --brand AppleSupport
python scripts/build_dataset.py --brand AmazonHelp --output data/processed/amazonhelp/AmazonHelp_conversations.csv

# 3. Build full FAISS retrieval indexes
python scripts/build_embeddings.py --input data/processed/AppleSupport_conversations.csv
python scripts/build_embeddings.py --input data/processed/amazonhelp/AmazonHelp_conversations.csv --output_dir data/embeddings/amazonhelp

# 4. Run automated unit tests
pytest -v
```

---

## Testing
Run the comprehensive unit test suite:
```bash
pytest -v
```
All 15 tests cover deterministic sampling, dynamic dataset path resolution, brand isolation, baseline classifiers, TF-IDF, FAISS retrievers, and escalation policies.

---

## Project Structure

```text
SupportIQ/
│
├── app.py                     # Interactive SaaS-style dark mode dashboard
├── README.md                  # Project overview and reproduction instructions
├── requirements.txt           # Python dependencies
├── .env.example               # Configuration and environment template
├── decision_log.md            # Architectural and design decision records
│
├── data/
│   ├── raw/                   # twcs.csv and twcs_sample.csv
│   ├── processed/             # Cleaned conversation turn pairs
│   ├── embeddings/            # FAISS vector indexes and metadata
│   └── golden/                # Intent taxonomies and golden evaluation set
│
├── src/
│   ├── config.py              # Central path and threshold configurations
│   ├── schemas.py             # Pydantic data models
│   ├── data/                  # Loader, cleaner, conversation builder, sampler
│   ├── intents/               # Intent classifiers and taxonomy loaders
│   ├── retrieval/             # SentenceTransformers embedder & FAISS index
│   ├── generation/            # RAG reply generator and prompts
│   ├── escalation/            # Hybrid deterministic escalation policy
│   ├── evaluation/            # Metrics, LLM judge, and human agreement
│   └── pipeline/              # Multi-brand SupportAgent pipeline
│
├── scripts/
│   ├── create_sample.py       # Deterministic subsample generator (<15 min reproduction)
│   ├── build_dataset.py       # Brand conversation extractor
│   ├── build_embeddings.py    # FAISS vector indexing
│   ├── create_golden_template.py # Golden evaluation set sampler
│   ├── annotate_golden.py     # Streamlit manual annotation tool
│   └── run_evaluation.py      # Automated benchmark runner
│
├── reports/
│   ├── intent_taxonomy.md     # AppleSupport 11-intent taxonomy analysis
│   └── amazonhelp_intent_taxonomy.md # AmazonHelp 10-intent taxonomy analysis
│
└── tests/                     # 21 automated pytest unit tests (including mock error handling)
```

---

## Sources & Attributions

SupportIQ utilizes standard industry frameworks and open-source models. All application logic, pipeline orchestration, prompt engineering, and UI components were developed natively for this project without copying external project code.

Official source attributions:
- **Twitter Customer Support (TWCS) Dataset**: Curated by ThoughtVector (Anurag Nagar) on Kaggle. Contains 2.8M customer support tweets and conversation turns from top enterprise brands.
  - *Source:* [Kaggle Dataset: Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)
- **Sentence Transformers (`all-MiniLM-L6-v2`)**: Developed by Nils Reimers and Iryna Gurevych (UKPLab / Hugging Face). Used for 384-dimensional dense semantic text embeddings.
  - *Source:* [Hugging Face Model Hub](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- **FAISS (Facebook AI Similarity Search)**: Developed by Meta AI Research (Johnson, Douze, Jégou, 2017). Used for high-efficiency vector similarity search and dense retrieval.
  - *Source:* [Meta Research / GitHub FAISS](https://github.com/facebookresearch/faiss)
- **OpenAI API (`gpt-4o-mini`)**: Developed by OpenAI. Used for structured JSON zero-shot intent classification and grounded RAG reply generation.
  - *Source:* [OpenAI Platform](https://platform.openai.com/docs/models)
- **Streamlit**: Open-source web application framework developed by Snowflake / Streamlit Inc. Used to power the interactive SaaS dashboard and golden-set annotation UI.
  - *Source:* [Streamlit](https://streamlit.io/)
