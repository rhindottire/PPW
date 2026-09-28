# Orange Workflow

Verifikasi visual dari tugas klasifikasi berita (Tugas 3). Notebook `Book 3`
menjalankan pipeline yang sama lewat kode Python; di sini rangkaian itu
dibangun ulang dengan Orange Data Mining agar setiap tahap bisa diamati.

Orange berjalan di lingkungan terpisah, `.venv-orange`, karena Orange 3.40
belum mendukung Python 3.14 yang dipakai proyek ini.

```bash
.venv-orange/bin/python scripts/orange-task3/run_pipeline.py
```

Skrip itu menjalankan rantai yang identik dengan kanvas dan mencetak angka yang
ditampilkan widget, sehingga hasilnya bisa diperiksa tanpa membuka GUI.

## Pipeline Orange

Workflow dibuka dari `task3.ows`:

- **File** — membaca `data/Web-Mining/crawling_detik.csv`.
- **Corpus** — menunjuk kolom `isi_berita` sebagai teks dokumen dan `label`
  sebagai variabel kelas. Tanpa node ini, teks berita tetap berupa kolom
  teks biasa dan tidak pernah sampai ke vektorisasi.
- **Bag of Words (TF-IDF)** — pembobotan frekuensi term, IDF, dan normalisasi
  L2; menghasilkan **8.109 term**.
- **PCA** — varian kumulatif diukur pada korpus hasil vektorisasi.
- **Naive Bayes dan kNN** — dua model dilatih dari data tereduksi; kNN
  memakai k = 2.
- **Test and Score** — akurasi kedua model.
- **Confusion Matrix** — kesalahan klasifikasi per kelas.

## Hasil

| Model | Akurasi | Precision | Recall | F1 | Confusion |
|---|---|---|---|---|---|
| Naive Bayes | 1,000 | 1,000 | 1,000 | 1,000 | `[[100, 0], [0, 100]]` |
| kNN (k=2) | 1,000 | 1,000 | 1,000 | 1,000 | `[[100, 0], [0, 100]]` |

Nilai 8.109 term berbeda dari 3.588 term di `Book 3` karena Orange tidak
membuang term yang hanya muncul sekali, sedangkan pipeline Python memakai
`min_df=2`.

## Tiga hal yang perlu diketahui

**Test and Score di sini menilai data latih.** Widget itu baru memakai data uji
yang benar bila output *Test Data* juga disambung. Pada workflow ini hanya
*Data* yang masuk, jadi skor 1,000 di atas adalah evaluasi pada data latih dan
wajar terjadi pada dua topik yang terpisah. Angka yang bisa dipertanggungjawabkan
tetap ada di `Book 3`, yang memakai pemisahan data dan cross-validation.

**Normalisasi menentukan berapa besar kNN.** Varian Bag of Words di Orange
menerapkan L2 pada bobot term, bukan panjang tiap dokumen; panjang dokumen
bervariasi dari 2 sampai 40.001 sehingga satu komponen PCA pertama sudah
menangkap 99,97% varian. Setelah tiap dokumen dinormalisasi ke panjang satuan,
kNN turun ke akurasi 0,780 dengan recall 0,560, sementara Naive Bayes tetap
1,000. Perbedaannya bukan pada model, melainkan pada skala jarak.

**Workflow lama tidak bisa dibuka di Orange 3.40.** `task3.ows` versi
sebelumnya menyambungkan File langsung ke input Corpus milik Bag of Words,
padahal widget itu hanya menerima objek Corpus hasil node Corpus. Node Corpus
sudah ditambahkan, dan itu sebabnya bagian tangkapan layar sebelumnya kosong.

## Tangkapan layar

Bagian ini masih perlu satu kali sesi `orange-canvas` interaktif: workflow
dibuka, file dan kolom dipilih, lalu setiap widget utama difoto. Angka pada
halaman ini bukan hasil tangkapan layar, melainkan hasil eksekusi skrip
`run_pipeline.py`.

Data berita bersumber dari hasil crawler detik.com di
`data/Web-Mining/crawling_detik.csv`.
