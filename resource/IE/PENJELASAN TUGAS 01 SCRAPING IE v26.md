TUGAS MATA KULIAH EKSTRAKSI INFORMASI

UJICOBA SCRAPING
A. MAKSUD DAN TUJUAN
     Mahasiswa melakukan proses ujicoba code scraping
     Mahasiswa memahami aplikasi scraping dan code di python
     Mahasiswa memahami tahapan dan proses pada masing-masing code scraping
     Mahasiswa memahami resource library scraping pyhton yang bisa digunakan

B. TAHAPAN TUGAS
  1. Mahasiswa memilih satu Pengadilan Negeri (PN) di Jawa Timur (Lihat Point F. PENGADILAN
     NEGERI YANG ADA DI JAWA TIMUR). Pembagian PN dan Nomor putusan silahkan dikoordinir
     ketua kelas dan ketua kelompok untuk menghindari dua atau lebih mahasiswa melakukan
     scraping nomor putusan yang sama dari PN yang sama.
  2. Silahkan pelajari code scraping yang disediakan.
     https://drive.google.com/drive/folders/1StUCQDNn7Gp7BG9yHiCVwMOojlZ4EDap?usp=sha
     ring
  3. Lakukan proses scraping untuk mendapatkan data pidana umum dari PN yang dipilih. Untuk
     mencapai posisi data pidana umum pada PN, ikuti langkah berikut:
     a) Akses link untuk menampilkan semua PN di jawatimur ini
          https://putusan3.mahkamahagung.go.id/pengadilan/profil/pengadilan/pt-
          surabaya.html
     b) Pada leftbar dengan judul pengadilan, klik atau pilih PN yang dituju.




      c) Jika tampilan PN sudah muncul, (hal ini ditandai dengan kemunculan nama PN di pojok
         kiri atas), kemudian klik atau pilih “pidana umum” yang ada pada leftbar




      d) Jika tampilan PN dan tulisan PIDANA UMUM sudah muncul, maka ambil URL yang muncul.
         Dari titik URL inilah code getURLlist.ipynb akan dijalankan.




     e) Kemudian jalankan code getMETAINFO.ipynb. (boleh melakukan berbagai modifikasi pada
         code yang intinya tetap melakukan proses mengambil data meta info dari halaman detail
         putusan. Setiap mahasiswa minimal mengambil meta info dari 200 putusan (pastikan data
         putusan yang diambil berbeda dengan teman yang lain).
  4. Buat file PDF untuk memperlihatkan proses menjalankan code beserta hasil dan berikan
     catatan seperlunya pada code. Jika pakai browser Opera bisa memilih menu page save
      as pdf. Sedangkan pada browser yang lain bisa pakai menu print dan pilih bentuk pdf. Beri
      nama file yang disimpan dengan IE-Scraping-nim.pdf
   5. Kumpulkan tugas dalam 2 bentuk, yaitu penjelasan code IE-Scraping-nim.pdf dikumpulkan
      via assignment GCR dan juga hasil scraping dikumpulkan dalam bentuk csv IE-NamaPN-
      nim.csv yang diletakkan pada satu folder kelas (mohon ketua kelas membuat share folder
      kelas)
   6. Kumpulkan tugas sesuai batas waktu yang sudah ditentukan di GCR.

C. INDICATOR PENILAIAN
   1. Kelengkapan catatan penjelasan dari setiap proses pada code
   2. Hasil meta info yang diperoleh (min 200 putusan)
   3. Jika masih terjadi 2 atau lebih mahasiswa dengan hasil scraping yang sama, maka mohon maaf
      nilai tidak akan diberikan.

D. PEMBAGIAN RENTANG NILAI
   Setiap tugas yang dikerjakan dengan benar sesuai ketentuan dari arahan dan penjelesan tugas ini,
   maka akan diberikan Nilai :
   - 100 (Seratus) = nilai maksimal untuk aplikasi berjalan dan mengumpulkan hari pertama
       sampai ketiga sejak assignment di posting.
   - 75 (Tujuh Puluh Lima) nilai maksimal untuk aplikasi berjalan dan mengumpulkan pada hari
       keempat dst sampai hari batas akhir pengumpulan.
   - 0 (Nol) bagi mereka yang tidak mengumpulkan tugas atau tidak sesuai batas waktu yang
       ditentukan

E. CATATAN

   Pastikan setiap mahasiswa sudah berhasil melakukan proses scraping pada notebook/laptopnya
   masing-masing. Tugas ini nantinya akan berkelajutan dan saling terkait dengan tugas berikutnya.

F. PENGADILAN NEGERI YANG ADA DI JAWA TIMUR
        Pilihan untuk Kelas A                Pilihan untuk Kelas B
    1) PN SIDOARJO 36.736                18) PN BLITAR 33.876
    2) PN PAMEKASAN 5.776                19) PN MALANG 31.080
    3) PN SURABAYA 98.730                20) PN PASURUAN 5.598
    4) PN BOJONEGORO 10.355              21) PN PROBOLINGGO 4.576
    5) PN TUBAN 11.148                   22) PN LUMAJANG 7.838
    6) PN LAMONGAN 8.655                 23) PN BANGIL 13.795
    7) PN GRESIK 11.121                  24) PN KRAKSAAN 7.486
    8) PN MOJOKERTO 15.503               25) PN MADIUN 6.359
    9) PN JOMBANG 15.385                 26) PN PONOROGO 6.222
    10) PN BONDOWOSO 5.874               27) PN PACITAN 2.440
    11) PN JEMBER 25.821                 28) PN NGAWI 6.237
    12) PN BANYUWANGI 16.042             29) PN MAGETAN 6.386
    13) PN SITUBONDO 4.823               30) PN SUMENEP 7.075
    14) PN KEDIRI 9.211                  31) PN BANGKALAN 8.394
    15) PN NGANJUK 9.157                 32) PN SAMPANG 5.610
    16) PN TULUNGAGUNG 17.407            33) PN KAB KEDIRI 21.969
    17) PN TRENGGALEK 6.842              34) PN KAB MADIUN 5.302
                                         35) PN KEPANJEN 8.421
