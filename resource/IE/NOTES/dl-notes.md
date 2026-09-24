# Catatan Folder DL

Catatan pembacaan `resource/IE/DL/`. Dibaca read-only; file tidak diubah.

## Inventori
- `bi-lstm-dataset-pidana-200.ipynb` — Bi-LSTM NER 200 dok pidana
- `bi-lstm-dataset-pidana-cbow.ipynb` — Bi-LSTM + representasi CBOW (Word2Vec), 500 dok
- `Salinan bi-LSTM.ipynb` — Bi-LSTM dataset gabungan 1100 dok (Merge)
- `LEGALNER-POS-PREV-NEXT-200.csv` (29,7 MB) — dataset token (107 doc, 24.515 kalimat)

## Dataset `LEGALNER-POS-PREV-NEXT-200.csv`
- 1.048.575 baris + header, 7 kolom: `doc, sentence, word, pos, prev, next, tag`
- **107 doc unik**, nilai `doc` = **hash MD5** (bukan `doc: 1..200`)
- 24.515 kalimat unik (= jumlah baris CSV TRANSFORMER, jembatan awal alur)
- `doc`/`sentence` hanya terisi di baris pertama blok → butuh `fillna(method='ffill')` (yang deprecated di pandas baru)
- `tag` ada 1 nilai kosong `''` (label NaN)
- Distribusi tag: O 93%; I_DEFN 25.283; I_ARTV 16.441; B_DEFN 13.034; I_VERN 6.607; sisanya kecil
- 18 baris `pos` rusak (campuran token, mis. `'PROPN> _ <PUNCT> IV <NUM'`)

## 1. bi-lstm-dataset-pidana-200.ipynb

- **Model**: Embedding → Dropout → BiLSTM 100 → TimeDistributed Dense softmax
  (CRF dari `keras-contrib` di-import TAPI gagal instal — layer akhir softmax)
- **Env**: TensorFlow 2.13.0; tensorflow-addons 0.23.0; sklearn; pandas; **latin1** baca CSV
- **Data**: Kaggle `/kaggle/input/dataset-pos-pidana-baru/DatasetPos-Pidana200.csv`
  1.235.507 baris × 7 kolom; 200 dok, 25 tag
- **Preprocess**: lowercase; angka → `<123>`→`<XXX>`; `fillna(method="ffill")`;
  buang POS `PUNCT, PRON, CCONJ, ADP, AUX, DET` + 6 nilai pos rusak → sisa 827.485 tag O;
  vocab 15.812; `SentenceGetter`; `MAX_LEN=10` padding post; split 90/10 tanpa shuffle
  (21.245/2.361 kalimat)
- **Konfigurasi**: BATCH 64, EPOCHS 100, EMBEDDING 100; rmsprop, categorical_crossentropy;
  total params **1.747.226**
- **Hasil**: loss 0.2529→0.0037; val_acc 0.9817→0.9946; evaluasi **P 0.469 / R 0.507 / F1 0.483**
  (macro), acc 0.99; 9 kelas entitas **0 support** di test (UndefinedMetricWarning);
  `MultiLabelBinarizer` (multi-label) dipakai utk masalah single-label → macro-metrik menyesatkan

## 2. bi-lstm-dataset-pidana-cbow.ipynb

- **Model**: Bi-LSTM 100 + input vektor **CBOW Word2Vec 10-d** (tanpa layer Embedding)
- **Env**: TensorFlow 2.13.0; gensim; keras; sklearn; pydot/graphviz; torch (simpan)
- **Data**: `Dataset-Pidana500.csv` — **6 kolom (TANPA pos)**, 3.296.250 baris, 500 dok, 65.700 kalimat
- **Preprocess**: `Word2Vec(vector_size=10, window=5, min_count=1, sg=0)` dari token kalimat;
  vocab 39.500; **MAX_LEN=100**; split 80/20 (52.560/13.140 kalimat)
- **Konfigurasi**: BATCH 64, EPOCHS 100; rmsprop; params hanya **93.624**
- **Hasil**: val_acc 0.9913→0.9937; **P 0.679 / R 0.723 / F1 0.676** (macro), acc 0.99
  (1.314.000 token); terbaik O 0.99, B_VERN 0.88, I_VERN 0.88, B_REGI 0.85; terburuk I_CRIA F1 0.01
- **BUG KRITIS**: `model.fit(np.array(X_tr).astype(int), ...)` — `X_tr` berisi vektor CBOW
  **float32**; `astype(int)` **memotong semua nilai jadi bilangan bulat** (embedding rusak,
  mayoritas 0). "Berhasil" hanya karena label didominasi O → angka tidak dapat dipercaya

## 3. Salinan bi-LSTM.ipynb

- **Model**: identik (softmax BiLSTM), dataset **1100 dok** gabungan
- **Env**: TensorFlow 2.15.0; tensorflow-addons terinstal sukses (Colab)
- **Data**: `/content/drive/MyDrive/NER nlp/Dataset/Dataset-Merge.csv` (latin1):
  7.662.678 × 6 kolom, 1100 dok, 140.394 kalimat, 25 tag
- **Preprocess**: lowercase+angka→X+ffill; **kalimat all-O dihapus** (7.662.678 → 7.627.482);
  vocab 69.608; MAX_LEN 10; split 90/10 (120.727/13.415 kalimat)
- **Hasil**: **TIDAK ADA** — sel `model.fit` (32), plot (34), metrik (44), classification report (47)
  **tidak punya output tersimpan** (notebook tak pernah tereksekusi penuh)
- Catatan penulis di MD 48: kekhawatiran dominasi O di matriks (belum ditangani kode)

## Bug Umum Ketiga Notebook

1. **`keras-contrib` gagal instal** (DNS github) → CRF tak pernah terpakai; layer akhir = softmax
2. **`SentenceGetter` groupby `sentence` TANPA `doc`** → kalimat bernomor sama lintas dokumen
   (contoh `000001` di doc 1 & doc 200) digabung jadi satu sekuens → konteks lintas-doc tercampur
3. **`torch.save(model_keras, 'model-*.pth')`** → model Keras disimpan dengan ekstensi `.pth` (menyesatkan)
4. `fillna(method='ffill')` deprecated di pandas ≥2.0
5. Metrik macro via `MultiLabelBinarizer` + `UndefinedMetricWarning` (kelas minoritas 0 support)
6. Kekhawatiran dominasi O tercatat SS cara resolve

## Run-Readiness

| Notebook | Status | Syarat |
|---|---|---|
| bi-lstm pidana-200 | ⚠️ sebagian | file Kaggle DatasetPos-Pidana200.csv (tidak ada di folder); TensorFlow env; kernel enWebmining |
| bi-lstm cbow | ⚠️ sebagian (untuk uji coba) | perbaiki `astype(int)` → float; Dataset-Pidana500.csv tak ada di folder |
| Salinan bi-LSTM | ❌ belum tereksekusi | Dataset-Merge.csv di Drive; butuh train+mengukur |

Catatan: file CSV yang dibutuhkan belum tentu tersedia lokal (beberapa di Kaggle/Drive).
Untung uji ulang perlu verifikasi ketersediaan data.