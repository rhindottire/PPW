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
- Deteksi bahasa per kalimat (id 3.868 dari 5.227 kalimat = **74,0%**,
  ms 10,9%, en 8,5%); `langid` per kata terbukti tidak andal sehingga tidak
  dipakai dan prosa Inggris asli dipertahankan.
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
  disimpan di `data/Web-Mining/` dalam tiga berkas: `tfidf_sparse.npz`,
  `tfidf_features.txt`, `tfidf_docs.csv`.
- **PCA** dua komponen mempertahankan **7,35%** varians; ambang kumulatif
  50/80/90/95% tercapai pada 45/109/140/160 komponen (semuanya di bawah 500),
  sehingga dipilih **140 komponen (90%)** setara reduksi **97,3%**.
- Angka komponen di tugas ini **tidak sebanding** dengan Book 3. Di sini PCA
  dihitung pada seluruh 200 dokumen dengan kosakata 5.200 term, sedangkan Book 3
  memakai TruncatedSVD pada 160 dokumen latih dengan 3.588 term. Algoritma,
  jumlah dokumen, dan kosakata ketiganya berbeda, sehingga 140 dan 118
  komponen sama-sama sah untuk konteksnya. Tugas ini tidak membagi data karena
  tujuannya menyiapkan vektor, bukan menilai model; pemisahan data baru relevan
  di Book 3.
- Refleksi penutup mencatat enam kelemahan pustaka (`langid`, Sastrawi,
  `sklearn`, `transformers`, PCA) beserta penyempurnaan yang diterapkan pada
  tiap tahap pengolahan.

Proses pengerjaan: [Book 2](book/book-2.ipynb)

## Book 3 — Data Classification

- **200 berita** (100 sport, 100 finance) bersih dan berkelas seimbang; teks
  finance lebih beragam panjangnya (median 2.501, maks 14.106 karakter)
  dibanding sport (median 2.409, maks 5.809).
- Data dibagi berstrata lebih dulu menjadi **160 latih dan 40 uji**, sebelum
  TF-IDF maupun SVD dijalankan, supaya dokumen uji tidak ikut memengaruhi model.
- TF-IDF pada data latih menghasilkan **3.588 term** (`min_df=2`); dimensi
  diturunkan dengan TruncatedSVD, dan ambang varians kumulatif
  20/50/80/90/95% tercapai pada **10/40/93/118/135 komponen**.
- Dipilih **118 komponen (90%)**, setara pengurangan dimensi **96,7%**, lalu
  vektorisasi dan SVD dibungkus `Pipeline` agar di-fit ulang di tiap lipatan.
- **Naive Bayes Gaussian unggul tipis**: akurasi **0,994 ± 0,019**, precision
  0,989 ± 0,033, recall 1,000 ± 0,000, dan f1 0,994 ± 0,018 pada 10-fold
  cross-validation.
- **kNN terbaik pada k=2** (akurasi CV-5 1,000) dengan akurasi **0,988 ± 0,025**,
  precision 0,978 ± 0,044, recall 1,000 ± 0,000, dan f1 0,988 ± 0,024.
- Pada 40 dokumen uji, akurasi **0,950** dengan dua kesalahan satu arah: dua
  berita finance diprediksi sport (precision finance 1,000, sport 0,909).
- `StandardScaler` terbukti merusak kNN tanpa menyentuh Naive Bayes: kNN turun
  dari 0,988 ke **0,838 ± 0,080**, sedangkan Naive Bayes tetap 0,994. Standar
  deviasi komponen SVD berbeda 17,9 kali, sehingga menyamaratakan semuanya
  memberi bobot yang sama kepada komponen noise.
- Kesimpulan: kedua model mencapai recall sempurna, dan selisihnya hanya pada
  dokumen yang tumpang tindih. Versi sebelumnya melaporkan 1,000 karena vektorisasi
  dijalankan sebelum pembagian data; perbaikannya tidak mengubah pemenang, tetapi
  membuat angkanya dapat dipertanggungjawabkan.

Proses pengerjaan: [Book 3](book/book-3.ipynb)

## Book 4 — Word Embedding

- **200 berita** (100 sport, 100 finance) diklasifikasikan dari vektor
  skip-gram **Word2Vec** dengan **Gaussian Naive Bayes**, tanpa reduksi dimensi.
- Representasi dokumen memakai **mean pooling** vektor kata; model skip-gram
  100 dimensi dibangun pada data latih saja (160 dokumen, kosakata **1.783**).
- Daftar slang tidak ditebak: dari 18 kandidat hasil hitung frekuensi, **12
  diterjemahkan** dan **6 ditahan**. `gas` bermakna ganda dan `lo` ternyata
  bagian nama orang, keduanya dibiarkan apa adanya.
- **16 kombinasi sakelar** stopword, tanda baca, slang, dan stemming diuji ulang
  masing-masing dengan modelnya sendiri: akurasi uji bergerak **0,850–1,000**,
  dan konfigurasi bawaan memberi **0,975** pada 40 dokumen uji.
- Arah tiap preprocessing berbeda: membuang stopword menaikkan akurasi
  (**0,991** berbanding 0,953), demikian pula stemming (**0,988** berbanding
  0,956) dan membakukan slang (**0,981** berbanding 0,962). Tanda baca justru
  sebaliknya, membuangnya menurunkan akurasi (**0,959** berbanding 0,984),
  sehingga tanda baca dibiarkan.
- Urutan per kombinasi tidak lurus: **7 kombinasi** mencapai **1,000**, tanpa
  semua langkah berada di **0,950**, sedangkan yang terendah justru kombinasi
  yang hanya membuang tanda baca (**0,850**). Selisih ini tipis karena data uji
  hanya 40 berita.
- **Skip-gram** lebih cocok daripada CBOW di korpus ini: skip-gram bertahan di
  **0,975–1,000**, sedangkan CBOW turun ke **0,700** pada `window=2` dan baru
  naik ke **0,950** saat `window=5`. Skip-gram sekitar dua kali lebih lambat
  (0,85–1,39 detik berbanding 0,46–0,50 detik), tetapi selisih itu tidak berarti
  pada 160 dokumen latih.
- **Peta vektor** dua dimensi memakai PCA hanya untuk keperluan gambar, bukan
  untuk model: kata kunci olahraga dan pasar modal dipetakan bersama, dan tiap
  dokumen digambar sebagai satu titik berwarna sesuai labelnya.
- Stemming memangkas rata-rata kata unik dari sekitar **2.120** menjadi
  **1.810**.
- Pembagian data dilakukan **sebelum pelatihan Word2Vec** tiap konfigurasi agar
  tidak ada kebocoran informasi dari data uji.

Proses pengerjaan: [Book 4](book/book-4.ipynb)

## Book 5 — Model Deployment

- Empat artefak pemenang dikemas ke folder distribusi `deploy/models/`:
  `word2vec.model` (1.656.252 byte), `protected.json` (12.981 byte),
  `gnb.joblib` (2.415 byte), dan `labels.json` (20 byte).
- Aplikasi memutar transformasi yang identik dengan data latih lewat
  `deploy/serve.py`: normalisasi ascii, artefak format, aturan angka, pemecahan
  kalimat, lalu lowercasing dan normalisasi slang dengan proteksi nama diri;
  token di luar kosakata skip-gram dilewati dan vektor sisanya dirata-rata
  sebelum masuk estimator naive bayes.
- Dua contoh cepat: kalimat finance diklasifikasikan finance dengan skor
  **1,000** (11 token, 9 dikenal kosakata), dan kalimat sport diklasifikasikan
  sport dengan skor **1,000** (13 token, 10 dikenal).
- **Parity check** pada 40 dokumen uji yang sama dengan Modeling: akurasi lewat
  pipeline aplikasi **39/40 = 0,975**, setara hasil validasi, sehingga kemasan
  tidak menggeser prediksi.
- Aplikasi dipasang sebagai **Hugging Face Space** `Rhindottire/News-Classifier`
  memakai Gradio pada perangkat **ZeroGPU** (Python 3.12) dan tercatat
  **RUNNING**: dapat diakses di `rhindottire-news-classifier.hf.space`.
- Cara pakai: tempel **link berita** (isi halaman diambil dengan trafilatura,
  jeda satu detik, user agent jujur, berhenti di 403/429) atau **teks berita**
  langsung; jawabannya kategori **sport/finance**, skor kedua kelas, dan
  ringkasan kalimat, token, serta cakupan kosakata.

Proses pengerjaan: [Book 5](book/book-5.ipynb)
