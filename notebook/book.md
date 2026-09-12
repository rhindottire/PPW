# Book

Hasil langsung dari setiap tugas. Proses pengerjaan masing-masing tugas
tersedia di bawah ini.

## Book 1 — Dataset Berita detik.com

- **200 artikel** dari detik.com: 100 sport, 100 finance.
- Kolom: `id`, `isi_berita`, `label`, `url`.
- Tidak ada nilai kosong, tidak ada baris maupun URL ganda, dan `id` terisi
  lengkap 1–200 sehingga dataset siap dipakai.

Proses pengerjaan: [Book 1](book/book-1.ipynb)

## Book 2 — Preprocessing Teks Berita

- **200 dokumen** (100 sport, 100 finance) sehat: tanpa nilai kosong, tanpa
  baris atau URL ganda, `id` lengkap 1–200.
- **6 artikel** memuat karakter non-ASCII (aksen pada nama, emoji dalam
  kutipan tweet) dinormalisasi sebelum pembersihan.
- Artefak format disisihkan utuh sebelum simbol/angka dibuang: 5 URL,
  285 mata uang (`Rp`, `US$`), 4.073 kata komposit berangka (`3x3`, `U-18`,
  `Grup A`, ...), dan 126 angka Romawi.
- Deteksi bahasa per kalimat (5.227 kalimat: id 74,0%, ms 10,9%, en 8,5%);
  prosa Inggris asli hanya **4 kalimat** pada 2 artikel dan dipertahankan
  `langid` per kata terbukti tidak andal sehingga tidak dipakai.
- **3.091 nama diri unik** dilindungi dari normalisasi lewat bukti kapitalisasi
  di tengah kalimat, termasuk partikel pada nama multi-kata.
- Kata tidak baku sejati yang dibakukan: **17 kata / 72 kemunculan**; 21 token
  lain ditahan karena ternyata nama atau singkatan (misal `mbg`, `sma`, `pass`).
- Korpus bersih: **70.645 token / 7.399 kata unik**.
- Representasi **TF-IDF 200 × 7.399** disimpan di `data/` dalam tiga berkas:
  `tfidf_sparse.npz`, `tfidf_features.txt`, `tfidf_docs.csv`.
- **PCA dua komponen** mempertahankan sekitar **6,7%** varians total dan
  menunjukkan keterpisahan awal antar label.

Proses pengerjaan: [Book 2](book/book-2.ipynb)

## Book 3