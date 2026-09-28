---
name: data-quality
description: Text-noise taxonomy and strict EDA/data-quality checklist for the PPW news corpus. Use whenever cleaning or exploring Indonesian text data (CRISP-DM stages, book tasks, or preprocessing), to classify artifacts, protect proper nouns, decide foreign-language policy, and produce evidence-driven decision tables.
---

# Data Quality & Text-Noise Taxonomy

Project-wide rules for turning the raw crawl (`data/crawling_detik.csv`) into a
clean, defensible text corpus. Applies to every notebook that cleans or
explores text (book tasks, CRISP-DM stages, future analyses), not just one task.

## Principles
1. **EDA before cleanup decisions.** Explore and quantify anomalies before any
   column/fitur removal. No pre-decided lists — names, tokens, and counts must
   surface from executed output at run time.
2. **Transparent transformations.** Each change shows examples (or counts and
   small tables) BEFORE and AFTER.
3. **Evidence-driven decisions.** Every artifact class and ambiguous token ends
   up in a decision table built in code with real numbers and context windows.
4. **Preserve-first foreign language.** Keep foreign sentences, quotes, and
   loanwords unless a token meets all criteria to translate (below).

## Text-noise taxonomy
Classify artifacts after a naive cleanup like
`re.sub(r"[^a-z\s]", " ", text.lower())`, then tokenize with length filter.

| Class | Example (source) | Decision guidance |
|---|---|---|
| Numeral/symbol residue | `x` from `3x3`, `adidas x Alba`; `u` from `U-20`; `ke` from `6-b`? | Drop single-character leftovers; they carry no lexical content |
| Unit / symbol tokens | `rp`, `kg`, `pt`, `cm`, `m` | Decide by table: currency and measurement units attached to numbers are symbols, not terms; drop unless a label-meaningful exception is proven |
| English particle inside a multi-word name | `of` in `Hall of Fame`, `de` in proper names | Protect the whole name span, including the lowercase particle |
| Two-letter English function words | `of`, `on`, `to`, `as`, `up`, `vs` | Occur in quotes/proper phrases; keep if they are genuine content in preserved quotes, otherwise covered by name-span protection |
| Slang-collision | token that is a slang-dictionary target AND a capitalized name in the source | Protect via original-casing evidence (see proper-noun rule) |
| Token-length residue | `a`, `i`, `u` from headers/abbrev | Enforce `min length = 2`; document count |

## Proper-noun protection (data-driven)
- A token is a name candidate if it appears capitalized mid-sentence in the
  **original** text and has no consistently lowercase counter-evidence.
- Multi-word names: consecutive capitalized tokens, with lowercase
  particles (`of`, `de`, `i`, `vs`) folded into the span, are protected as a
  whole.
- Protected names never undergo slang replacement or translation, even when a
  slang equivalent exists (`bca` vs `baca`, name tokens vs noun tokens).

## Foreign-language policy
1. Detect per **sentence** with `langid`; treat `{id, ms}` as Indonesian.
2. Keep sentences/quotes in their original language; document why (context
   preservation).
3. Detect per **token** only to surface candidates for a decision table; do not
   trust raw token-level `langid` (it labels common Indonesian words `en`).
4. Translate a token ONLY when every occurrence shares one non-name meaning
   that has a single natural Indonesian equivalent, proven by context windows.
   Otherwise preserve and document. Zero translations is a valid outcome.

## Strict EDA checklist
Run these before finalizing datasets (structural checks already covered in
`CRISP-DM/EDA.ipynb`):
- [ ] Missing values, duplicate rows/URLs, sequential `id`, label balance.
- [ ] Text-length distribution per label (describe + boxplot/histogram).
- [ ] Top tokens per label; flag anomalies.
- [ ] Cleanup artifact census (taxonomy table w/ counts + contexts).
- [ ] Language census per sentence; token-level evidence vs sentence-level.
- [ ] Name-vs-slang collision census (capitalized evidence + context).
- [ ] Before/after comparisons for every transformation.
- [ ] Unique-word count via scikit-learn; TF-IDF shape; storage as sparse files.
- [ ] Dimensionality-reduction decision with explained-variance numbers.

## Output
Final model-ready dataset only as TF-IDF sparse representation, saved under
`data/` (`.npz`, feature list, doc labels). When a notebook must show
discovery, keep numbers and decision tables inside the notebook — never in
`note.md` or `book.md`.