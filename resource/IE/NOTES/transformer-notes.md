# Catatan Folder TRANSFORMER

Catatan pembacaan `resource/IE/TRANSFORMER/`. Dibaca read-only; file tidak diubah.

## Inventori (7 notebook + 1 CSV)

| File | Peran |
|---|---|
| ConvertDatasetToBERT.ipynb | Konversi token-level → format BERT per kalimat |
| Preprocessing LEGALDataset Without O labels.ipynb | Buang kalimat semua-O |
| Pretrain cahya_bert-base-indonesian-522M.ipynb | Fine-tune BERT |
| Pretrain cahya_roberta-base-indonesian-522M.ipynb | Fine-tune RoBERTa |
| Pretrain Venkatesh4342_xlm-roberta-base-NER-ind.ipynb | Fine-tune XLM-RoBERTa NER-ind |
| Pretrain indolem_indobert-base-uncased.ipynb | Fine-tune IndoBERT |
| Uji Coba Pengindexan Database NER.ipynb | Uji SQLite indexing (model mentah) |
| LEGALBERTNER-POS-PREV-NEXT-200.csv | Data hasil konversi (24.515 kalimat, 2 kolom) |

## Alur Data

```
LEGALNER-POS-PREV-NEXT-200.csv (1.048.575 token / 24.515 kalimat / 107 doc)  [folder DL]
  → ConvertDatasetToBERT.ipynb → LEGALBERTNER-POS-PREV-NEXT-200.csv (text, labels)
  → Preprocessing Without O    → 7.954 kalimat tersisa (dari 24.515)
  → Pretrain ×4 (hanya subset 1.000 baris pertama! 80/10/10 split)
```

## ConvertDatasetToBERT.ipynb
- Input `/content/drive/MyDrive/IE-ML/NEW-DATASET/LEGALNER-POS-PREV-NEXT-200.csv`
  (`str(row["word"])` + `str(row["tag"])` digabung spasi per kalimat)
- Output `/content/drive/MyDrive/BERT/LEGALBERTNER-POS-PREV-NEXT-200.csv`
- **BUG KRITIS**: `str(row["tag"])` pada nilai kosong/NaN → string literal **`'nan'`**
  bocor ke dataset hasil (1 baris mengandung `nan`); DtypeWarning (doc campur teks/NaN);
  stream output besar terpotong

## LEGALBERTNER-POS-PREV-NEXT-200.csv
- 24.515 baris data × 2 kolom: `text`, `labels`
- 26 label unik = 25 tag + **`nan`** (pencemaran)
- 16.561 baris hanya `O`; **7.954 baris** mengandung ≥1 label non-O (persis hasil filter)

## Preprocessing LEGALDataset Without O labels.ipynb
- Regex `\b(?!O\b)\w+\b` utk deteksi kalimat berisi label non-O → `df.drop` sisanya
- **24.515 → 7.954 baris**, reset index
- **BUG**: `nan` lolos pola `\w+` → baris berlabel `nan` TIDAK terfilter
- Output `LegalNER NEW.csv` (di `/content/`, tidak ikut zip)

## 4 Notebook Pretrain (struktur bersama)

- `pip install transformers` (4.33.2) + `dataloader` (paket tak relevan)
- Baca `LEGALBERTNER...csv` → split `df[0:1000]` 80/10/10 (`random_state=42`)
- `align_label` (word_ids; -100 utk special & subword), `DataSequence`/`DataLoader`
- **Konfigurasi**: BATCH 2; EPOCHS 5; LR **5e-3 SGD**; max_length 512; padding max; `label_all_tokens=False`;
  **num_labels=26 (termasuk `nan`)**
- Metrik = akurasi token (non-`-100`) saja → **didominasi O**, angka terlalu optimistis

### Hasil (acc test)

| Model | E1→E5 (loss/acc/val_acc) | Test Acc | Catatan |
|---|---|---|---|
| cahya/bert-base-indonesian-522M | 0.209/0.961/0.967 → 0.037/0.992/0.985 | **0.985** | head baru |
| indolem/indobert-base-uncased | 0.244/0.958/0.971 → 0.043/0.990/0.986 | **0.982** | paling stabil |
| cahya/roberta-base-indonesian-522M | 0.242/0.955/0.964 → 0.054/0.989/0.977 | **0.975** | terendah ke-2 |
| Venkatesh xlm-roberta-base-NER-ind | 0.252/0.959/0.972 → E5 **0.151/0.972/0.965** | **0.963** | **overfit epoch 5**; head 10 kelas dibuang (`ignore_mismatched_sizes=True`) |

### Bug bersama
1. **Label `nan` jadi kelas ke-26** (`'nan': 25`) — pencemaran dari ConvertDatasetToBERT,
   ikut dilatih di semua pretrain
2. Akurasi hanya atas token ≠ -100 & didominasi O → 0.96–0.99 menyesatkan utk NER
3. `total_loss_train += loss.item()` **di dalam loop per-sampel** → loss ter-inflasi ~2×
4. Loop ganda `for i in range(logits.shape[0])` (batch=2) redundan
5. `evaluate_one_text` sering menghasilkan rangkaian label identik panjang (bias kelas)
6. Fine-tune subset kecil (1.000 kalimat, 800 train) → bukan ukuran performa final
7. Venkatesh overfit epoch 5 → butuh early stopping / LR lebih kecil

## Uji Coba Pengindexan Database NER.ipynb
- Transformers 4.35.0; SQLite **in-memory**; tabel `texts`+`entities` (FK)
- Model `AutoModelForTokenClassification.from_pretrained("cahya/bert-base-indonesian-522M")`
  → **model MENTAH (tanpa fine-tune)** → prediksi `LABEL_0/LABEL_1` acak, bukan NER hukum
- ~50 teks umum (bukan teks hukum); subword/special token ikut terindeks
- V1 `.lower()` vs token mentah → query "Restoran" tidak berhasil; V2 copy per token → duplikat
- Kesimpulan: ini uji fungsional indexing, BUKAN uji model NER nyata

## Run-Readiness

| Item | Status |
|---|---|
| ConvertDatasetToBERT | ⚠️ jalan; perbaiki `str(tag)`/`str(word)` NaN agar tidak bocor `nan` |
| Preprocessing Without O | ✅ jalan; perbaiki regex agar `nan` ikut difilter |
| Pretrain 4 model | ⚠️ perlu transformers + dataset; subset 1000; instal crash-probable di Python baru |
| Uji Pengindexan DB NER | ✅ jalan (Model mentah, hasil tak bermakna utk NER) |

Catatan: seluruh alur tight-coupled dengan `nan` yang bocor dari konversi — isu
data paling penting utk dibereskan (bersihkan label `nan` sebelum training).