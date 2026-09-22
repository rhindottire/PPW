# Book

Hasil langsung dari setiap tugas. Proses pengerjaan masing-masing tugas
tersedia di bawah ini.

## Book 1 — News Dataset

- **200 artikel** dari detik.com: 100 sport, 100 finance.
- Kolom: `id`, `isi_berita`, `label`, `url`.
- Tidak ada nilai kosong, tidak ada baris maupun URL ganda, dan `id` terisi
  lengkap 1–200 sehingga dataset siap dipakai.

Proses pengerjaan: [Book 1](book/book-1.ipynb)

## Book 2 — Text Preprocessing

- **200 dokumen** (100 sport, 100 finance) sehat: tanpa nilai kosong, tanpa
  baris atau URL ganda, `id` lengkap 1–200.
- **6 artikel** memuat karakter non-ASCII (aksen pada nama, emoji dalam
  kutipan tweet) dinormalisasi sebelum pembersihan.
- Token naif **72.138 / 7.544 unik**: 425 token satu huruf dan 2.878 token dua
  huruf; setelah proteksi dan pemotongan cukup huruf menjadi **71.234 / 7.500**
  dengan token satu huruf hilang seluruhnya.
- Artefak format disisihkan utuh sebelum simbol/angka dibuang: **5 URL**,
  **285 mata uang** (`Rp`, `US$`), **4.073 komposit berangka** (`3x3`, `U-18`,
  `76ers`, `GA-604`), dan **126 angka Romawi**.
- Deteksi bahasa per kalimat (5.227 kalimat: **id 74,0%**, ms 10,9%,
  en 8,5%); `langid` per kata terbukti tidak andal sehingga tidak dipakai dan
  prosa Inggris asli dipertahankan.
- **3.091 nama diri unik** (14.332 kemunculan) dilindungi dari normalisasi
  lewat bukti kapitalisasi di tengah kalimat.
- Kata tidak baku sejati yang dibakukan: **17 kata / 72 kemunculan**; 21 token
  lain ditahan karena nama atau singkatan (misal `mbg`, `sma`, `dunk`, `fans`).
- Sebelum stopword dibuang, **70.645 token** dilabeli kategori gramatikal lewat
  model RoBERTa bahasa Indonesia (`w11wo/indonesian-roberta-base-posp-tagger`);
  kategori terbanyak nomina umum **NNO 24.638**, nama diri **NNP 11.490**,
  preposisi **PPO 6.981**, verba transitif **VBT 3.763**, dan adjektiva
  **ADJ 3.522**.
- Stopword Sastrawi dibuang: **16.886 kemunculan (109 jenis)**; korpus menjadi
  **53.759 token / 7.290 unik**.
- Stemming Sastrawi mengecilkan kosakata menjadi **5.200 kata unik**;
  **531 kandidat** nama diri dengan kapital dominan dilindungi sehingga
  `Perbasi`, `Bali`, dan `Maluku` tidak runtuh.
- Kata unik per label: **sport 3.318**, **finance 3.141**, dipakai kedua label
  1.259.
- Dataset siap model berupa **TF-IDF 200 × 5.200** (29.089 entri bukan nol)
  disimpan di `data/` dalam tiga berkas: `tfidf_sparse.npz`,
  `tfidf_features.txt`, `tfidf_docs.csv`.
- **PCA** dua komponen mempertahankan **7,35%** varians; ambang kumulatif
  50/80/90/95% tercapai pada 45/109/140/160 komponen (semuanya di bawah 500),
  sehingga dipilih **140 komponen (90%)** setara reduksi **97,3%**.
- Refleksi penutup mencatat enam kelemahan pustaka (`langid`, Sastrawi,
  `sklearn`, `transformers`, PCA) beserta penyempurnaan yang diterapkan pada
  tiap tahap pengolahan.

Proses pengerjaan: [Book 2](book/book-2.ipynb)

## Book 3