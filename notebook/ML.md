# Machine Learning

## Task 1 - Regresi Multivariate

Mencari study kasus dengan minimal 3 feature dan 5 data. lakukan perhitungan untuk mencari w0, w1, w2, dan w3 menggunakan pendekatan matrix. kemudian lakukan evaluasi dengan salah satu metode evaluasi (MSE, RMSE, R-square, MAE, MAPE). kelompok maksimal 3 orang dan ditulis tangan, kumpulkan hard copy saat perkuliahan pertemuan 3. pertemuan ke 3 akan ditanya secara random terkait hasil pekerjaan kelompok.

Dari tugas minggu sebelumnya (multivariate), gunakan data tersebut untuk membuat code. Struktur code python untuk tugas regresi linear multivariate: 
1. Import Library
2. Membuat Dataset
3. Menentukan X dan y
4. Train-Test Split
5. Membuat Model
6. Training
7. Mendapatkan b0, b1, b2, b3
8. Membentuk Persamaan Regresi
9. Testing / Prediksi
10. Bandingkan Aktual vs Prediksi
11. Lakukan evaluasi sesuai pilihan yang ada pada tugas sebelumnya.

Proses pengerjaan: [Task 1](ML/01-Linear-Regression.ipynb)

Studi kasus
Universitas memiliki beberapa gedung perkuliahan, selama ini pelaporan kerusakan fasilitas di

ketika ac ruang kelas rusak, mahasiswa menghubungi
ketua kelas meneruskan kepada petugas sarana dan prasarana
petugas kemudian mencatat laporan pada buku kerja
dan menghubungi teknisi yang di anggap sesuai
teknisi memeriksa kerusakan
jika kerusakannya ringan, teknisi langsung melakukan perbaikan
tapi jika membutuhkan suku cadang, teknisi menyampaikan kebutuhan kepada petugas
petugas mengajukan permintaan pembelian kepada bagian atau pihak yang terkait
setelah suku cadang tersedia, teknisi melanjutkan perbaikan
dalam prakteknya, pelapor sering menghubungi petugas berulang kali
untuk menanyakan perkembangannya.
beberapa laporan tidak tercatat
laporan yang lebih mendesak tidak selalu ditangani duluan
dan pimpinan tidak punya rekap waktu penyelesaian setiap kerusakan sarana

buatkan pemodelan bisnis as is nya.
siapa saja actor, pool, lane nya?
input dan outputnya apa?
sebutkan 5 pain point dari hasil pemodelan bisnis as is ini.
cari apakah ada eliminasi, simplify, dll
tentukan mana yang punya potensi untuk diperbaiki pada to-be