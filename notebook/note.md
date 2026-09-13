# Note

Perintah dan ringkasan setiap tugas. Catatan materi kuliahnya tersedia per
tugas di bawah ini.

## Note 1 — Repository & Webpage

1. Membuat repositori web mining di GitHub dengan nama `ppw`,
   `github.com/<username>/ppw`.
2. Membuat halaman statis (webstatis) berisi:
   - profil pribadi: nama, NPM, email
   - pengantar web mining

Catatan materi kuliah 1: [Note 1](note/note-1.md)

## Note 2 — Text Preprocessing

1. Lakukan eksplorasi data terlebih dahulu — cari anomali (misal kata asing,
   sebaran panjang teks per label) sebelum membuang kolom atau fitur.
2. Buang simbol, angka, dan karakter lain dari dokumen; angka tidak dihitung
   sebagai *term*. Anomali yang muncul akibat pembersihan (artefak format)
   ditangani dengan tabel keputusan berbasis bukti dari output.
3. Mendeteksi sisipan bahasa asing (per kalimat dan per kata). Kata/kalimat
   asing dipertahankan bila terjemahan berisiko mengubah konteks; setiap
   keputusan pertahankan/terjemahkan ditulis dalam tabel keputusan.
4. Membakukan kata tidak baku menjadi baku (slang preprocessing). Lindungi nama
   diri agar tidak ikut dinormalisasi, termasuk nama dari beberapa kata.
5. Mengekstrak seluruh kata unik dari dokumen menggunakan library `sklearn`.
6. Merepresentasikan setiap dokumen berita dalam bentuk vektor **TF-IDF**
   sebagai dataset siap model.
7. Mengurangi dimensi data TF-IDF menggunakan **PCA** dan memeriksa proporsi
   varians yang dipertahankan.

Catatan materi kuliah 2: [Note 2](note/note-2.md)

## Note 3