# PPW — Web Search & Mining

A practical course project on **Information Retrieval / Web Search & Mining**.
This repository contains a web crawler for [detik.com](https://www.detik.com),
the resulting Indonesian news dataset (200 articles), and a Jupyter Book that
documents the full web mining pipeline (crawling, preparation, modeling, and
deployment) following the CRISP-DM methodology.

All web scraping is done with **`trafilatura`** following polite-crawling
practices.

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Re-crawling (optional)](#re-crawling-optional)
- [Crawling Ethics](#crawling-ethics)
- [Code Conventions](#code-conventions)
- [License](#license)

## Overview

The goal of this course project is to practice the complete web search and
mining pipeline:

1. **Crawling** — collect news article URLs from the official detik.com sitemap
   and extract clean article text.
2. **Data cleaning** — build a structured tabular dataset with a defined schema.
3. **(Upcoming)** preprocessing, indexing (TF-IDF / BM25), clustering, and text
   mining — the required libraries are already pinned in `requirements.txt`.

The Jupyter Book is built from `notebook/` and published to GitHub Pages:
<https://rhindottire.github.io/PPW/>.

## Dataset

`data/crawling_detik.csv` / `data/crawling_detik.json` contain **200 Indonesian
news articles** crawled from detik.com: 100 `sport` (ids 1–100) and 100
`finance` (ids 101–200). Each row has the schema `id`, `isi_berita` (article
text extracted with `trafilatura`), `label` (`sport` / `finance`), and `url`.

## Project Structure

```
.
├── AGENTS.md              # Project instructions for AI agents / collaborators
├── notebook/              # Jupyter Book source (published to GitHub Pages)
├── data/                  # Crawl results — 200 articles (csv + json)
├── lectures/              # Course lecture materials (.ppt/.pptx + readable .md, assets in lecture-{N}-assets/)
├── scripts/               # Standalone crawling script
├── .github/workflows/     # CI that builds and deploys the book
├── requirements.txt       # Pinned Python dependencies
└── LICENSE
```

The book is organized into coursework notes (`note/`), coursework deliverables
(`book/`), and CRISP-DM stage notebooks (`CRISP-DM/`).

## Prerequisites

- Python **3.14.7**
- A virtual environment (see below)
- Jupyter kernel **`enWebmining`** (course requirement)

## Setup

```bash
# 1. Create and activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install pinned dependencies
pip install -r requirements.txt

# 3. Register the Jupyter kernel (course requirement)
python -m ipykernel install --user --name=enwebmining --display-name="enWebmining"

# 4. Launch JupyterLab
jupyter lab
```

> **Note:** The notebooks must run with the `enWebmining` kernel. If it does
> not appear in the kernel list, re-run step 3.

## Usage

1. Open the notebooks under `notebook/` (e.g. `notebook/CRISP-DM/EDA.ipynb` or
   `notebook/book/book-1.ipynb`) and select the kernel **`enWebmining`**.
2. The stored crawl results are loaded from `data/`; the notebooks validate the
   required columns, label balance, and data quality without re-crawling.

To build the book locally:

```bash
source .venv/bin/activate
jupyter-book build notebook/
```

## Re-crawling (optional)

Only run this if you explicitly want to re-collect the data (stable internet
required, ~200 requests over several minutes):

```bash
source .venv/bin/activate
python scripts/run_crawl.py
```

Data is already available in `data/crawling_detik.csv` — do **not** re-crawl unless
asked.

## Crawling Ethics

- detik.com allows crawling (`User-agent: * Allow: /`).
- Use the official **sitemap** (`sitemap.xml` / `sitemap_news.xml`) to discover
  URLs instead of scraping the site index.
- Always send a **polite User-Agent** and keep a **delay of at least 1 second**
  between requests.
- Content is used solely for educational purposes / this course assignment.

## Code Conventions

- **Python only** (no TypeScript / JavaScript).
- Use `trafilatura` for main web content extraction (not `requests` + `bs4`
  alone).
- DataFrame output format: columns `id`, `isi_berita`, `label`, `url`.
- Always use `with_metadata=True` or `include_comments=False` when calling
  `trafilatura.extract`.
- Never delete existing crawl data without permission.
- Jupyter kernel must be `enWebmining` (not the default `python3`).
- Include crawling ethics section in every notebook.

## License

[MIT](LICENSE) © 2026 rhindottire
