# PPW — Web Search & Mining

A practical course project on **Information Retrieval / Web Search & Mining**.
This repository contains a web crawler for [detik.com](https://www.detik.com),
the resulting Indonesian news dataset (200 articles), and the Jupyter notebook
that loads, validates, and analyzes it.

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
   mining — the notebook already ships with the libraries for it.

All web scraping is done with **`trafilatura`** following polite-crawling
practices.

## Dataset

`data/crawling_detik.csv` / `data/crawling_detik.json` contain **200 Indonesian
news articles** crawled from detik.com:

| Label | Count | IDs |
|-------|-------|-----|
| `sport` | 100 | 1–100 |
| `finance` | 100 | 101–200 |

Each row has the following schema:

| Column | Description |
|--------|-------------|
| `id` | Sequential integer (1–200) |
| `isi_berita` | Main article text extracted with `trafilatura` |
| `label` | Category (`sport` or `finance`) |
| `url` | Source article URL |

## Project Structure

```
.
├── AGENTS.md              # Project instructions for AI agents / collaborators
├── book/                  # Jupyter Book source (published to GitHub Pages)
│   ├── CRISP-DM/          # CRISP-DM stage notebooks (kernel: enWebmining)
│   │   ├── Business.ipynb         # Task 1: goal, scope & crawling ethics
│   │   ├── EDA.ipynb              # Task 1: detik.com crawl, sport & finance
│   │   ├── Input.ipynb            # (empty — upcoming)
│   │   ├── Modeling.ipynb         # (empty — upcoming)
│   │   ├── Output.ipynb           # (empty — upcoming)
│   │   └── Production.ipynb       # (empty — upcoming)
│   ├── intro.md, CRISP-DM.md, _config.yml, _toc.yml
│   └── _build/            # (generated) build output
├── data/                  # Crawl results — 200 articles
│   ├── crawling_detik.csv
│   └── crawling_detik.json
├── lectures/              # Course lecture materials (.ppt + readable .md)
├── opencode.json          # Local OpenCode config (permissions, LSP, agents)
├── requirements.txt       # Pinned Python dependencies
└── scripts/
    └── run_crawl.py       # Standalone crawling script (re-crawl entry point)
```

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

> **Note:** The notebook must run with the `enWebmining` kernel. If it does not
> appear in the kernel list, re-run step 3.

## Usage

```bash
jupyter lab
```

Open `book/CRISP-DM/EDA.ipynb` and select kernel **`enWebmining`**.
The notebook is organized in sections:

- **Section A (reference)** — the original crawling code used once to produce
  the dataset. Not executed by default (avoids re-crawling).
- **Section B (main)** — loads `data/crawling_detik.csv` / `.json`, validates the
  required columns and label distribution, and prints example articles.
- **Section C (optional)** — re-crawl all 200 articles from scratch when
  `_re_crawl = True`.

The dataset is already complete, so **Section B is all you need**. The other CRISP-DM
stage notebooks (`Input`, `Modeling`, `Output`, `Production`) are placeholders for
upcoming assignments.

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
