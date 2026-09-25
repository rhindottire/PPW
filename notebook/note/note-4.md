# Word Embedding

Model AI/ML tidak bisa bekerja langsung pada teks mentah. Setiap kata perlu
diubah menjadi representasi angka, dari yang paling sederhana sampai yang
menangkap makna.

## Text Representation

Cara merepresentasikan kata berkembang dari vektor jarang (sparse) menuju
vektor padat (dense) yang membawa informasi semantik:

- **One-hot vector** — vektor biner dengan satu posisi bernilai 1.
- **Bag of Words (BOW)** — frekuensi kemunculan kata dalam dokumen.
- **TF-IDF** — pembobotan yang menekan kata umum.
- **Word embeddings** — vektor padat berdimensi tetap yang menangkap kemiripan
  makna antar kata.

## One-Hot Encoding

Setiap kata dipetakan ke posisi tunggal dalam vektor sebesar ukuran kosakata
(N): semua elemen bernilai 0 kecuali satu yang bernilai 1.

Kekurangan utamanya:

- **Konsumsi memori tinggi** — ukuran vektor membengkak mengikuti jumlah
  kosakata (misalnya 1 juta kata berarti vektor berdimensi 1 juta).
- **Curse of dimensionality** — ruang fitur bertambah eksplosif.
- **Tanpa informasi semantik** — setiap kata saling ortogonal, sehingga kata
  berdekatan maknanya seperti "football" dan "soccer" tidak tampak mirip.

Tetap berguna untuk dataset kecil, variabel kategorikal, dan model baseline.

## Bag of Words

Prinsipnya:

- Menerapkan integer encoding (setiap kata punya indeks).
- Mengabaikan tata bahasa dan urutan kata.
- Bobot kata adalah frekuensi kemunculannya di dokumen.

Dipakai untuk mesin pencari, sistem rekomendasi, dan ekstraksi fitur awal
klasifikasi teks. Kelemahannya: urutan kata hilang, kata umum mendominasi,
matriks menjadi jarang, dan tidak mengenal kata baru (OOV).

## TF-IDF

TF-IDF memperbaiki BOW dengan menurunkan bobot kata yang muncul di banyak
dokumen sekaligus:

```
tf_idf(t, d, D) = tf(t, d) × idf(t, D)
idf(t) = log(N / df(t))
```

- `tf(t, d)` — frekuensi kata `t` dalam dokumen `d`.
- `idf(t)` — kebalikan frekuensi dokumen: kata yang umum (df besar) mendapat
  penalti, kata yang jarang dan spesifik berbobot tinggi.
- `N` — jumlah dokumen, `df(t)` — banyak dokumen yang memuat kata `t`.

Hasilnya menyoroti kata kunci unik per dokumen. Keterbatasannya tetap pada
konteks yang diabaikan dan matriks yang masih sparse.

## SVD Embeddings

Salah satu cara membangun embedding adalah faktorisasi matriks:

1. Bentuk matriks ko-okurensi, misalnya **document-term matrix** (N × D):
   frekuensi setiap kata pada setiap dokumen.
2. Terapkan **Singular Value Decomposition (SVD)** untuk mereduksi dimensi
   menjadi (N × d), dengan `d` dimensi embedding yang diinginkan
   (misalnya 2, 100, hingga 500).
3. Setiap baris hasil SVD menjadi vektor kata berdimensi `d`. Kata yang
   sering muncul bersama akan berdekatan dalam ruang vektor baru.

Kelemahan SVD: matriks didominasi kata berfrekuensi tinggi sehingga skewness
parah, biaya komputasi mahal, dan seluruh matriks harus dihitung ulang saat
ada kata atau dokumen baru.

## Word2Vec

Pendekatan kedua adalah model berbasis jaringan saraf yang belajar vektor kata
dengan memprediksi kata tetangga, terbagi dalam dua arsitektur:

- **CBOW (Continuous Bag of Words)** — memprediksi kata pusat dari kata-kata
  konteks di sekitarnya.
- **Skip-Gram** — sebaliknya, memprediksi kata konteks dari kata pusat.

Prinsipnya dirangkum oleh Firth (1957): *"You shall know a word by the company
it keeps"* — makna kata ditentukan oleh kata-kata yang sering muncul di
sekitarnya.

## Training Skip-Gram

Data pelatihan dibuat dengan pasangan (kata pusat, kata konteks) berdasarkan
ukuran jendela (window); misalnya dengan window = 1, kata pusat dikaitkan
dengan satu kata di kiri dan satu kata di kanan.

Tahapannya:

1. Encode kata pusat sebagai one-hot (X) dan kata konteks sebagai one-hot
   target (y).
2. Masukkan ke jaringan dengan lapisan bobot dan aktivasi **softmax** di
   lapisan akhir untuk memprediksi probabilitas kata konteks.
3. Setelah pelatihan, setiap baris bobot pada lapisan pertama diambil sebagai
   **embedding** kata yang bersangkutan.

Hasil pelatihan adalah vektor padat yang menempatkan kata bermakna serupa di
posisi berdekatan, diukur misalnya dengan cosine similarity.