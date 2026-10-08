# Model Deployment

Deployment adalah tahap penutup siklus CRISP-DM: model yang sudah terbukti
baik diuji cara menghidupkannya sebagai layanan yang bisa dipakai pengguna
nyata, bukan hanya angka evaluasi di notebook.

## Serving Pipeline

Model tidak berjalan di ruang hampa. Saat permintaan datang, teks masukan harus
dibersihkan dengan aturan yang sama persis dengan data latih — jika
pembersihan waktu servis berbeda dari waktu pelatihan, prediksi melenceng tanpa
perlu diubah modelnya.

- **Pelatihan (training time)** — teks mentah disimpan, lalu dibersihkan
  melalui pipeline berurutan: normalisasi ascii, artefak format, aturan angka,
  pemecahan kalimat, lowercase, normalisasi slang dengan proteksi nama.
- **Servis (serving time)** — teks masukan diputar lewat pipeline yang sama,
  dipetakan ke representasi vektor, lalu diprediksi oleh estimator yang sudah
  dilatih.

Kesetaraan kedua jalur itu dicek dengan **parity test**: dokumen uji yang sama
dijalankan lewat jalur servis, dan hasilnya dibandingkan dengan evaluasi asli
model.

## Menangani Masukan Teks

Berbeda dari data latih yang sudah tersimpan, aplikasi menerima dokumen baru
saat itu juga:

- **Teks tempel** — pengguna menyalin isi berita langsung ke aplikasi.
- **URL berita** — aplikasi mengambil halaman web dari tautan yang diberikan,
  memakai *content extraction* yang tidak bergantung pada struktur HTML tertentu
  (misalnya `trafilatura`), lalu membersihkan dan memprediksi teks hasil
  ekstraksi.

Pengambilan halaman mematuhi etika crawling yang sama seperti saat koleksi:
membaca `robots.txt`, jeda antar permintaan minimal satu detik, user agent
jujur, berhenti dan mencatat bila situs menolak (403/429).

## Kemasan Rilis

Sebelum dipasang, model dikemas menjadi artefak mandiri supaya layanan tidak
bergantung pada notebook:

- model vektor kata (misalnya skip-gram Word2Vec),
- estimator terlatih (misalnya Naive Bayes),
- urutan kelas label,
- daftar pelengkap transformasi, seperti daftar nama yang dilindungi dari
  normalisasi slang.

Versi dependensi dikunci agar lingkungan produksi dapat direproduksi dengan
persis.

## Pilihan Hosting

Model dengan antar muka web biasa di-deploy melalui beberapa rute:

- **Hugging Face Space** — repositori aplikasi dengan lingkungan bawaan;
  mendukung Gradio dan Streamlit.
- **Streamlit Community Cloud** — sederhana untuk aplikasi Python murni.
- **Web statis** — hanya untuk model yang berjalan sepenuhnya di sisi klien.

Platform gratis biasanya memiliki batasan perangkat. Beberapa platform
mengenakan biaya untuk aplikasi biasa dan menyediakan perangkat *zero-GPU*
gratis dengan syarat, misalnya, aplikasi harus mendefinisikan sekurangnya satu
fungsi berdekorator penjadwalan GPU — berlaku juga untuk model CPU karena
platform tidak bisa membedakannya sebelum aplikasi menyala.

## Evaluasi Rilis

Setelah aplikasi hidup, verifikasi dilakukan dua arah:

- **Kesetaraan angka** — akurasi yang diukur lewat jalur servis harus sama
  dengan hasil validasi model di notebook.
- **Nasib permintaan** — status publik layanan (menyala, berhenti, gagal)
  dipantau lewat API platform, bukan hanya dicoba sekali oleh pembuatnya.