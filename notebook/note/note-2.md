# Word Representation

Algoritma NLP tidak bisa membaca teks mentah secara langsung; kata-kata harus
diubah menjadi angka. Materi kuliah kedua membahas cara merepresentasikan kata
beserta metode preprocessing teks yang menjadi dasar tugas praktikum.

## Word Encoding

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

## POS Tagging

POS tagging (Part-of-Speech) memberi label kategori gramatikal pada setiap kata,
misalnya kata benda (NN), kata kerja (VB), kata sifat (JJ), dan kata depan (IN).
Label ini menangkap peran kata dalam kalimat sehingga teks dapat dianalisis
lebih dalam, misalnya membedakan nama diri dari kata biasa atau menyusun fitur
berdasarkan pola gramatikal.

Terdapat beberapa set tag. Set universal (UD/UPOS) menyediakan label seperti
`NOUN`, `VERB`, `ADJ`, `ADP`, `PRON`, `DET`, `PROPN`. Bahasa Indonesia juga
memiliki tagset berbasis akronim kategori, misalnya `NNP` (nama diri orang),
`NNO` (nomina umum), `VBT`/`VBI` (verba transitif/intransitif), `ADJ`
(adjektiva), serta `PPO` (preposisi). Penamaan tag yang berbeda tidak mengubah
konsep dasarnya.

Posisi tagging dalam alur preprocessing menentukan kualitas hasilnya. Tagger
dilatih pada kalimat utuh sehingga ia perlu *sebelum* stopword removal — kata
fungsi memberi konteks untuk mendisambiguasi kata di sekitarnya — dan *sebelum*
stemming, karena bentuk infleksi (penuh afiks) adalah masukan asli model.
Anotasi POS bersifat pelengkap; representasi fitur akhir seperti TF-IDF tidak
harus menggunakannya.

## Stopword Removal

Stopword adalah kata yang nyaris tanpa makna sendiri dan muncul di hampir semua
dokumen, misalnya *dan*, *yang*, *di*, *dengan*, *untuk*. Karena terlalu umum,
kata-kata ini tidak membantu membedakan isi dokumen dan biasanya dibuang sebelum
representasi dibuat.

Pustaka **Sastrawi** menyediakan daftar stopword bahasa Indonesia siap pakai.
Pemotongan dilakukan dengan mencocokkan tiap token terhadap daftar tersebut;
token yang cocok dihapus dari dokumen. Contoh efeknya:

- Sebelum: "para pemain yang bermain keras dan disiplin"
- Sesudah: "para pemain bermain keras disiplin"

TF-IDF sebenarnya sudah memberi bobot rendah pada stopword karena frekuensi
dokumennya tinggi. Pembuangan eksplisit tetap berguna karena mengecilkan kosakata
dan membebaskan bobot bagi kata yang bermakna.

## Stemming

Stemming memotong afiks (awalan, akhiran, sisipan, dan kombinasinya) sehingga
bentuk kata sekeluarga dikembalikan ke kata dasarnya. Tujuannya agar bentuk yang
berlainan tetapi bermakna sama tidak diperlakukan sebagai fitur terpisah.
**Sastrawi** menyediakan stemmer bahasa Indonesia dengan hasil berupa kata dasar:

- `menambahkan` → `tambah`
- `permainan` → `main`
- `memakannya` → `makan`
- `menjadikan` → `jadi`

Manfaatnya: jumlah kata unik menurun (dimensi kosakata mengecil) dan kecocokan
antar dokumen lebih mudah diperoleh. Risikonya adalah *over-stemming* yang
menyatukan kata berbeda makna, sehingga nama diri perlu dilindungi dan hasil
pemotongan ditinjau kembali.

## Dimensionality Reduction

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