# PPW — Web Search & Mining

## Project Info
- Practical course: Web Search & Mining
- Python 3.14.7, virtual environment in `.venv/`
- Jupyter kernel: `enWebmining`

## Key Commands
- Activate venv: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run Jupyter: `jupyter lab`
- Re-crawl: `python scripts/run_crawl.py`

## Code Conventions
- All code must be Python, not TypeScript/JavaScript
- Use `trafilatura` for web content extraction (not requests+bs4 for main extraction)
- DataFrame output format: columns `id`, `isi_berita`, `label`, `url`
- Never crawl without delays (polite delay of at least 1 second)
- Data is already available in `data/crawling_detik.csv` — do not re-crawl unless asked
- Always use `with_metadata=True` or `include_comments=False` on trafilatura
- Give every `print` call or visualization its own notebook cell — one output per
  cell — so each cell's output is clear and never overlaps with other prints

## Project Structure
- `notebook/` — Jupyter Book build root (built and published to GitHub Pages).
  Structure follows the rhindottire/Data-Science pattern: methodology chapters
  plus a per-assignment coursework chapter, both coexisting. There are two kinds
  of Markdown page directly under `notebook/`:
  - **Summary/index** of a sibling folder's contents — only `CRISP-DM.md`
    summarizes the notebooks in `CRISP-DM/`.
  - **Role-specific pages** with their own content linked to a sibling folder —
    `note.md` and `book.md` are NOT summaries; each holds different content (see
    below).
  - `note/` + `note.md` — coursework notes. `note.md` holds the assignment
    instructions/overview for each task (headings `Note N`); `note/note-N.md`
    holds the personal notes or material summary learned from lectures and the
    PPT.
  - `book/` + `book.md` — coursework deliverables. `book.md` shows the direct
    result/outcome of each task (headings `Book N`); `book/book-N.ipynb` is the
    working process notebook that produces that result.
  - `CRISP-DM/` — CRISP-DM stage notebooks (kernel: enWebmining)
    - `Business.ipynb` — Task 1: goal, scope & crawling ethics (completed)
    - `EDA.ipynb` — Task 1: detik.com crawl & exploration (completed)
    - `Input.ipynb`, `Modeling.ipynb`, `Output.ipynb`, `Production.ipynb` —
      placeholders for upcoming tasks
  - `intro.md`, `CRISP-DM.md`, `_config.yml`, `_toc.yml` — book pages/config
- `data/crawling_detik.csv/.json` — crawl results of 200 articles (100 sport + 100 finance)
- `scripts/run_crawl.py` — standalone crawling script (re-crawl entry point)
- `lectures/` — course lecture/assignment materials (`.ppt` + readable `.md`)
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

## Lecture Instructions
- Course lecture/assignment instructions live in `lectures/` as editable
  Markdown (`.md`) files, each paired with the original source file (`.ppt`).
- **Before modifying code or writing any program**, AI agents MUST first read
  the relevant instruction file(s) in `lectures/` and treat them as
  authoritative for interpreting the assignment.
- When a new lecture file is added, convert its Markdown version so agents can
  read it without a binary viewer.

## Version Control Discipline
- Never commit or push immediately after making changes.
- After edits, show the user the diff/status and wait for an explicit instruction.
- Commit only when the user asks; push (public remote) only with separate confirmation.

## Ownership & Verification
- Before modifying or deleting any content, check the git history first.
- If a change in the repository was NOT done by us (agents), ASK the user first
  whether they made it — never assume or silently overwrite it.
- Do not take initiative outside the assigned task (renaming, scaffolding, adding
  files, restructuring) without explicit confirmation.
- When in doubt or not understanding something, ASK the user instead of guessing.

## No AI-fingerprints in Deliverables
Anything the lecturer will see (notebooks, the published web book, scripts) must
read as natural, human-written work — not as AI-generated output:

1. **Never reference agent configuration files inside code/documents** that the
   reader can see: `AGENTS.md`, `CLAUDE.md`, `.opencode/`, `skills/`, etc.
   Example of a banned pattern: `while not (PROJECT_ROOT / "AGENTS.md").exists()`.
2. No decorative comment banners (`# ============`) and no `CELL n` / `SEL n`
   cell labels.
3. Comments must be short and natural; do not restate the code line by line, and
   avoid agent-style narration such as `# (REFERENCE — not executed)` or
   `print("… helper ready (function definitions only, not executed)")`.
4. Avoid excessive/redundant status prints and guard scaffolding that reads like
   instructions (`print("Change _re_crawl = True to re-crawl")`).
5. Keep file paths simple (relative to the project root); avoid over-engineered
   root-discovery loops.

## Project Help Files
- Read `AGENTS.md`, `README.md`, and other project help files
  to understand the task before working.
- Treat these files as authoritative context for how the project is interpreted.
- At the start of a new session, recall PPW context from Supermemory
  (`search_memory`) before working, so no context needs to be rebuilt.

## Available Agents
- Delegate work to the configured subagents instead of doing everything inline:
  - `python-helper` — debug, review, and write Python code for this project
  - `data-scientist` — data mining and data science analysis following CRISP-DM
- Subagents are defined as files in `.opencode/agent/`.
- Use subagents for heavy or parallelizable work to keep the main context clean.

## Language
- Interact with the user in Indonesian unless asked otherwise.
- **English** for: source code, comments, docstrings, commit messages,
  `README.md`, `AGENTS.md`, `lectures/`, `intro.md`, `CRISP-DM/*`, and build
  tooling/config.
- **Indonesian (may mix with English)** for the coursework content the student
  reads: `note.md`, `note/note-N.md`, `book.md`, and `book/book-N.ipynb`.
