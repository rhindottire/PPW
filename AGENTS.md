# PPW — Web Search & Mining

## Project Info & Environment
- Course: Web Search & Mining (PPW) | Python 3.14.7 | Virtualenv: `.venv/` | Kernel: `enWebmining`
- Key Commands:
  - Run Notebook: `jupyter lab`
  - Re-crawl: `python scripts/run_crawl.py`
  - Orange Pipeline: `.venv-orange/bin/python scripts/orange-task3/run_pipeline.py`
  - Lint & Format: `.venv/bin/ruff check scripts notebook` && `.venv/bin/ruff format --check scripts`
  - Type Check: `.venv/bin/pyright scripts` && `.venv/bin/pyrefly check`
  - Pre-commit Gate: `.githooks/pre-commit` (enforces Ruff, Pyright, and dynamic Pytest)

## Multi-Course Workspace Boundaries & Scope
This workspace hosts 3 separate courses. Each stream stands alone with strict directory and data isolation:

| Stream | Core Notebooks & Notes | Local Data Directory | Course Scope & Specific Rules |
| :--- | :--- | :--- | :--- |
| **PPW** | `intro.md`, `note/`, `book/`, `CRISP-DM/` | `data/Web-Mining/` | Enforce: exactly 1 output per code cell + markdown interpretation. Model dataset: TF-IDF vector. |
| **IE** | `notebook/IE.md`, `notebook/IE/` | `data/IE/` (Local only) | Follow `resource/IE/` tasks. Stored outputs contain no personal names. Do NOT enforce 1 output/cell. |
| **ML** | `notebook/ML.md`, `notebook/ML/` | `data/ML/` | Follow `notebook/ML/` assignments. Do NOT enforce 1 output/cell. |

- **No Cross-Course Dependencies:** No notebook or page may cite or rely on the deliverables/data of another stream.
- **Workflow Order (PPW):** `note-N.md` (material) → `note.md` (task list) → `book-N.ipynb` (process) → `book.md` (result summary last).

## Web Extraction & Crawling Ethics (Hard Boundaries)
Non-negotiable. Every violation blocks the task.
1. **Extraction Library:** Use `trafilatura` (with `with_metadata=True` / `include_comments=False`). Fallback to `requests` + `bs4` only when trafilatura fails.
2. **DataFrame Output:** Must strictly follow columns `id`, `isi_berita`, `label`, `url`.
3. **Data Provenance:** Data is in `data/Web-Mining/crawling_detik.csv`. Never delete crawl data and do not re-crawl without permission.
4. **Polite Crawling Ethics:**
   - Always read `robots.txt` and Terms of Service first.
   - Maintain a polite delay of >= 1 second between requests; avoid parallel bursts.
   - Identify client honestly with a polite User-Agent; never bypass bot protection (no CAPTCHA solvers, proxy rotation, header spoofing).
   - Stop immediately on `403` or `429` and record refusal.
   - Keep row-level personal data local; published deliverables show only aggregate counts and source URLs.

## Deliverable Standards & Verification Checklist
All coursework must read naturally as human-written work (pass global 6-Layer Defense + these checks):
1. **Headings:** Full English, max level 3 (`###`), max 4 alphanumeric words (`&`, `—`, `:` not counted).
2. **Structure:**
   - `note.md`: Numbered generic instruction list; closing line `Catatan materi kuliah N: [Note N](note/note-N.md)`.
   - `note/note-N.md`: Lecture material summary only (headed `# <topik>`); never repeats task list.
   - `book.md`: Result bullets matching executed notebook numbers; closing line `Proses pengerjaan: [Book N](book/book-N.ipynb)`.
   - `book/book-N.ipynb`: Unnumbered `## ...` headings, 1 output per cell with immediate interpretation markdown, closing `## Conclusion`.
3. **Data Handling:** Explore (EDA) before dimension reduction; show before/after examples for all transformations; preserve proper nouns during normalization; translate foreign tokens only when unambiguous.
4. **No AI Fingerprints:** Never cite config/prompt files (`AGENTS.md`, `.opencode/`, `skills/`); no decorative cell banners (`CELL n`); comments short and natural.
5. **Readable Lectures:** Lecture instructions in `resource/Web-Mining/*.md` and `resource/IE/*.md` are authoritative. Always consult them before coding.

## Available Agents & Reusable Skills
- Core behaviors and governance follow global brain: `~/.gemini/config/AGENTS.md`.
- Project skills live in `.opencode/skills/`:
  - `data-quality`: Text-noise taxonomy and strict EDA checklist for Indonesian news corpus.
  - `data-preprocessing`: IR snippets (tokenization, stopwords, stemming, TF-IDF).
  - `crawling`: Trafilatura scraping patterns and ethics.
  - `information-extraction`: IE sub-project pipeline and verification.
- Before IE coursework, read `docs/ie-task-log.md` (task status, artifacts, known traps) and update it upon completion.
