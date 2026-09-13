# Verification Matrix — `notebook/IE`

Status tiap file terhadap misi dosen: **pastikan code bisa dijalankan**.
Diverifikasi 2026-09-13 pada `.venv` (Python 3.14.7, kernel `enWebmining`,
library section `[11]` `requirements.txt` sudah terpasang: python-crfsuite,
sklearn-crfsuite, flair, gdown, gradio, rapidfuzz, PyPDF2, transformers 4.57,
tokenizers, eli5).

- `runnable` — jalan apa adanya pada data yang tersedia.
- `run-true` — jalan setelah patch kecil yang sudah di-izin-kan (import typo,
  nama variabel, path data). Fix tercantum.
- `blocked-license` — tidak bisa jalan di env ini (data Drive/Kaggle hilang;
  TensorFlow tanpa wheel untuk Python 3.14) → diverifikasi via inspeksi kode.
- `blocked-env` — library tidak tersedia untuk Python 3.14.

## GET-COURT

| File | Status | Bukti / alasan | Fix lokal |
|---|---|---|---|
| `getURLlist.ipynb` | ⚠️ `runnable` tak lengkap | Hanya 2 halaman; anchor `'<a href="'` posisi 9 → 7 URL campuran; `verify=False`, tanpa delay/UA | Loop halaman; parser; +delay ≥1 dtk; User-Agent |
| `getMETAINFO.ipynb` | ❌ `blocked-license` | Path `/content/drive/...` (Colab); `IndexError` `rowsMETA2[1]`; ribuan `url` kosong | Lokalkan path; delay; parse `url` robust |
| `getFileDownload.ipynb` | ❌ `blocked-license` | Path `D:/6.PYTHON-CODE/...` (Windows); butuh CSV 21 kolom bebas-bug | Lokalkan path; validasi kolom |

Catatan etika: semua notebook tanpa delay/User-Agent/`verify=False` — tidak
boleh dipindah ke deliverable tanpa revisi etika crawl.

## RULE-BASED

| File | Status | Bukti / alasan | Fix |
|---|---|---|---|
| `entityGenerator.py` | ⚠️ `runnable` (versi lama) | Hanya untuk membaca; magic offset rapuh; lowercase | — |
| `newEntityGenerator.py` | ✅ `run-true` (terverifikasi) | **Replika berhasil (2026-09-13)** setelah fix; `O-48Pid.*.txt` dibuat; `errors='ignore'` agar tahan baris non-UTF8 | Ganti `nomor`→`baris` |
| `entityGenerator3.py` | ✅ `run-true` (terverifikasi) | `return listHasil` (15 kolom); replika butuh guard `eNomor` (regex gagal di beberapa file) | Guard `if eNomor:` |
| `ruleBased-IE.py` | ⚠️ `runnable` | Import `entityGenerator` (akses langsung); butuh `INPUT/` terisi (sudah: 14 txt) | — |
| `newRule-BasedIE.py` | ✅ `run-true` (terverifikasi) | **Replika berhasil**: 14 txt → 14 `O-*.txt`; crash hanya file `.zip` di INPUT | `errors='ignore'` |
| `ruleBased-IE3.py` | ✅ `run-true` (terverifikasi) | **Replika berhasil**: pipeline penuh INPUT→CSV; 14 nomor match CSV asli; baris kosong dari `.zip` ikut terbaca | Ganti `entityGenerator2`→`entityGenerator3` |
| `courtHistoryCsv.py` | ✅ `run-true` (terverifikasi) | Header + append; 15 kolom; replika tulis 1 header + 15 baris | — |

Pasangan input→output: 14 txt → 14 entitas; baris ke-15 (kosong) berasal dari
file `INPUT-*.zip` ikut terbaca `listdir` (pada run asli jadi `O-200Pid.*.txt`
tanpa input). `courtHistory.csv` asli (85 baris = 6× append) JANGAN ditimpa —
patch `courtHistoryCsv.py` pakai mode append atau path uji.
Replika verifikasi menjalankan pipeline dari directory kosong di `/tmp`, tak
menyentuh `courtHistory.csv` atau `OUTPUT/` proyek.

## DATASET

| File | Status | Bukti / alasan | Fix |
|---|---|---|---|
| `(FIX) Preprocessing & Labeling Dataset.ipynb` | ✅ `runnable` (dgn data Drive) | Paling siap; butuh 4 CSV + `entities_pn_all.xlsx` di Drive | Buat kernel `enWebmining`; export sel gdown |
| `Anotasi Data Perdata.ipynb` | ✅ `runnable` (gdown) | Butuh akses gdown URL | Kernel + delay |
| `Anotasi Pidana.ipynb` | ✅ `runnable` (gdown) | print accuracy literal; `SettingWithCopy` — tidak fatal | Kernel |
| `Convert Dataset.ipynb` | ⚠️ `run-true` cacat logika | Sel 17 → 124.704.912 baris artefak; teks↔label tak sejajar | Perbaiki logika konversi; lokalkan `all.json` |
| `Pre Processing Data Baru.ipynb` | ⚠️ `run-true` (rerun) | `df.loc(0)` sebagai fungsi → `TypeError` | `df.loc[0]` |
| `Pre Processing Data Lama.ipynb` | ⚠️ `run-true` data korup | `'tag': row['tag']` menyalin label seluruh dokumen ke tiap kalimat → `zip` truncate | Label per-token sejajar |
| `Pre Processing Data Merge.ipynb` | ❌ error | Kolom `text/text-tags` tanpa pembuat sel 20/30 → `KeyError`; `label_converter` dikomentari | Baca ulang alur kolom; terapkan mapping skema |
| `Pre Processing Data Perdata.ipynb` | ⚠️ `run-true` bug label | `'text-tags': row['text-tags']` (bug sejajar, sel 14) | Mapping label sejajar |
| `Salinan Anotasi Pidana.ipynb` | ❌ error | `generate_label` tanpa `return`; `anotasi()`, `countLabel`, `accuracy` tak ada → `NameError` | Definisikan fungsi; perbaiki `generate_label` |

Semua notebook Colab (`/content/drive/`), data komoditi 4 CSV + 2 xlsx bukan
produk zip — perlu lokalisasi saat dipindah ke deliverable.

## ML

| File | Status | Bukti / alasan | Fix |
|---|---|---|---|
| `ML1/POS Tag.ipynb` | ⚠️ `run-true` (berat) | Butuh `legal-dataset500.csv` + download embedding id-crawl + `UD_INDONESIAN` (~300MB) | Path lokal; kernel |
| `ML1/Flair_2_0.ipynb` | ⚠️ `run-true` (berat) | sama; flair terpasang sekarang | Path lokal |
| `ML1/make-prev-next.ipynb` | ❌ `blocked-license` | Input `pos200.csv` tidak ada di zip; nama output tidak konsisten | — |
| `ML1/NER-200-WithoutPos.ipynb` | ⚠️ `run-true` (terverifikasi) | CRF tereksekusi asli (0.96/0.56); replika subset 26 CRF fit 59.5s; CSV di folder sama bukan `../datasets/`; `to_dict('Record')`; `ffill` deprecated; `jcopml` tak butuh | path; `to_dict('records')`; `ffill()`; hapus `jcopml` |
| `ML1/NER-200-WithPos.ipynb` | ⚠️ `run-true` | Hasil 5 vector classifier tersimpan; sel CRF belum tereksekusi | sama seperti `-WithoutPos` |
| `ML1/NER-200-WithPosPrev.ipynb` | ⚠️ `run-true` | Hasil tersimpan; sel CRF belum | sama |
| `ML1/NER-200-WithPosNext.ipynb` | ⚠️ `run-true` | Hasil tersimpan; sel CRF belum | sama |
| `ML1/NER-200-WithPosPrevNext.ipynb` | ⚠️ `run-true` | Hasil tersimpan; sel CRF belum | sama |
| `ML2/POS tagging.ipynb` | ⚠️ `run-true` | Identik ML1 POS; copy `best-model.pt` ke Drive | Path |
| `ML2/FinalCode.ipynb` | ⚠️ `run-true` (parsial) | Drive (`data_all.csv`, `entities_all.xlsx`, `best-model.pt`, pkl); `applymap` dihapus pandas ≥2.1; `fillna` deprecated; fitur sel 93–94 tidak sinkron dgn model | Lokalkan data; `df.applymap`→`map`; samakan fitur train/inference |
| `ML2/Testing/600crf.ipynb` | ✅ `run-true` | `gdown` + `crfsuite` terpasang; file Drive (37,8–44,4 MB) harus live | kernel |
| `ML2/Testing/600crf-pos.ipynb` | ⚠️ `run-true` (`-pos` rentan) | Hasil tersimpan (macro-F1 0.60); `KeyError` bila Drive berubah | verifikasi skema kolom |
| `ML2/Testing/600crf-wordfrom.ipynb` | ✅ `run-true` | Hasil tersimpan (0.59) | kernel |
| `ML2/Testing/600crf-pos-wordfrom.ipynb` | ✅ `run-true` | Hasil tersimpan (0.59) | kernel |
| `ML2/Testing/600crf-prevnext.ipynb` | ✅ `run-true` | Hasil tersimpan (macro-F1 0.81, terbaik) | kernel |
| `ML2/Testing/600crf-pos-prevnext.ipynb` | ⚠️ `run-true` (`-pos` rentan) | Hasil tersimpan (0.80) | verifikasi skema kolom |
| `ML2/Testing/600crf-prevnext-wordfrom.ipynb` | ✅ `run-true` | Hasil tersimpan (0.80) | kernel |
| `ML2/Testing/600crf-pos-prevnext-wordfrom.ipynb` | ⚠️ `run-true` (`-pos` rentan) | Hasil tersimpan (0.81) | verifikasi skema kolom |

Hasil terverifikasi: prev/next fitur memberi lompatan macro-F1 0.59→0.81 (600crf).
`eli5` sudah terpasang untuk interpretasi.

## DL (bi-LSTM, TensorFlow)

| File | Status | Bukti / alasan |
|---|---|---|
| `bi-lstm-dataset-pidana-200.ipynb` | ❌ `blocked-license` | Data Kaggle + TensorFlow 2.13 (no wheel py3.14). Inspeksi: prosa; **CRF** `keras-contrib` gagal instal → softmax; `SentenceGetter` groupby `sentence` tanpa `doc` → konteks lintas-dok tercampur; `MultiLabelBinarizer` pada single-label → macro-F1 0.48 menyesatkan |
| `bi-lstm-dataset-pidana-cbow.ipynb` | ❌ `blocked-license` + `blocked-env` | TF tak ada wheel; **gensim tak ada wheel cp314** → build gagal. Inspeksi: `astype(int)` memotong vektor CBOW float32 → hasil "berhasil" tak dapat dipercaya |
| `Salinan bi-LSTM.ipynb` | ❌ `blocked-license` | TF 2.15; sel `model.fit`, metrik, report **tanpa output tersimpan** (notebook belum pernah tereksekusi penuh) |

Keputusan user: 3 notebook DL diverifikasi **by-inspection** (tanpa mengubah
source), dijalankan di Colab/Kaggle; untuk lapor ke dosen: env TF diperlukan.

## TRANSFORMER

| File | Status | Bukti / alasan | Fix |
|---|---|---|---|
| `ConvertDatasetToBERT.ipynb` | ⚠️ `run-true` | `str(row["tag"])` pada NaN → string `'nan'` bocor ke label (26 kelas, 1 baris); path Drive | Bersihkan NaN sebelum `str()`; lokalkan path |
| `Preprocessing ... Without O.ipynb` | ✅ `runnable` | Regex gagal filter baris `nan` → `nan` tetap lolos | Tambah filter `nan` |
| `Pretrain cahya_bert-base-indonesian-522M.ipynb` | ⚠️ `run-true` (berat) | transformers terpasang; butuh download model ~1.3GB; `num_labels=26` (termasuk `nan`); acc didominasi O; loss double-count ±2× | Clean `nan`; ukur macro metrik |
| `Pretrain cahya_roberta-base-indonesian-522M.ipynb` | ⚠️ `run-true` | Sama; tes acc 0.975 | Sama |
| `Pretrain indolem_indobert-base-uncased.ipynb` | ⚠️ `run-true` | Sama; paling stabil (0.982) | Sama |
| `Pretrain Venkatesh...-NER-ind.ipynb` | ⚠️ `run-true` | Sama + overfit epoch5 (tes 0.963); `ignore_mismatched_sizes=True` | +early stopping |
| `Uji Coba Pengindexan Database NER.ipynb` | ✅ `run-true` (terverifikasi) | **Replika lokal berhasil (2026-09-13)**: model 522M jalan di GPU GTX 1650; 31 teks → SQLite in-memory 470 baris entity; V1/V2 query bekerja. Peringatan `classifier` random-init = head NER tak fine-tune → prediksi label acak; notebook memang uji SQLite indexing, bukan kualitas NER | — |

Isu dominan seluruh TRANSFORMER: label `'nan'` bocor dari konversi → 26th
class ikut dilatih. Bersihkan sebelum training.

## Verifikator yang Jalan Lokal (batch ringan)

1. RULE-BASED: **replika jalan** — fix `entityGenerator2`→3 & `nomor`→`baris`
   (plus `errors='ignore'` + guard `eNomor`); 14 txt → CSV 15 kolom, 14 nomor
   match data asli ✓
2. ML1 `NER-200-WithoutPos.ipynb`: path CSV lokal + fix `to_dict`/`fillna`; CRF ✓
3. ML2 `Testing/600crf-prevnext.ipynb`: **replika jalan** (`gdown` ID file; 7.985/3.287 fragment fit 156 s; acc 0.9712 / macro-F1 0.8065) ✓
4. TRANSFORMER `ConvertDatasetToBERT.ipynb` + `Preprocessing Without O`: path lokal ✓
5. `Uji Coba Pengindexan Database NER.ipynb`: **replika jalan** (GPU, 470 entity SQLite) ✓