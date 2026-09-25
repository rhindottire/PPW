# Catatan Folder ML

Catatan pembacaan `resource/IE/ML/`. Dibaca read-only (via `unzip -p`).
Source `ML1-20260913T082839Z-1-001.zip` & `ML2-20260913T082847Z-1-001.zip`
sudah diekstrak ke `ML/ML1/` dan `ML/ML2/`; arsip `.zip` aslinya dihapus dari
repo setelah ekstraksi (semua isi terverifikasi terekstrak).

## Ide Utama

NER dokumen hukum Indonesia memakai **CRF (sklearn-crfsuite)** berbasis fitur
token — TANPA embedding model besar. Flair dipakai hanya untuk **POS tagging**.
ML1 = eksperimen pembanding fitur (pos/prev/next); ML2 = pipeline skripsi
end-to-end + eksperimen 600 dokumen.

## ML1 (ML1/)

### Inventori
- `POS Tag.ipynb`, `Flair_2_0.ipynb` — POS Flair
- `make-prev-next.ipynb` — membuat kolom prev/next dari shift word
- `NER-200-{WithoutPos,WithPos,WithPosPrev,WithPosNext,WithPosPrevNext}.ipynb` — 5 varian
- `LEGALNER-POS-PREV-NEXT-26.csv` (135.974 baris, 26 doc), `LEGALNER-POS-PREV-NEXT-200.csv` (1.048.575 baris, 108 doc)

### POS Tag.ipynb
- Flair `SequenceTagger` (POS/upos), `use_crf=True`, hidden 256
- Embedding: `WordEmbeddings('id-crawl')` + `id` (fastText 300d)
- Corpus: `UD_INDONESIAN`, lr 0.1, batch 32, epoch 10
- Input `legal-dataset500.csv` (Drive, tidak ada di zip) → `pos500.csv`

### make-prev-next.ipynb
- `prev = word.shift(insert '.')`, `next = word.shift(append '.')`
- Output `datasets/pos-prev-next200.csv`; **penamaan beda** dengan yang dibaca
  NER (`LEGALNER-POS-PREV-NEXT-200.csv`) → harus rename manual

### NER-200-* (5 varian fitur CRF)
- Vector part → `DictVectorizer` + 5 classifier: MultinomialNB, SGD, PassiveAggressive, Perceptron, LinearSVC
- CRF part → `sklearn_crfsuite.CRF(lbfgs, c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)`
- Split 75 doc train / 32 doc test (hardcode `doc[74]`; komentar "140/60","20/6" inkonsisten)
- `SentenceGetter` groupby kolom `sentence` saja (**cacat**: nomor kalimat restart antar doc)

Hasil tersimpan (train vs test):

| Varian | NB | SGD | PAC | Perceptron | SVM | CRF |
|---|---|---|---|---|---|---|
| WithPos | 0.77/0.07 | 0.95/0.10 | 0.94/0.10 | 0.94/0.08 | 0.71/0.09 | — (error CRF) |
| WithPosPrev | 0.79/0.11 | 0.95/0.12 | 0.95/0.17 | 0.95/0.17 | 0.48/0.13 | — |
| WithPosNext | 0.77/0.10 | 0.95/0.12 | 0.95/0.15 | 0.94/0.12 | 0.22/0.09 | — |
| WithPosPrevNext | 0.81/0.11 | 0.96/0.14 | 0.96/0.21 | 0.95/0.21 | 0.70/0.19 | — |
| WithoutPos | 0.79/0.11 | 0.95/0.10 | 0.95/0.10 | 0.95/0.11 | 0.75/0.10 | 0.96/**0.56** |

- Accuracy didominasi O (93%); macro-F1 ≤ 0.21 di semua vector classifier → minoritas tak tergambar
- CRF bermakna hanya `WithoutPos`: acc 0.96, macro-F1 0.56, train 157 dtk; `WithPos`
  terhenti `KeyError: 'Unnamed: 0'` (cell 80), varian lain menyisakan output CRF utuh

#### Per-file varian NER-200 (5 notebook, 6 metode per file)

| Notebok | Fitur token | Status (2026-09-13) |
|---|---|---|
| NER-200-WithoutPos.ipynb | word + jendela ±1 | CRF tereksekusi (acc 0.96/macro-F1 0.56); 5 vector classifier tereksekusi |
| NER-200-WithPos.ipynb | word + pos | hasil 5 vector classifier tersimpan; sel CRF tereksekusi lalu `KeyError: 'Unnamed: 0'` |
| NER-200-WithPosPrev.ipynb | word + pos + prev | hasil tersimpan; sel CRF juga tereksekusi (output utuh) |
| NER-200-WithPosNext.ipynb | word + pos + next | hasil tersimpan; sel CRF juga tereksekusi (output utuh) |
| NER-200-WithPosPrevNext.ipynb | word + pos + prev + next | hasil tersimpan; sel CRF juga tereksekusi (output utuh) |

Semuanya: patch path CSV → folder sama + `to_dict('records')` + `ffill()` + hapus `jcopml` agar
bisa dijalankan lokal (diverifikasi dengan replika `-WithoutPos` pada subset 26: CRF fit 59,5 s).

### Statistik `LEGALNER-POS-PREV-NEXT-200.csv`
- 1.048.575 baris data + header = **tepat batas Excel** (1.048.576) → terpotong export Excel
- 108 doc unik (bukan 200); 1 baris tag kosong `''`
- Distribusi: `O` 92.98%; `I_DEFN` 2.41%, `I_ARTV` 1.57%, `B_DEFN` 1.24%, sisanya <1%

### Bug & Risiko ML1
1. `X.to_dict('Record')` → benar `'records'`; ValueError di pandas modern
2. `fillna(method='ffill')` deprecated (dihapus pandas ≥3.0)
3. `SentenceGetter` groupby `sentence` tanpa `doc` → konteks lintas dok tercampur
4. Path `../datasets/LEGALNER...csv` — CSV ada di folder sama, bukan `datasets/` → file tak ketemu
5. Import `jcopml` tak terpakai → crash bila tak terpasang
6. Sel CRF **belum pernah dieksekusi** (butuh ~3–17 menit)
7. `updated-sklearn-crfsuite` (fork MeMartijn) diperlukan di Python ≥3.12/3.14 (PyPI asli rawan gagal build)

## ML2 (ML2/)

### Inventori
- `ReadMe.docx`: app HF `huggingface.co/spaces/byann/validation-ner`;
  dataset Drive folder `1VkY-jsvbwiNbUg1xWfGevHR75CaUx96t`; pembagian kerja Colab/Kaggle
- `POS tagging.ipynb`: identik dgn ML1 POS; **copy `best-model.pt` ke Drive**
- `FinalCode.ipynb` (1.2 MB, 103 sel): pipeline end-to-end
- `Testing/600crf*.ipynb` (7 varian, dijalankan di Kaggle)

### FinalCode.ipynb (alur)
1. **Scraping** `putusan3.mahkamahagung.go.id` (PN Bangkalan dkk): pagination → unduh PDF → ekstrak teks → `data_bkl.csv` → gabung 4 PN = 602 dok (`data_all.csv`)
2. **Anotasi otomatis dict-based**: `generate_label(row)` dari metadata
   `entities_all.xlsx` → map label (penuntut→B_PROS, terdakwa→B_DEFN, dst.);
   `labeling_token` trie matching + `handleDuplicatePena` (B_PENA kedua → B_PUNI)
3. `split_token` → fragment per ';' → `df_pertoken` `doc,fragment,token,label`
4. **POS Flair** training ulang → tagging 2.041.298 token → `data_mlformat_clean.csv`
5. Feature engineering (Kaggle): `FragmentGetter` + `token2features`
6. Model CRF, split 70/30 acak seed 42 → **acc 0.99, macro P 0.87/R 0.81/F1 0.83** (test 538.488 token)
7. Testing PDF baru: preprocessing + `representation_crf` + **fitur minimal token/prev/next** → predict `600crf.pkl`
8. App **Gradio** + fuzzywuzzy + joblib memuat `600crf_prevnext.pkl`

### Login & Bug FinalCode
1. **Mismatch fitur train vs inference**: sel 73 (train) fitur lengkap
   (token+pos+prev+next+wordform), sel 93–94 (inference) meng-comment nyaris semua →
   fitur tidak konsisten dengan model
2. `entities.applymap(str)` dihapus di pandas ≥2.1 → error di env baru
3. `fillna(method='ffill')` deprecated
4. Butuh Drive: `data_all.csv`, `entities_all.xlsx`, `best-model.pt`, `600crf*.pkl` (tak ada di zip)
5. Crawling tanpa delay/UA sopan

### Testing/600crf-*.ipynb (hasil, test ~389.179 token)
- Semua: `gdown` file_id `1-GhEOfug-V5KbvESx3ZzQOxQ8x0HIZrG` → `data.csv` (37,8–44,4 MB);
  drop doc 601/602 → 600 doc; train 70% **doc urut** (tidak acak): 7.985 fragment train / 3.287 test

| Varian | Fitur | Acc | Macro-F1 |
|---|---|---|---|
| 600crf | token saja | 0.95 | — |
| 600crf-pos | + postag | 0.95 | 0.60 |
| 600crf-wordfrom | + wordform | 0.95 | 0.59 |
| 600crf-pos-wordfrom | token+wordform+pos | 0.95 | 0.59 |
| **600crf-prevnext** | + prev1/prev2/next1/next2 | **0.97** | **0.81** |
| 600crf-pos-prevnext | + pos & prev/next | 0.97 | 0.80 |
| 600crf-prevnext-wordfrom | prev/next + wordform | 0.97 | 0.80 |
| 600crf-pos-prevnext-wordfrom | semua | 0.97 | 0.81 |

- **Kesimpulan: fitur prev/next memberi lompatan terbesar** (0.59→0.81);
  POS & wordform marginal
- Model disimpan `600crf{...}.pkl`; `eli5.show_weights` untuk interpretasi
- Dua versi file Drive (37,8 / 44,4 MB) → perbedaan support antar run

#### Per-file Testing/600crf (8 notebook)

| Notebook | Fitur CRF | Status (2026-09-13) |
|---|---|---|
| Testing/600crf.ipynb | token saja | hasil tersimpan (acc 0.95); butuh gdown Drive |
| Testing/600crf-pos.ipynb | token + postag | hasil tersimpan (macro-F1 0.60); varian `-pos` berisiko KeyError bila Drive berubah |
| Testing/600crf-wordfrom.ipynb | token + wordform | hasil tersimpan (macro-F1 0.59) |
| Testing/600crf-pos-wordfrom.ipynb | token + wordform + pos | hasil tersimpan (macro-F1 0.59) |
| Testing/600crf-prevnext.ipynb | token + prev1/prev2/next1/next2 | hasil tersimpan (macro-F1 0.81, terbaik) |
| Testing/600crf-pos-prevnext.ipynb | + pos & prev/next | hasil tersimpan (macro-F1 0.80) |
| Testing/600crf-prevnext-wordfrom.ipynb | prev/next + wordform | hasil tersimpan (macro-F1 0.80) |
| Testing/600crf-pos-prevnext-wordfrom.ipynb | semua fitur | hasil tersimpan (macro-F1 0.81) |

Semuanya `gdown` file_id `1-GhEOfug-V5KbvESx3ZzQOxQ8x0HIZrG`; sudah dapet `gdown` +
`sklearn-crfsuite` di `.venv` → tinggal akses Drive untuk replikasi.

## Perbandingan ML1 vs ML2

| Aspek | ML1 (2023) | ML2 (2024) |
|---|---|---|
| Tujuan | Eksperimen fitur (pos/prev/next) | Pipeline skripsi end-to-end + app |
| NER model | 5 vector classifier + CRF | CRF tunggal 7 kombinasi fitur |
| Fitur | kolom prev/next literal (shift) + word/pos + window | window token/pos fragmen + wordform + postag |
| Data | `doc,sentence,word,pos,prev,next,tag` 107–108 doc | `doc,fragment,token,pos,label` 600 doc |
| Hasil terbaik | CRF WithoutPos 0.96 acc / 0.56 macro-F1 | prevnext 0.97 / 0.81; FinalCode 0.99 acc / 0.83 macro-F1 |

## Run-Readiness

| Item | Status |
|---|---|
| ML1 POS/Flair | ⚠️ perlu Drive + download embedding id-crawl/id + UD (~300MB) + kernel enWebmining |
| ML1 make-prev-next | ❌ input `pos200.csv` tak ada di zip |
| ML1 NER-200-* | ❌ CSV perlu dipindah ke `../datasets/`; perbaiki to_dict/fillna; hapus jcopml; CRF butuh ~3–17 menit; kernel enWebmining |
| ML2 POS tagging | ⚠️ sama dgn ML1 POS |
| ML2 FinalCode | ⚠️ butuh Drive (data_all.csv, entities_all.xlsx, model pkl); perbaiki applymap/fillna; samakan fitur sel 93–94 |
| ML2 Testing/600crf-* | ✅ paling siap: perlu pip gdown/jcopml/eli5 + fork MeMartijn sklearn-crfsuite; varian -pos berisiko KeyError bila Drive di-update |