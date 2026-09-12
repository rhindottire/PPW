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
  - `note/` + `note.md` — coursework notes (headings `Note N`). `note.md` holds
    the short task instructions as explained in class (the authoritative task
    list, one numbered list per task); `note/note-N.md` holds the lecture
    material summary written to be displayed on GitHub Pages / the web book.
  - `book/` + `book.md` — coursework deliverables (headings `Book N`).
    `book.md` summarizes the task results; `book/book-N.ipynb` is the working
    notebook with the details and overall process that produces those results.
  - Work on a task in this order: `note-N.md` (material) → `note.md`
    (task instructions) → `book-N.ipynb` (working process) → `book.md` (result
    summary, LAST, so numbers match the executed notebook).
  - `CRISP-DM/` — CRISP-DM stage notebooks (kernel: enWebmining)
    - `Business.ipynb` — Task 1: goal, scope & crawling ethics (completed)
    - `EDA.ipynb` — Task 1: detik.com crawl & exploration (completed)
    - `Input.ipynb`, `Modeling.ipynb`, `Output.ipynb`, `Production.ipynb` —
      placeholders for upcoming tasks
  - `intro.md`, `CRISP-DM.md`, `_config.yml`, `_toc.yml` — book pages/config
- `data/crawling_detik.csv/.json` — crawl results of 200 articles (100 sport + 100 finance)
- `scripts/run_crawl.py` — standalone crawling script (re-crawl entry point)
- `lectures/` — course lecture/assignment materials (`.ppt`/`.pptx` + readable
  `.md`, with content images under `lecture-{N}-assets/` as `slide{NN}-{slug}.png`)
- `requirements.txt` — pinned package list

## Coursework Consistency
Every task folder follows the same writing template, so the published web book
reads uniformly and no instruction needs repeating:

- `note.md` — one `## Note N — <topik>` per task, a numbered instruction list
  (the task as explained in class), and a closing line
  `Catatan materi kuliah N: [Note N](note/note-N.md)`.
- `note/note-N.md` — lecture material summary only, headed `# <topik>`; it must
  NOT repeat the task list (that lives only in `note.md`).
- `book.md` — one `## Book N — <topik>` per task, result bullets, and a closing
  line `Proses pengerjaan: [Book N](book/book-N.ipynb)`.
- `book/book-N.ipynb` — the working process: unnumbered `## ...` section
  headings, short prose between code cells, exactly ONE output per cell, closed
  by a `## Kesimpulan` section.

Data handling principles for the working notebooks:

- Explore the data (EDA) BEFORE any dimensionality reduction or column/fitur
  removal so anomalies surface first.
- Every data transformation must be transparent: show examples (or counts and
  small tables) of the data BEFORE and AFTER each change.
- The extraction model-ready dataset is the TF-IDF vector representation; no
  other dense representation is saved as the final dataset.
- Slang/foreign-language normalization must be context-aware: protect
  capitalized proper nouns using the original casing of the text, resolve
  ambiguous tokens with a small context-window heuristic, and surface every
  ambiguous case in a decision table for review.
- Decisions must be evidence-driven: names, ambiguous tokens, and counts found
  during work surface from notebook output at execution time — never prefilled
  in `note.md`, `book.md`, or policy files (they hold only generic
  instructions). Concrete findings live in the working notebook.
- Foreign-language handling is preserve-first: translate a token only when
  every occurrence shares one non-name meaning with a single natural Indonesian
  equivalent, proven by context; otherwise keep and document why.

## Main Libraries
- `trafilatura` — web text extraction
- `pandas` — data manipulation
- `scikit-learn` — TF-IDF, clustering
- `nltk` / `spacy` — NLP
- `langid` — language detection
- `Sastrawi` — Indonesian stemming
- `rank-bm25` — document ranking
- `wordcloud` — word frequency visualization
- `torch` — deep learning (CUDA-enabled)

## Course Rules
- Jupyter kernel must be `enWebmining` (not the default python3)
- Never delete existing crawl data without permission
- Use a polite User-Agent when crawling
- Include crawling ethics in every notebook that performs crawling (collection
  or re-crawl); non-crawling notebooks only get a one-line data provenance note

## Lecture Instructions
- Course lecture/assignment instructions live in `lectures/` as editable
  Markdown (`.md`) files, each paired with the original source file (`.ppt` /
  `.pptx`).
- **Before modifying code or writing any program**, AI agents MUST first read
  the relevant instruction file(s) in `lectures/` and treat them as
  authoritative for interpreting the assignment.
- When a new lecture file is added, convert its Markdown version so agents can
  read it without a binary viewer.
- Name the Markdown copy after the source file (same base name with the `.md`
  extension), e.g. `01. Pengantar Web Mining.ppt` → `01. Pengantar Web
  Mining.md`.

### Lecture assets
When a lecture Markdown references images, extract them as follows:

- Extract the content-material images from the **source file**
  (`lectures/*.ppt` / `lectures/*.pptx`), not from cached or scraped copies.
- Keep only substantive diagrams (typically >20 KB, near document size, and
  unique to one slide). Skip slide backgrounds/templates (e.g. a full-slide
  image reused across many slides) and decorative icons/bullets (small,
  15–50 px, ~1–5 KB).
- Every file must be a **valid PNG that renders in browsers**; convert
  mislabeled JPEG/EMF extracts to real PNG before committing.
- Name files consistently as `slide{NN}-{slug}.png` (e.g.
  `slide30-arsitektur-jaringan.png`) inside `lectures/lecture-{N}-assets/`,
  and reference them as `![...](./lecture-{N}-assets/slide{NN}-{slug}.png)`.
- When the same diagram appears on several slides, reference it once at the
  first occurrence.

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

## Working Flow
Each task runs through three roles so revisions are caught before the user sees
them:

- **Plan** — read help files and `lectures/*.md`, then fix the file outline and
  the verification rubric before writing anything. Instruction files stay
  generic; concrete findings from earlier runs are never written into them.
- **Execute with observation** — the executor writes and RUNS code, reads every
  output, and improvises from what the data shows (artifacts, ambiguous tokens,
  counts), deriving rules and decision tables from real numbers at execution
  time. Where useful, `eda-inspector` runs in parallel and reports independent
  findings the executor merges before proceeding.
- **Verify** — `plan-verifier` checks deliverables against the plan rubric
  (note.md without code-derived findings; notebook sections matching the task
  list; one output per cell; kernel `enWebmining`; `book.md` numbers matching
  the executed notebook; no AI fingerprints). Fix before delivering.

JARVIS orchestrates: assign the executor, integrate observer findings, run the
verifier, and show `git status`/`git diff` — commit only on explicit
instruction.

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
  - `eda-inspector` — strict data quality / EDA auditor that returns structured
    findings (artifacts, ambiguous tokens, evidence) for the executor to merge
  - `plan-verifier` — checks finished deliverables against the plan rubric
- Subagents are defined as files in `.opencode/agent/`.
- Use subagents for heavy or parallelizable work to keep the main context clean.
- Reusable project skills live in `.opencode/skills/` (e.g. `data-quality` for
  the text-noise taxonomy and strict EDA checklist).

## Language
- Interact with the user in Indonesian unless asked otherwise.
- **English** for: source code, comments, docstrings, commit messages,
  `README.md`, `AGENTS.md`, `lectures/`, `intro.md`, `CRISP-DM/*`, and build
  tooling/config.
- **Indonesian (may mix with English)** for the coursework content the student
  reads: `note.md`, `note/note-N.md`, `book.md`, and `book/book-N.ipynb`.
