# Information Extraction

Ringkasan instruksi setiap tugas, disusun dari PDF penjelasan tugas resmi
dari dosen. Proses pengerjaan lengkap tersedia pada notebook masing-masing.

## Task 1 — Court Scraping

**Maksud dan tujuan.** Mahasiswa melakukan proses ujicoba code scraping,
memahami aplikasi scraping dan kode Python, memahami tahapan proses pada
masing-masing kode scraping, serta memahami resource library scraping Python
yang bisa digunakan.

**Tahapan tugas.**

1. Pilih satu Pengadilan Negeri (PN) di Jawa Timur. Pembagian PN dan nomor putusan
   dikoordinasikan dengan ketua kelas dan ketua kelompok agar tidak ada dua
   mahasiswa atau lebih yang melakukan scraping nomor putusan dari PN yang sama.
2. Pelajari code scraping yang disediakan pada
   [drive kelas](https://drive.google.com/drive/folders/1StUCQDNn7Gp7BG9yHiCVwMOojlZ4EDap?usp=sharing).
3. Lakukan proses scraping untuk mendapatkan data pidana umum dari PN yang
   dipilih. Untuk mencapai posisi data pidana umum pada PN:
   1. Akses link yang menampilkan semua PN di Jawa Timur:
      <https://putusan3.mahkamahagung.go.id/pengadilan/profil/pengadilan/pt-surabaya.html>
   2. Pada leftbar dengan judul pengadilan, klik atau pilih PN yang dituju.
   3. Jika tampilan PN sudah muncul — ditandai dengan kemunculan nama PN di
      pojok kiri atas — klik atau pilih "pidana umum" pada leftbar.
   4. Jika nama PN dan tulisan PIDANA UMUM sudah muncul, ambil URL yang muncul.
      Dari titik URL inilah `getURLlist.ipynb` dijalankan.
   5. Kemudian jalankan `getMETAINFO.ipynb`. Modifikasi pada kode diperbolehkan,
      selama inti kode tetap mengambil meta info dari halaman detail putusan.
      Setiap mahasiswa minimal mengambil meta info dari 200 putusan, dan pastikan
      data putusan yang diambil berbeda dengan teman yang lain.
4. Buat file PDF yang memperlihatkan proses menjalankan kode beserta hasilnya,
   dan berikan catatan seperlunya pada kode. Pada browser Opera bisa memakai menu
   page → save as pdf, sedangkan browser lain memakai menu print lalu pilih
   bentuk pdf. Beri nama file `IE-Scraping-nim.pdf`.
5. Kumpulkan tugas dalam dua bentuk: penjelasan kode `IE-Scraping-nim.pdf`
   dikumpulkan via assignment GCR, dan hasil scraping dikumpulkan dalam bentuk
   csv `IE-NamaPN-nim.csv` yang diletakkan pada satu folder kelas.
6. Kumpulkan tugas sesuai batas waktu yang ditentukan di GCR.

**Indikator penilaian.**

- Kelengkapan catatan penjelasan dari setiap proses pada kode.
- Hasil meta info yang diperoleh, minimal 200 putusan.
- Jika dua mahasiswa atau lebih menghasilkan scraping yang sama, nilai tidak
  akan diberikan.

**Pembagian nilai.** Nilai maksimal 100 bila aplikasi berjalan dan tugas
dikumpulkan pada hari pertama sampai ketiga sejak assignment diposting. Nilai
maksimal 75 bila dikumpulkan pada hari keempat dan seterusnya sampai batas
akhir pengumpulan. Nilai 0 bila tidak mengumpulkan tugas atau pengumpulan
melewati batas waktu.

**Catatan.** Setiap mahasiswa harus berhasil melakukan proses scraping pada
notebook atau laptopnya masing-masing. Tugas ini berkelajutan dan saling
terkait dengan tugas berikutnya.

**Penugasan.** Kelas B — PN Ngawi.

Proses pengerjaan: [Task 1](IE/01-Scraping-230411100197.ipynb)
