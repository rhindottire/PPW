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

1. Lakukan eksplorasi data terlebih dahulu — cari anomali (sebaran panjang teks
   per label, karakter non-ASCII, sisipan bahasa asing) sebelum membuang kolom
   atau fitur.
2. Buang angka dan tanda baca; angka tidak dihitung sebagai *term*. Artefak
   pembersihan (URL, lambang mata uang, token komposit, angka Romawi) ditangani
   dengan tabel keputusan berbasis bukti dari output.
3. Deteksi bahasa asing per kalimat dan per kata. Kata asing dipertahankan bila
   terjemahan berisiko mengubah konteks, dan keputusan pertahankan/tolak
   ditulis dalam tabel keputusan.
4. Bakukan kata tidak baku menjadi kata baku (slang preprocessing). Lindungi
   nama diri agar tidak ikut dinormalisasi.
5. Buang stopword bahasa Indonesia menggunakan daftar Sastrawi.
6. Stemming kata ke bentuk dasar menggunakan Sastrawi.
7. Ekstrak seluruh kata unik dokumen menggunakan library `sklearn`.
8. Representasikan setiap dokumen berita dalam vektor **TF-IDF** sebagai
   dataset siap model, dengan tabel bobot yang memperlihatkan term lawan
   dokumen.
9. Kurangi dimensi TF-IDF dengan **PCA**; hitung explained variance kumulatif
   dan target dimensi di bawah 500.
10. Lakukan **POS tagging** untuk melabeli kategori kata. Posisinya sebelum
    stopword removal agar kata fungsi tetap menjadi konteks, dan hasil anotasi
    tidak mengubah representasi final (TF-IDF).

## Note - 3 gunakan orange
1. import data
2. PCA
2. klasifikasi menggunakan naive bayes / KNN
4. test and score

Catatan materi kuliah 2: [Note 2](note/note-2.md)
