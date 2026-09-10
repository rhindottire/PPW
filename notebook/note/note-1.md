# Apa itu Web Mining

Web mining adalah proses menemukan dan mengekstrak informasi dari internet
menggunakan berbagai teknik data mining. Dua definisi yang sering dirujuk:

- Penggunaan teknik data mining untuk mencari dan mengekstrak informasi dari
  layanan web secara otomatis (Etzioni, 1996).
- Mencari pola berguna atau pengetahuan dari struktur hyperlink, isi halaman,
  dan perilaku pengguna web (Bing Liu, 2007).

## Tantangan pemrosesan data web

- Web merupakan basis data yang sangat besar, kompleks, dinamis, dan tidak
  memiliki domain spesifik.
- Datanya tersedia dalam berbagai format: HTML, XML, teks biasa.

## Taxonomy Web Mining

Web mining terbagi menjadi tiga cabang:

| Cabang | Fokus |
| --- | --- |
| **Content Mining** | Mengekstrak informasi dari isi halaman web: teks, gambar, audio, video, serta data terstruktur. |
| **Structure Mining** | Menemukan pola dari struktur tautan (hyperlink) dan jaringan sosial antar pengguna. |
| **Usage Mining** | Menganalisis data yang dihasilkan dari kunjungan dan transaksi pengguna, misalnya log server dan clickstream. |

## Content Mining

Fokus pada isi dokumen web, dengan tugas-tugas seperti:

- **Ekstraksi informasi** — mengambil data terstruktur dari konten web yang
  tidak atau semi-terstruktur.
- **Klasifikasi dokumen** — mengkategorikan dokumen baru ke kelas yang tepat,
  misalnya kategorisasi berita, produk, dan deteksi spam.
- **Clustering** — mengelompokkan dokumen yang mirip, misalnya untuk hasil
  pencarian atau topic discovery.
- **Analisis sentimen** — menentukan polaritas teks (positif, netral,
  negatif) pada tingkat dokumen, kalimat, atau fitur.
- **Topic modelling**, peringkasan dokumen, dan ekstraksi kata kunci.

Metode yang dipakai antara lain Naive Bayes, SVM, jaringan saraf,
transformers, K-Means, dan similarity measures seperti cosine dan Jaccard.

## Structure Mining

Mempelajari grafik web, di mana halaman adalah simpul dan hyperlink adalah
sisi. Aplikasinya:

- Menentukan otoritas halaman, misalnya **PageRank** pada Google Search.
- Mendeteksi komunitas online dan komunitas dalam jaringan sosial.
- Identifikasi simpul penting (centrality), misalnya pengguna influencer.

## Usage Mining

Mengolah data yang dihasilkan saat pengguna mengunjungi halaman: log akses
server, log referer, cookie, dan clickstream. Aplikasinya antara lain product
recommendation dan personalized search.

## Proses Web Mining

Secara umum sama dengan proses data mining, hanya berbeda pada tahap
pengumpulan dan pemrosesan data:

1. **Gathering & exploration** — mengumpulkan data lewat crawling atau Web API,
   lalu memahami datanya dengan ringkasan statistik dan visualisasi.
2. **Preprocessing & transformation** — mengubah data ke representasi yang
   sesuai metode data mining, misalnya reduksi dimensi, seleksi fitur, dan
   vektorisasi teks.
3. **Actual data mining** — menerapkan metode, mengevaluasi model, dan
   melakukan iterasi (uji hyperparameter, tambah data, perbaiki praproses).

Pemrosesan data biasa memakan 70–80% dari total waktu proyek data mining.