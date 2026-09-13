# Decision Log

1. **One-Brand Scope (`AppleSupport`)**
   - **Decision:** Restrict the initial pipeline to a single brand.
   - **Why:** The full Kaggle dataset contains millions of tweets across many brands with highly varied response styles and intent structures. Focusing on one high-volume brand ensures retrieval and intent clustering represent a cohesive domain, rather than a generic mess.
   - **Trade-off:** We limit the generalized out-of-the-box utility for other brands, requiring reconfiguration and retraining to adapt to a new brand.

2. **Taxonomy Size (8-12 Intents)**
   - **Decision:** Target a relatively small, flat taxonomy of 8 to 12 intents.
   - **Why:** Deep hierarchical taxonomies or massive 100+ intent sets are extremely difficult for human annotators to label consistently (low human agreement) and hard for classifiers to confidently predict without massive datasets. A small taxonomy covers the "80/20" of customer service issues effectively.
   - **Trade-off:** We lose granular intent resolution (e.g., distinguishing between "password reset" and "2FA failure" if both fall under "account_access").

3. **TF-IDF + Logistic Regression Baseline**
   - **Decision:** Use TF-IDF with Logistic Regression instead of a neural baseline (like fine-tuned BERT) as the primary ML baseline.
   - **Why:** It trains in seconds, handles high-dimensional sparse text data reasonably well, offers easy interpretability (coefficients map directly to words), and provides robust calibrated probabilities.
   - **Trade-off:** Cannot capture deep semantic meaning, synonyms, or complex phrasing context as effectively as transformer models.

4. **Macro F1 as Primary Classification Metric**
   - **Decision:** Use Macro F1 rather than plain Accuracy to evaluate the intent classifiers.
   - **Why:** Customer support datasets are notoriously imbalanced (e.g., thousands of "complaints" vs. a few "security_or_fraud" issues). Macro F1 ensures we measure performance across *all* classes equally, preventing the model from succeeding just by predicting the majority class.
   - **Trade-off:** A severe drop in a rare class heavily penalizes the overall score, even if that class only represents 1% of total traffic.

5. **Retrieval-Augmented Generation (RAG) vs. Fine-Tuning**
   - **Decision:** Use RAG for generating replies instead of fine-tuning a generative LLM on historical replies.
   - **Why:** RAG grounds the generation in specific, retrieveable historical precedents, allowing the LLM to refuse answering if no evidence is found (reducing hallucinations). It also requires zero model training and allows policies to be updated simply by modifying the retrieval database.
   - **Trade-off:** Higher latency per inference due to retrieval step and larger prompt sizes (context window consumption).

6. **Top-K Retrieval (`TOP_K = 5`)**
   - **Decision:** Retrieve exactly 5 historical examples per query.
   - **Why:** 5 examples provide enough variance to synthesize a robust reply and determine consensus in historical brand behavior, without overflowing the LLM context window or confusing it with too much noise.
   - **Trade-off:** Edge-case issues that are sparsely represented might not be captured if they don't immediately surface in the top 5.

7. **Strict Golden Set Separation**
   - **Decision:** The 200 manually labeled golden examples are explicitly excluded from the TF-IDF training set and the FAISS retrieval index.
   - **Why:** Prevents data leakage. If the LLM generates a response based on retrieving the exact golden example, or the classifier is evaluated on data it saw during training, the evaluation metrics would be artificially inflated and meaningless for production estimation.
   - **Trade-off:** We lose 200 high-quality examples that could otherwise improve model performance and retrieval accuracy.

8. **Hybrid Escalation Policy**
   - **Decision:** Combine deterministic rules (e.g., low confidence) with semantic rules (e.g., high-risk intents) to decide whether to escalate.
   - **Why:** Pure ML escalation is risky and unpredictable; pure rules-based escalation is rigid. A hybrid approach ensures hard boundaries (always escalate "legal") while catching uncertain cases (escalate if classifier confidence < 0.60).
   - **Trade-off:** Requires maintaining and tuning a set of thresholds and rules, adding complexity compared to a purely learned approach.

9. **Pydantic Validation for LLM Outputs**
   - **Decision:** Force all LLM outputs (classification, reply generation, evaluation) to be parsed and validated through Pydantic schemas.
   - **Why:** LLMs can generate malformed JSON or hallucinate fields. Pydantic provides a hard boundary layer to catch these failures, allowing the pipeline to degrade gracefully (e.g., fallback to escalation) rather than crashing with a KeyError.
   - **Trade-off:** Adds overhead and requires prompt engineering to enforce the schema format.

10. **Human Agreement Anchor for LLM-as-Judge**
    - **Decision:** Require a small 50-example human validation set to calculate Pearson/Cohen's Kappa against the LLM Judge.
    - **Why:** LLMs exhibit biases (e.g., preferring longer answers or specific tones). Without verifying that the LLM Judge correlates with human preferences, the automated evaluation metrics are untrustworthy.
    - **Trade-off:** Introduces a manual bottleneck into the evaluation loop.

11. **Retrieval Similarity Thresholding (`MIN_RETRIEVAL_SIMILARITY = 0.35`)**
    - **Decision:** Ignore or penalize retrieved examples that fall below a similarity threshold.
    - **Why:** If a customer asks a completely novel question, FAISS will still return the "nearest" neighbors, even if they are completely irrelevant. A threshold acts as a safety guard to trigger escalation when the query is out-of-distribution.
    - **Trade-off:** Selecting the right threshold requires tuning; too high causes unnecessary escalations, too low allows hallucinations based on bad evidence.

12. **No Autonomous Account Actions**
    - **Decision:** The agent can draft replies and retrieve knowledge, but is structurally isolated from executing account changes (e.g., issuing refunds).
    - **Why:** Security and safety priority. An SDE intern project scope cannot guarantee the safety requirements for autonomous read-write API access to user accounts.
    - **Trade-off:** Limits the "resolution rate" of the bot, as it can only provide information rather than fixing stateful issues.

13. **Reproducibility Seed (`RANDOM_SEED = 42`)**
    - **Decision:** Hardcode a random seed across sampling, TF-IDF training, and FAISS indexing.
    - **Why:** Scientific rigor. Evaluation metrics must be directly comparable across runs when tweaking prompts or classifier logic. Without a fixed seed, metric variance could be attributed to data shuffling rather than model improvement.
    - **Trade-off:** Risk of accidentally overfitting to the specific random split chosen by the seed.
