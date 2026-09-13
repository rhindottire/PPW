# Word Representation & Text Preprocessing

Algoritma NLP tidak bisa membaca teks mentah secara langsung; kata-kata harus
diubah menjadi angka. Materi kuliah kedua membahas cara merepresentasikan kata
beserta metode preprocessing teks yang menjadi dasar tugas praktikum.

## Word Representation (Word Encoding)

### One-Hot Encoding

Satu kata diubah menjadi vektor berdimensi N, dengan N = ukuran kosakata di
dalam korpus. Vektor berisi nol di semua posisi kecuali satu nilai (hot) yang
mewakili kata tersebut.

Contoh korpus 6 kata unik: `i`, `love`, `playing`, `football`, `indians`,
`cricket`. Vektor untuk `football`:

| Kata | Indeks | Vektor (N = 6) |
| --- | --- | --- |
| football | 3 | [0, 0, 0, 1, 0, 0] |

Kelebihan: sederhana dan mudah diimplementasikan. Kekurangan:

- **Boros memori** — kosakata besar menghasilkan vektor yang hampir semua
  nilainya nol (sparse).
- **Curse of dimensionality** — dimensi bertambah seiring bertambahnya kata.
- **Tanpa informasi semantik** — setiap kata dianggap ortogonal, jadi
  `football` dan `soccer` dianggap sama jauhnya.

### Bag-of-Words (BOW)

Representasi yang menghitung frekuensi setiap kata di dalam dokumen, mengabaikan
tata bahasa dan urutan kata. Contoh untuk dua dokumen dengan 6 kata unik:

- Doc 1 "I love playing football." → `[1, 1, 1, 1, 0, 0]`
- Doc 2 "Indians love playing Cricket." → `[0, 1, 1, 0, 1, 1]`

Kelemahan BOW: urutan kata hilang (`not good` sama dengan `good`), kata umum
mendominasi bobot, matriks hasilnya sparse, dan tidak mengenal kata baru (OOV).

### TF-IDF

Perbaikan terhadap BOW dengan memberikan penalti pada kata yang muncul di banyak
dokumen:

```
tf_idf(t, d, D) = tf(t, d) × idf(t, D)
idf(t) = log(N / df(t))
```

- `tf` — seberapa sering kata muncul di dokumen.
- `idf` — seberapa langka kata tersebut di seluruh korpus.

Kata yang muncul di semua dokumen (misal `love`) mendapat bobot nol; kata khas
dokumen (misal `football`, `cricket`) mendapat bobot tinggi.

### Word Embedding

Representasi kata dalam vektor padat berdimensi tetap (50–300) yang menangkap
kemiripan makna. "You shall know a word by the company it keeps" (J. R. Firth).
Dibuat lewat dua pendekatan: berbasis faktorisasi matriks (SVD pada matriks
ko-okurensi) dan berbasis jaringan saraf (Word2Vec CBOW / Skip-Gram).

## Dimensionality Reduction with PCA

PCA (Principal Component Analysis) adalah metode untuk mengurangi jumlah
dimensi data dengan tetap mempertahankan sebanyak mungkin varians. Data TF-IDF
berdimensi sebesar kosakata (bisa ribuan fitur) dan sangat sparse, sehingga sulit
dilihat atau dipakai langsung di banyak metode.

Prinsip kerja PCA:

- Mencari arah (komponen utama) yang menampung variansi data terbesar.
- Proyeksi data ke komponen pertama (PC1), kedua (PC2), dan seterusnya.
- Setiap komponen baru adalah kombinasi linier dari fitur asli dan saling
  ortogonal (tidak berkorelasi).

Informasi seberapa banyak varians yang dapat dipertahankan diukur dengan
`explained variance`; nilainya menurun di tiap komponen berikutnya. Dengan PCA
dua komponen, misalnya, data TF-IDF bisa diplot dalam bidang 2 dimensi sehingga
pola kelompok (misal antar label dokumen) lebih mudah diamati, meski sebagian
kecil varians hilang.