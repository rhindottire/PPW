# PPW — Web Search & Mining

## Project Info
- Practical course: Information Retrieval / Web Search & Mining
- Python 3.14.7, virtual environment in `.venv/`
- Jupyter kernel: `enWebmining`

## Key Commands
- Activate venv: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run Jupyter: `jupyter lab`
- Re-crawl: `python run_crawl.py`

## Code Conventions
- All code must be Python, not TypeScript/JavaScript
- Use `trafilatura` for web content extraction (not requests+bs4 for main extraction)
- DataFrame output format: columns `id`, `isi_berita`, `label`, `url`
- Never crawl without delays (polite delay of at least 1 second)
- Data is already available in `crawling_detik.csv` — do not re-crawl unless asked
- Always use `with_metadata=True` or `include_comments=False` on trafilatura

## Project Structure
- `crawling_detik.ipynb` — main notebook (kernel: enWebmining)
- `run_crawl.py` — standalone crawling script
- `crawling_detik.csv/.json` — crawl results of 200 articles (100 sport + 100 finance)
- `requirements.txt` — pinned package list

## Main Libraries
- `trafilatura` — web text extraction
- `pandas` — data manipulation
- `scikit-learn` — TF-IDF, clustering
- `nltk` / `spacy` — NLP
- `Sastrawi` — Indonesian stemming
- `rank-bm25` — document ranking
- `wordcloud` — word frequency visualization
- `torch` — deep learning (CUDA-enabled)

## Course Rules
- Jupyter kernel must be `enWebmining` (not the default python3)
- Never delete existing crawl data without permission
- Use a polite User-Agent when crawling
- Include crawling ethics in every notebook

## Version Control Discipline
- Never commit or push immediately after making changes.
- After edits, show the user the diff/status and wait for an explicit instruction.
- Commit only when the user asks; push (public remote) only with separate confirmation.

## Project Help Files
- Read `AGENTS.md`, `README.md`, and other project help files
  to understand the task before working.
- Treat these files as authoritative context for how the project is interpreted.

## Available Agents
- Delegate work to the configured subagents instead of doing everything inline:
  - `code-reviewer` — review code for bugs, quality, and convention compliance
  - `docs-writer` — write and fix documentation, README, and code comments
  - `research-analyst` — deep analysis of data, papers, or literature
  - `research-gap-analyst` — identify gaps in research or literature
  - `research-planner` — structure research: questions, methodology, steps
  - `security-auditor` — audit code security (injection, secrets, auth)
  - `python-helper` — debug, review, and write Python code for this project
- Use subagents for heavy or parallelizable work to keep the main context clean.

## Language
- Interact with the user in Indonesian unless asked otherwise.
- Source code, comments, docstrings, commit messages, and documentation are in English.