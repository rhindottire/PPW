# Orange Workflow

Verifikasi visual dari tugas klasifikasi berita (Tugas 3). Notebook `Book 3`
menjalankan pipa yang sama dengan kode Python; di sini rangkaian itu dibangun
kembali lewat antarmuka grafis Orange Data Mining agar setiap tahap
(preprocessing, reduksi dimensi, model, evaluasi) bisa diamati sekaligus.

## Pipeline Orange

Workflow dibuka dari file `orange-task3/task3.ows` dan mengikuti urutan:

- **File** — membaca `data/Web-Mining/crawling_detik.csv` (200 berita; 100
  sport, 100 finance).
- **Bag of Words (TF-IDF)** — teks berita diubah menjadi representasi vektor
  dengan pembobotan TF-IDF (term frequency, global IDF, normalisasi L2).
- **PCA** — dimensi vektor 4.092 diturunkan dengan mempertahankan 90 persen
  varians (141 komponen).
- **Naive Bayes dan kNN** — dua model klasifikasi dilatih dari data tereduksi;
  kNN memakai nilai k = 2.
- **Test and Score** — akurasi kedua model diukur lewat *cross-validation*.
- **Confusion Matrix** — kesalahan klasifikasi dilihat per kelas.

Setelah file dipilih pada widget File, seluruh pipa berjalan otomatis berkat
modus *auto commit* yang aktif pada Bag of Words, PCA, dan kedua model.

## Screenshots

Bagian ini diisi dengan tangkapan layar tiap widget utama hasil eksekusi
workflow di Orange.

Data berita bersumber dari hasil crawler detik.com di
`data/Web-Mining/crawling_detik.csv`.