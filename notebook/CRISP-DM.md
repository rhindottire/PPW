# CRISP-DM

The course work in this book follows the **CRISP-DM** process model, the standard
data-mining methodology. Each stage is documented as a notebook under
`CRISP-DM/`:

| File | Stage | Current status |
|------|-------|----------------|
| `Business.ipynb` | Frame the goal and constraints of the task, including crawling ethics. | **Completed** — full plan for the assignment series as the starting state: problem, objectives, stakeholders, success criteria, and ethics; no results recorded here. |
| `EDA.ipynb` | Load the stored corpus, then describe, explore, visualize, and validate the dataset. | **Completed** — 200-article corpus described and validated with a text-noise and character-encoding census; decision table and preprocessing pipeline for Data Preparation recorded (no re-crawl). |
| `Input.ipynb` | Clean and transform the raw text into a mining-ready representation. | **Completed** — 200-article corpus cleaned with encoding, format-artifact, whitespace, number, and short-token rules; preserve-first language policy, protected-name slang normalization, POS annotation before stopword removal, and guarded Sastrawi stemming produce the TF-IDF dataset (200 x 5431) plus the stored PCA matrix (200 x 161, 95%). The integrated `tokens.json` (7 keys) also carries the sentence corpus for the skip-gram arm, so Modeling trains directly. |
| `Modeling.ipynb` | Apply mining methods (classification, clustering, ranking). | **Completed** — Naive Bayes comparison on 160 train / 40 test (stratified, before any fit): sparse TF-IDF with MultinomialNB, PCA-projected TF-IDF with GaussianNB, and skip-gram Word2Vec (mean pooling) with GaussianNB, each tuned by grid search (alpha, PCA threshold, eight embedding configurations). Held-out accuracy 1.0 / 1.0 / 0.975; the skip-gram route is persisted to `data/Web-Mining/models/` (`word2vec.model`, `gnb.joblib`, `labels.json`, `protected.json`) for deployment. |
| `Output.ipynb` | Assess model quality against the goal. | Empty — upcoming task. |
| `Production.ipynb` | Present and publish results in the Jupyter Book / GitHub Pages. | **Completed** — the winning skip-gram route is packaged into `deploy/serve.py` with the exact Data Preparation transform and stored artifacts; a parity run over the same 160/40 stratified split reproduces served accuracy 0.975 (39/40). The classifier is published as a public Gradio app (`Rhindottire/News-Classifier`) on a free Hugging Face ZeroGPU Space with Python 3.12, currently RUNNING at `rhindottire-news-classifier.hf.space`. |

Since Task 1 only required crawling and gathering data, the **Business**,
**EDA**, **Input**, **Modeling**, and **Production** stages are populated so
far; the remaining **Output** stage is a placeholder to be completed as the
course progresses.