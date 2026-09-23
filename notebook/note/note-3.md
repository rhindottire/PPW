# Orange Data Mining

Materi kuliah ketiga memulai perjalanan ke machine learning: setelah teks
direpresentasikan sebagai vektor, data siap diolah menjadi model klasifikasi.
Praktikum ini menggunakan **Orange** — aplikasi data mining visual berbasis
Python yang menyusun alur kerja dari widget-widget yang saling terhubung.
Instruksi tugas merangkum empat langkah: import data, PCA, klasifikasi dengan
Naive Bayes / kNN, lalu test and score.

## Data Import

Langkah pertama setiap eksperimen adalah memuat data ke dalam kanvas Orange.
Widget *File* membaca berkas CSV dan menafsirkan isinya menjadi tiga bagian:

- **feature** — kolom yang dipakai sebagai masukan model,
- **meta** — informasi pelengkap yang tidak ikut dipelajari,
- **class** — satu kolom target yang menjadi label yang hendak diprediksi.

Pada materi ini datanya berita hasil crawl: kolom teks berita menjadi fitur,
sedangkan kolom `label` (sport / finance) menjadi *class*. Sebelum dipakai,
data diperiksa dulu: jumlah baris, keseimbangan antar kelas, dan karakter isi
teks. Data yang timpang kelasnya akan membuat evaluasi menyesatkan, sehingga
pemeriksaan awal ini wajib.

## Principal Component Analysis

Teks yang diubah menjadi vektor berjumlah fitur sangat besar (ribuan term),
sementara jumlah dokumen hanya ratusan. Kurva *explained variance* dari PCA
menunjukkan berapa komponen yang cukup untuk mewakili hampir semua varians.

Prinsipnya sama dengan yang dipelajari pada materi preprocessing: PCA mencari
arah kombinasi linier yang menampung variansi terbesar, setiap komponen saling
ortogonal, dan varians menurun di tiap komponen berikutnya. Untuk representasi
teks yang sparse, penguraian dilakukan lewat dekomposisi nilai singular
sehingga data tetap ringkas tanpa perlu dijejali nol.

Hasil reduksi membuat data berdimensi kecil dan terpusat, yang sangat
membantu metode berbasis jarak seperti kNN serta model probabilistik. Keputusan
jumlah komponen didasarkan pada kurva varians yang muncul saat data dijalankan,
bukan angka yang ditetapkan di awal.

## Classification Models

### Naive Bayes

Naive Bayes menerapkan aturan Bayes untuk memilih kelas dengan peluang
tertinggi:

```
P(kelas | fitur) ∝ P(kelas) × P(fitur | kelas)
```

Asumsinya sederhana: setiap fitur dianggap independen terhadap fitur lain,
itulah kata "naive". Meski asumsi ini jarang benar pada teks, model tetap cepat
dan sering bekerja baik untuk klasifikasi dokumen. Pada komponen PCA keluaran
PCA yang bersifat kontinu, digunakan varian Gaussian yang menganggap setiap
komponen menyebar normal.

### k-Nearest Neighbors

kNN mengklasifikasikan dokumen baru dari mayoritas label `k` dokumen terdekat
berdasarkan ukuran jarak (umumnya jarak Euclidean). Model tidak belajar
parameter; ia menyimpan seluruh data latih dan menghitung jarak saat prediksi.
Pilihan nilai `k` penting: `k` kecil peka terhadap noise, `k` besar bisa
menghaluskan batas kelas terlalu jauh. Bila fitur berskala berbeda-beda,
data distandarkan dulu agar jarak tidak didominasi satu dimensi.

## Test and Score

Widget *Test and Score* mengevaluasi model dengan skema yang dipilih, biasanya
**cross-validation**: data dibagi menjadi `k` lipatan, model dilatih pada
`k-1` lipatan dan diuji pada lipatan tersisa, berulang hingga tiap lipatan
pernah diuji. Hasil setiap lipatan dirata-rata sehingga angka evaluasi tidak
bergantung pada satu pembagian data acak.

Metrik yang dihitung:

```
accuracy  = benar / total
precision = benar-total / diprediksi-positif
recall    = benar-total / aktual-positif
f1        = 2 × precision × recall / (precision + recall)
```

Karena label berjumlah dua kelas, precision dan recall untuk kelas yang sama
bisa (dan sebaiknya) diamati bersama. Tabel hasil perbandingan Naive Bayes dan
kNN menentukan model mana yang paling layak dipakai berikutnya.