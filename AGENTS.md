# PPW — Web Search & Mining

## Project Info
- Practical course: Web Search & Mining
- Python 3.14.7, virtual environment in `.venv/`
- Jupyter kernel: `enWebmining`

## Hard Rules
Non-negotiable. Every violation blocks the task.

1. All code is Python only (no TypeScript/JavaScript).
2. Web extraction uses `trafilatura` (requests+bs4 only for pages it cannot handle).
3. DataFrame output: columns `id`, `isi_berita`, `label`, `url`.
4. Never crawl without a polite delay of at least 1 second; crawling ethics apply.
5. Data is already in `data/Web-Mining/crawling_detik.csv` — do not re-crawl unless asked.
6. One print/visualization per notebook cell (one output per cell).
7. Never delete existing crawl data without permission.

## Key Commands
- Activate venv: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run Jupyter: `jupyter lab`
- Re-crawl: `python scripts/run_crawl.py`
- Orange pipeline: `.venv-orange/bin/python scripts/orange-task3/run_pipeline.py`
- Lint: `.venv/bin/ruff check scripts notebook`
- Format check: `.venv/bin/ruff format --check scripts`
- Type check: `.venv/bin/pyright scripts` and `.venv/bin/pyrefly check`
- Pre-commit gate: `.githooks/pre-commit` (ruff + pyright; enable once with
  `git config core.hooksPath .githooks`)

## Code Conventions
- Use `with_metadata=True` or `include_comments=False` on trafilatura
- Keep file paths simple (relative to the project root); avoid over-engineered
  root-discovery loops

## Project Structure
Full inventory, per-folder detail, and course layout live in
[Project map](docs/project-map.md). Keep the mental model:

- `notebook/` — Jupyter Book build root (built & published to GitHub Pages).
  The coursework core is `note/` + `note.md` and `book/` + `book.md`:
  `note.md` pairs with `note/note-N.md`, `book.md` with `book/book-N.ipynb`.
  Deliverables never cite or rely on `CRISP-DM/`; each stream stands alone.
- Work on a task in this order: `note-N.md` (material) → `note.md`
  (instructions) → `book-N.ipynb` (working process) → `book.md` (result summary,
  LAST, so numbers match the executed notebook).
- `data/Web-Mining/` holds the PPW dataset; `data/IE/` holds IE court outputs
  (personal data — local only, never committed).
- `scripts/`, `resource/` (lecture materials + read-only IE sub-project),
  `img/`, `requirements.txt` — see the project map for details.

## Separate Courses
This workspace hosts more than one course; keep the streams apart. No page or
notebook of one course may cite or rely on the deliverables of another, and no
course may use another course's data directory. Chapter file lists live in the
[Project map](docs/project-map.md):

- **PPW**: `intro.md`, `note/`, `book/`, `CRISP-DM/`, `data/Web-Mining/`.
- **IE**: `IE.md`, `IE/`, `data/IE/`.
- **ML**: `ML.md`, `ML/`.

## Coursework Consistency
Every task folder follows the same template so the published web book reads
uniformly:

- `note.md` — one `## Note N — <topik>` per task, a numbered instruction list,
  closing line `Catatan materi kuliah N: [Note N](note/note-N.md)`.
- `note/note-N.md` — lecture material summary only, headed `# <topik>`; must NOT
  repeat the task list.
- `book.md` — one `## Book N — <topik>` per task, result bullets, closing line
  `Proses pengerjaan: [Book N](book/book-N.ipynb)`.
- `book/book-N.ipynb` — working process: unnumbered `## ...` headings, short
  prose, exactly ONE output per cell, closed by a `## Conclusion` section.
- Headings are full English, at most level 3 (`###`), no more than 4 words
  (count alphanumeric tokens separated by spaces; `&`, `—`, `:` not counted).
  Applies to `note.md`, `book.md`, `note/note-N.md`, `book/book-N.ipynb`,
  `intro.md`, `CRISP-DM.md`, `IE.md`, and the `CRISP-DM/` notebooks.

Data handling principles for the working notebooks:

- Explore (EDA) BEFORE any dimensionality reduction or column/fitur removal.
- Every transformation is transparent: show examples (or counts/small tables)
  BEFORE and AFTER each change.
- The model-ready dataset is the TF-IDF vector representation; no other dense
  representation is saved as the final dataset.
- Slang/foreign normalization is context-aware: protect capitalized proper nouns
  using original casing, resolve ambiguous tokens with a small context-window
  heuristic, and surface every ambiguous case in a decision table.
- Decisions are evidence-driven: names, ambiguous tokens, and counts surface from
  notebook output at execution time — never prefilled in policy files.
- Foreign-language handling is preserve-first: translate a token only when every
  occurrence shares one non-name meaning with a single Indonesian equivalent,
  proven by context; otherwise keep and document why.

## Main Libraries
List and install notes: `trafilatura`, `pandas`, `scikit-learn`, `nltk`/`spacy`,
`langid`, `Sastrawi`, `rank-bm25`, `wordcloud`, `gensim`, `torch` — see the
[Project map](docs/project-map.md).

## Course Rules
- Jupyter kernel must be `enWebmining` (not the default python3)
- Never delete existing crawl data without permission
- Use a polite User-Agent when crawling
- Include crawling ethics in every notebook that performs crawling (collection or
  re-crawl); non-crawling notebooks get a one-line data provenance note
- Follow the Crawling Ethics rules below for every collection, in any course

## Crawling Ethics
Any notebook that collects from the web must pass these rules before its first
request:

1. Read `robots.txt` and the site's terms of service first. If automated access is
   disallowed, do not crawl automatically: request written permission, or use an
   official API or export instead.
2. Never bypass bot protection. No stealth plugins, header or User-Agent
   spoofing, proxy or VPN rotation, CAPTCHA solving, cookie replay, or rate-limit
   evasion, regardless of how the block is reported.
3. Stop on `403` or `429` and record the refusal in the notebook instead of
   looking for another way in.
4. Identify the client honestly, keep at least a one-second delay between
   requests, avoid parallel bursts, and keep the volume small.
5. Document the authorization status in the working notebook — who granted it,
   when, and what scope it covers. Concrete findings about one specific site
   belong in that notebook, never in this policy file.
6. Public court and news data contains personal names. Keep row-level data and
   raw snapshots local; published pages show aggregate counts, schemas, and
   source URLs only.

## Lecture Instructions
- Course lecture/assignment instructions live in `resource/Web-Mining/` as
  editable Markdown (`.md`) files, each paired with the original source file
  (`.ppt` / `.pptx`).
- **Before modifying code or writing any program**, AI agents MUST first read the
  relevant instruction file(s) and treat them as authoritative for interpreting
  the assignment.
- When a new lecture file is added, convert its Markdown version (same base name,
  `.md` extension) so agents can read it without a binary viewer.
- Extracting lecture images (asset naming, PNG rules) — see the
  [Project map](docs/project-map.md).

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
- When in doubt or not understanding something, ASK instead of guessing.

## Working Flow
Each task follows a single inline pass with built-in review gates:

- **Plan** — read help files and `resource/Web-Mining/*.md`, then fix the file
  outline and the verification rubric before writing anything. Instruction files
  stay generic; concrete findings from earlier runs are never written into them.
- **Execute with observation** — write and RUN code, read every output, and
  improvise from data (artifacts, ambiguous tokens, counts), deriving rules and
  decision tables from real numbers at execution time. Where useful, load the
  `data-quality` skill for the text-noise taxonomy and strict EDA checklist.
- **Verify** — after finishing, run the Verification Rubric below and fix
  failures before delivering.

JARVIS owns all three passes. Show `git status`/`git diff` — commit only on
explicit instruction.

## Verification Rubric
Run these checks on every finished task before showing results:

1. `note.md` holds only the generic numbered task instructions; no
   code-derived names, tokens, or counts.
2. `note/note-N.md` is lecture-material only and never repeats the task list.
3. Working notebook: kernel `enWebmining`; sections match the task list; exactly
   ONE output per code cell; every transformation shows before/after examples or
   counts; decision tables come from executed code with real numbers.
4. `book.md` numbers match the executed notebook outputs; closing line
   `Proses pengerjaan: [Book N](book/book-N.ipynb)` present.
5. No AI fingerprints in visible deliverables: no `AGENTS.md`/`.opencode/`/
   `skills/` references, no decorative banners or `CELL n`/`SEL n` labels, no
   agent-style narration prints.
6. Separate-course chapters: `IE.md` links a notebook that exists and is listed in
   `_toc.yml`; stored notebook outputs contain no personal names or case numbers;
   any collection states its access limits and never documents a bypass.
7. Source code stays as simple as the task allows: no extra features,
   abstractions, or refactors beyond the objective. The closing message answers
   the five simplicity questions from the global `AGENTS.md` checklist with
   checkable facts (paths, counts, command output).
8. Static checks are clean on changed files: `.venv/bin/ruff check scripts
   notebook`, `.venv/bin/ruff format --check scripts`, `.venv/bin/pyright scripts`,
   and `.venv/bin/pyrefly check` report zero errors AND warnings. Tool noise is
   suppressed narrowly at the source, never by disabling a whole rule.

## No AI-fingerprints in Deliverables
Anything the lecturer will see (notebooks, the web book, scripts) must read as
natural, human-written work:

1. **Never reference agent configuration files inside code/documents** the reader
   can see: `AGENTS.md`, `CLAUDE.md`, `.opencode/`, `skills/`, etc.
2. No decorative comment banners and no `CELL n` / `SEL n` cell labels.
3. Comments are short and natural; do not restate code line by line, and avoid
   agent-style narration (`# (REFERENCE — not executed)`, etc.).
4. Avoid excessive/redundant status prints and guard scaffolding that reads like
   instructions.
5. Keep file paths simple (relative to the project root); avoid over-engineered
   root-discovery loops.

## Project Help Files
- Read `AGENTS.md`, `README.md`, and other project help files
  to understand the task before working.
- Treat these files as authoritative context for how the project is interpreted.
- At the start of a new session, recall PPW context from Supermemory
  (`search_memory`) before working.

## Available Agents
- JARVIS (main agent) handles all coding and inline QA; the routine workflow runs
  inline without dedicated subagents.
- Global subagents stay for their domains: `edith` (Linux sysadmin; also OpenCode
  runtime diagnosis) and `friday` (documents, research, general knowledge) — see
  identity tags and escalation rules in the global `~/.config/opencode/AGENTS.md`.
- Reusable project skills live in `.opencode/skills/`:
  - `data-quality` — text-noise taxonomy and strict EDA checklist for the news
    corpus (load when cleaning/exploring Indonesian text).
  - `data-preprocessing` — IR preprocessing snippets (tokenization, stopwords,
    stemming, TF-IDF).
  - `crawling` — polite trafilatura crawling workflow and ethics.
  - `information-extraction` — IE sub-project pipeline and verification workflow
    for `resource/IE/`.
  Load the matching skill when a task enters one of those domains.

## Language
- Interact with the user in Indonesian unless asked otherwise.
- **English** for: source code, comments, docstrings, commit messages,
  `README.md`, `AGENTS.md`, `resource/Web-Mining/`, `intro.md`, `CRISP-DM/*`,
  and build tooling/config.
- **Indonesian (may mix with English)** for the coursework content: `note.md`,
  `note/note-N.md`, `book.md`, `book/book-N.ipynb`, `IE.md`, and `IE/*.ipynb`.
  Heading text is always English per the heading rule; only the narrative prose
  uses the language listed here.