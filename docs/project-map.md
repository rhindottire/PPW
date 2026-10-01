# PPW Project Map

Inventory moved out of `AGENTS.md` so the always-loaded policy stays slim. Rules and
principles live in `AGENTS.md`; concrete paths, counts, and structures live here.

## Repository Layout

- `notebook/` — Jupyter Book build root (built and published to GitHub Pages).
  Structure follows the rhindottire/Data-Science pattern: methodology chapters plus
  a per-assignment coursework chapter, both coexisting. Every folder directly under
  `notebook/` stands on its own; none depends on another. The one exception is the
  coursework core — `note/` + `note.md` and `book/` + `book.md` — which is the heart
  of the project: `note.md` pairs with `note/note-N.md`, `book.md` with
  `book/book-N.ipynb`, and the `book/` notebooks may carry findings between tasks
  (explore in one book, apply the change in the next). The coursework deliverables
  are never tied to `CRISP-DM/`: they must not cite or rely on the `CRISP-DM/`
  notebooks as a source of decisions, and each stream remains comprehensible on its
  own. There are two kinds of Markdown page directly under `notebook/`:
  - **Summary/index** of a sibling folder's contents — only `CRISP-DM.md`
    summarizes the notebooks in `CRISP-DM/`.
  - **Role-specific pages** with their own content linked to a sibling folder —
    `note.md` and `book.md` are NOT summaries; each holds different content.
  - `note/` + `note.md` — coursework notes (headings `Note N`). `note.md` holds the
    short task instructions as explained in class (the authoritative task list, one
    numbered list per task); `note/note-N.md` holds the lecture material summary
    written to be displayed on GitHub Pages / the web book.
  - `book/` + `book.md` — coursework deliverables (headings `Book N`). `book.md`
    summarizes the task results; `book/book-N.ipynb` is the working notebook with
    the details and overall process that produces those results.
  - Task order: `note-N.md` (material) → `note.md` (task instructions) →
    `book-N.ipynb` (working process) → `book.md` (result summary, LAST, so numbers
    match the executed notebook).
  - `CRISP-DM/` — CRISP-DM stage notebooks (kernel: enWebmining)
    - `Business.ipynb` — Task 1: goal, scope & crawling ethics (completed)
    - `EDA.ipynb` — Task 1: detik.com crawl & exploration (completed)
    - `Input.ipynb`, `Modeling.ipynb`, `Output.ipynb`, `Production.ipynb` —
      placeholders for upcoming tasks
  - `intro.md`, `CRISP-DM.md`, `IE.md`, `_config.yml`, `_toc.yml` — book
    pages/config.
  - `IE.md` + `IE/` — published chapter for the separate Information Extraction
    course, not a PPW deliverable. `IE.md` states the objective, scope, results,
    access and ethics, and links the notebooks; `IE/NN-*.ipynb` are the working
    notebooks registered as sections in `_toc.yml`.
  - `ML.md` / `ML/` — placeholder chapter for the Machine Learning course.
- `data/Web-Mining/` — PPW dataset & model-ready artifacts:
  `crawling_detik.csv/.json` (200 articles, 100 sport + 100 finance),
  `tfidf_sparse.npz`, `tfidf_features.txt`, `tfidf_docs.csv`.
- `data/IE/` — Information Extraction assignment outputs, one folder per court:
  `PN-Ngawi/` holds the submitted CSV `IE-PN-Ngawi-<NIM>.csv`, the candidate URL
  list, the error report, and the `html/` snapshots. Snapshots and row-level CSV
  contain personal data, so they stay local and are never committed or published.
- `scripts/run_crawl.py` — standalone crawling script (re-crawl entry point).
- `scripts/orange-task3/` — Orange Data Mining re-run of Book 3: `task3.ows`
  (canvas), `run_pipeline.py` (same chain headless, prints the widget numbers),
  `orange-task-3.md` (findings), `results.json` (output). Orange lives in its own
  environment `.venv-orange` (Python 3.12, Orange 3.40) because Orange does not
  support the Python 3.14 of the main `.venv`; run it with
  `.venv-orange/bin/python scripts/orange-task3/run_pipeline.py`.
- `resource/` — non-PPW course materials shared in this workspace:
  - `resource/Web-Mining/` — course lecture/assignment materials (`.ppt`/`.pptx` +
    readable `.md`, assets under `lecture-{N}-assets/` as `slide{NN}-{slug}.png`).
  - `resource/IE/` — lecturer-provided IE sub-project (see below).
- `img/` — web book logo (`Doo.jpg`).
- `requirements.txt` — pinned package list (gensim is installed via a separate
  script — see section `[12]`).
- `docs/` — this project map (sibling to `AGENTS.md`, not part of the web book).

## Separate Courses

This workspace hosts more than one course. Keep the streams apart: no page or
notebook of one course may cite or rely on the deliverables of another.

- **PPW — Web Search & Mining**: `intro.md`, `note/` + `note.md`, `book/` +
  `book.md`, `CRISP-DM/` + `CRISP-DM.md`, and `data/Web-Mining/`.
- **IE — Information Extraction**: `IE.md`, `IE/`, and `data/IE/`.
- **ML — Machine Learning**: `ML.md` and `ML/`.

Rules for the IE and ML chapters:

- Each course keeps its own page pattern: a role-specific `.md` file that states
  the objective, scope, results, and constraints, plus notebooks registered as
  sections in `_toc.yml`.
- Working notebooks use unnumbered `## ...` section headings, short prose between
  code cells, exactly ONE output per code cell, and a closing `## Conclusion`.
- Headings follow the same limits as the PPW pages: full English, level 3 at
  deepest, at most 4 words each.
- Never renumber another course's tasks into this one, and never reuse another
  course's data directory.

## Main Libraries

- `trafilatura` — web text extraction
- `pandas` — data manipulation
- `scikit-learn` — TF-IDF, clustering
- `nltk` / `spacy` — NLP
- `langid` — language detection
- `Sastrawi` — Indonesian stemming
- `rank-bm25` — document ranking
- `wordcloud` — word frequency visualization
- `gensim` — word2vec / skip-gram (installed via `scripts/install_gensim.py`;
  no cp314 wheel, see `requirements.txt` `[12]`)
- `torch` — deep learning (CUDA-enabled)

## resource/IE — Lecturer-Provided IE Sub-Project

Hosted in this shared workspace. Treat every `.py` and `.ipynb` here as read-only
lecturer source: run it, verify it, and report what breaks without editing the
files. The student's own coursework for this course does not live here — it lives
in `notebook/IE/` and `data/IE/`. Structure:

- `GET-COURT/` (get-court crawlers), `RULE-BASED/` (regex IE → CSV), `DATASET/`
  (annotation/preprocessing), `ML/` (CRF NER: `ML1/NER-200-*`, `ML2/...` incl.
  `ML2/Testing/600crf-*`), `DL/` (bi-LSTM, needs TF), `BERT/` (BERT/RoBERTa/
  IndoBERT pretrain + SQLite indexing demo).
- `NOTES/` — verification deliverables (one `*-notes.md` per folder +
  `VERIFICATION-MATRIX.md`). Do NOT edit lecturer source files (`.py`, `.ipynb`)
  under `resource/IE/`; verify via copies in `/tmp` instead and keep the source
  bugs intact. Never overwrite `RULE-BASED/courtHistory.csv`. Classifications:
  `runnable`, `run-true`, `blocked-license`, `blocked-env`. Requirements section
  `[11]`/`[11b]` of `requirements.txt`. See `NOTES/VERIFICATION-MATRIX.md` for
  the full per-file status.
- **Tracked in git, and it holds court records.** Nine of these notebooks keep
  stored outputs that name judges (878 occurrences), carry case numbers (959),
  and name parties (177); `GET-COURT/metaPerceraianPASBY.csv` adds 997 divorce-case
  records with judge, registrar, ruling, and reasoning fields. The material is
  lecturer-provided and has been public since commit `57882e4`, so this is
  inherited rather than newly introduced, and it is not published to the web book
  — only `notebook/` is built. Know this before changing anything here, and keep
  the student's own row-level data in `data/IE/`, which stays out of version
  control.

## Lecture Assets

When a lecture Markdown references images, extract them from the **source file**
(`resource/Web-Mining/*.ppt` / `*.pptx`), not from cached or scraped copies. Keep
only substantive diagrams (typically >20 KB, near document size, and unique to one
slide); skip slide backgrounds/templates and decorative icons/bullets (small,
15–50 px, ~1–5 KB). Every file must be a valid PNG that renders in browsers —
convert mislabeled JPEG/EMF extracts to real PNG before committing. Name files
consistently as `slide{NN}-{slug}.png` inside
`resource/Web-Mining/lecture-{N}-assets/`, reference them as
`![...](./lecture-{N}-assets/slide{NN}-{slug}.png)`, and when the same diagram
appears on several slides reference it once at the first occurrence.