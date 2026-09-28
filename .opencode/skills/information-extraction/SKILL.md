---
name: information-extraction
description: Information Extraction (IE) pipeline for Indonesian legal court documents. Use when working on resource/IE tasks — scraping, rule-based extraction, dataset/labelling, machine learning (POS, CRF), deep learning (bi-LSTM), or transformer (BERT) fine-tuning — including verification that provided code actually runs.
---

# Information Extraction Pipeline

The IE course deliverable list lives in `resource/IE/`. The pipeline flows:
scraping → rule-based extraction → dataset/labelling → ML (POS/CRF) →
DL (bi-LSTM) → Transformer (BERT). Each stage has its own folder with
source code the lecturer provided; the goal is proving it runs.

## Stage Order

1. **Scraping** (`GET-COURT/`) — fetch court decision URLs, metadata,
   and PDFs from the court website using trafilatura/requests.
2. **Rule-based** (`RULE-BASED/`) — hand-written patterns extract entity
   spans (nomor putusan, tanggal, pasal, hukuman) from plain text.
3. **Dataset / labelling** (`DATASET/`) — turn raw sentences + entity spans
   into IOB-labelled rows for model training.
4. **Machine learning** (`ML/ML1`, `ML/ML2`) — POS tagging (flair), CRF
   sequence labelling, and vector classifiers.
5. **Deep learning** (`DL/`) — bi-LSTM char/word/CBOW models (TensorFlow).
6. **Transformer** (`BERT/`) — BERT pretrain + fine-tune for NER,
   plus dataset conversion to HuggingFace format.

## Verification Workflow (lecturer task: "code runs")

1. Read the corresponding `resource/IE/NOTES/*-notes.md` first — it records
   bugs already found, so do not rediscover them blindly.
2. Classify each file as:
   - `runnable` — runs unchanged for the version of data present.
   - `run-true` — runs only after small, permission-approved patches (import
     typos, undefined names, data paths). Never patch lecturer code without
     asking the user.
   - `blocked-license` — cannot run in this environment (Google Drive /
     Kaggle data missing; TensorFlow has **no wheel for Python 3.14, so DL
     notebooks are verified by inspection only**).
3. Record every file in `resource/IE/NOTES/VERIFICATION-MATRIX.md` with
   evidence (traceback lines, path checks) and the local fix.
4. Use kernel `enWebmining` for notebooks; never change crawl data or
   lecturer source files without explicit permission.

## Known Bug Patterns (check these first)

- Import of a module that does not exist (e.g. `entityGenerator2`, the real
  file is `entityGenerator3`).
- Undefined variable from a typo (`nomor` vs `baris`).
- Module-level code that executes on import.
- Label misalignment: mapping the whole-document label list onto each
  sentence (`'tag': row['tag']`) instead of per-token labels; zip() then
  truncates silently.
- `'nan'` as a label value leaking into a real class (str() on a NaN tag) —
  often the "26th class" in BERT notebooks.
- DataFrame operations with wrong API for the installed pandas:
  `X.to_dict('Record')` → `'records'`; `fillna(method='ffill')` → deprecated,
  use `fillna(method=None)` + `ffill()`; `applymap` → `map` on DataFrame.
- `astype(int)` on float embeddings (CBOW vectors) that destroys them.
- Saving Keras models with a `.pth` extension (PyTorch-style naming).
- Old data files truncated at the Excel limit (~1,048,576 rows) — NER files
  may hold only ~108 documents instead of 200.
- Hardcoded Colab/Windows paths (`/content`, `C:\\`); Google Drive file IDs
  that cannot be accessed locally.

## Environment Facts

- Python **3.14.7** in `.venv`; kernel name `enWebmining`.
- Installed for IE: `python-crfsuite`, `sklearn-crfsuite`, `flair`,
  `gdown`, `gradio`, `rapidfuzz`, `PyPDF2`, `transformers` 4.x,
  `tokenizers`, `eli5` (see `requirements.txt` section `[11]`).
- **Not** installed: `gensim` (no cp314 wheel, source build fails),
  `tensorflow`/`tensorflow-addons` (no cp314 wheel).
- CRF/POS/rule-based files run locally; TF bi-LSTM is inspection-only.

## Data Principles

- Show data before/after every transformation; keep original data intact.
- Surface ambiguous tokens, names, and counts from notebook output at
  execution time — never prefill them in `note.md`/`book.md`.
- Preserve-first foreign/hilanguage handling; translate only when every
  occurrence shares one non-name meaning with a single Indonesian
  equivalent.

## Related Skills

- `data-quality` — text-noise taxonomy and strict EDA checklist.
- `data-preprocessing` — tokenization, stopword removal, and stemming for IR.
- `crawling` — polite crawl workflow (delays, ethics) for the scraping stage.