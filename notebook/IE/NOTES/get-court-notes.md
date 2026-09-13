# Catatan Folder GET-COURT

Catatan pembacaan source code `notebook/IE/GET-COURT/`. Dibuat read-only;
tidak ada file sumber yang diubah. Semua file notebook & data berasal dari
`GET-COURT-*.zip` yang sudah diekstrak ke `GET-COURT/`; arsip `.zip`
aslinya dihapus dari repo setelah ekstraksi (semua isi terverifikasi terekstrak).

## Inventori File

- **Notebook (3)**: `getURLlist.ipynb`, `getMETAINFO.ipynb`, `getFileDownload.ipynb`
- **Data `listURL*.txt`**: daftar URL halaman detail putusan (`.../direktori/putusan/{id}.html`)
- **Data `meta*.csv`**: metadata putusan hasil scraping (21 kolom)
- `hasilListURLPage1.txt`: artefak uji (7 URL saja)
- `OUTPUT/listURLPerbuatanMelwanHukum*.txt`: daftar URL kategori perbuatan melawan hukum (5 file)

Data listURL besar (jumlah baris):

| File | Jumlah URL | Kategori / Pengadilan |
|---|---|---|
| listURLPencurianPNJAKPUS.txt | 1.073 | Pencurian — PN Jakarta Pusat |
| listURLNarkobaPNJAKPUS.txt | 1.000 | Narkoba — PN Jakarta Pusat |
| listURLPerceraianPAJAKPUS.txt | 1.000 | Perceraian — PA Jakarta Pusat |
| listURLPerceraianPAJAKPUS1..5.txt | 200 × 5 | Perceraian — PA Jakarta Pusat (chunk; gabungan = 1.000, saling-disiplin) |
| listURLPerceraianPASBY.txt | 1.000 | Perceraian — PA Surabaya |
| OUTPUT/listURLPerbuatanMelwanHukumPNJAKPUS.txt | 40 | PMH — PN Jakarta Pusat |
| OUTPUT/listURLPerbuatanMelwanHukumPNJAKPUS1.txt | 0 (kosong) | PMH — PN Jakarta Pusat |
| OUTPUT/listURLPerbuatanMelwanHukumPNJAKPUS2.txt | 20 | PMH — PN Jakarta Pusat |
| OUTPUT/listURLPerbuatanMelwanHukumPNJAKBAR.txt | 140 | PMH — PN Jakarta Barat |
| OUTPUT/listURLPerbuatanMelwanHukumPNSBY.txt | 380 | PMH — PN Surabaya |
| hasilListURLPage1.txt | 7 | Campuran (uji awal) |

Data metaCSV (baris = jumlah data):

| File | Baris | Kondisi |
|---|---|---|
| metaPutusan.csv | 4 | 2 kasus unik terduplikasi; ada byte non-UTF8 (0x97) |
| metaPutusan1.csv | 7 | Campuran pengadilan; 1 baris tanpa URL |
| metaPencurianPNJAKPUS.csv | 1.073 | Header ber-trailing comma+CRLF → 22 kolom; 551 baris `url` kosong |
| metaPerceraianPAJAKPUS1.csv | 198 | **Semua 198 baris** `url` kosong |
| metaPerceraianPASBY.csv | 997 | 588 `url` kosong, 409 unik |
| metaPerbuatanMelwanHukumPNSBY.csv | 263 | 202 `url` kosong, 61 unik |

## Alur Pipeline (3 Tahap)

```
Tahap 1  getURLlist.ipynb   → listURL*.txt          (daftar URL halaman detail)
Tahap 2  getMETAINFO.ipynb  → meta*.csv             (metadata + URL unduh PDF)
Tahap 3  getFileDownload.ipynb → {id}.pdf           (unduh PDF dari kolom url)
```

### getURLlist.ipynb
- Target: `https://putusan3.mahkamahagung.go.id/direktori/index/pengadilan/.../kategori/pencurian-1.html`
- Library: `requests` (pakai `verify=False`), `BeautifulSoup` (bs4)
- Logika: `findAll('a')`, URL valid jika anchor persis mulai di index 9 `'<a href="'` dan mengandung `html">Putusan`
- `main()`: hanya ambil `ulang = 2` halaman → tulis `hasilListURLPage.txt`
- Data listURL besar **bukan** hasil dari kode apa adanya (butuh loop lebih besar)

### getMETAINFO.ipynb
- Parsing: `ul class="portfolio-meta"` → tabel meta; pidana vs perdata (deteksi `/Pdt.`)
- URL unduh diambil dari elemen ul kedua, `li` index 4, dipotong antara `"https"` dan `'">'`
- Header CSV 21 kolom: `terdakwa, penuntut_umum, nomor, tingkat_proses, klasifikasi, kata_kunci, tahun, tanggal_register, lembaga_peradilan, jenis_lembaga_peradilan, hakim_ketua, hakim_anggota, panitera, amar, amar_lainnya, catatan_amar, tanggal_musyawarah, tanggal_dibacakan, kaidah, abstrak, url`
- Error per-baris hanya di-print (`Error Get Meta Inf, ...`) lalu baris dilewati → CSV kekurangan data tanpa artefak jelas

### getFileDownload.ipynb
- Ambil `row[20]` (kolom `url`) → `requests.get` → simpan `{segment_terakhir}.pdf`
- Baris dengan `url` kosong di-skip

## Poin Kritis & Bug

1. **TIDAK ADA delay politeness** sama sekali (semua notebook). Tidak ada User-Agent/session khusus. `time` di-import tapi tidak dipakai. Melanggar etika crawl minimal 1 detik.
2. **Path hardcoded**:
   - `getMETAINFO.ipynb`: `/content/drive/MyDrive/GET-COURT/listURLPerceraianPASBY.txt` dan `metaPerceraianPASBY.csv` (Google Colab) → tidak jalan di lokal tanpa edit
   - `getFileDownload.ipynb`: `D:/6.PYTHON-CODE/GET-PUTUSAN/metaPutusan1.csv` dan folder output `D:/6.PYTHON-CODE/GET-PUTUSAN/OUTPUT` (Windows) → tidak jalan di lokal tanpa edit
3. **Parsing rapuh**:
   - `getURLlist`: mensyaratkan anchor persis dimulai `'<a href="'` di posisi 9 → anchor dengan atribut lain (class dll.) tidak tertangkap. Ini menjelaskan `hasilListURLPage1.txt` hanya 7 URL campuran
   - `getMETAINFO`: `rowsMETA2[1]` dan `urlDL[4]` → IndexError bila struktur halaman berbeda → ribuan baris `url` kosong
   - `metaPencurianPNJAKPUS.csv` 22 kolom (header excess) → `getFileDownload` berisiko IndexError
4. Nama file output di kode `hasilListURLPage.txt`, di zip `hasilListURLPage1.txt` → bukan produk run kode versi ini
5. `getURLlist`: `data_path = "./data/"` tak terpakai
6. SSL `verify=False` di notebook 1 & 2 (InsecureRequestWarning diredam)


## Penilaian Run-Readiness

| Notebook | Status | Syarat agar jalan |
|---|---|---|
| getURLlist.ipynb | ⚠️ Jalan tapi hasil tidak sesuai | Conflict hanya 2 halaman; parsing rapuh; ubah target/loop bila ingin mereproduksi listURL besar |
| getMETAINFO.ipynb | ❌ Tidak siap | Ubah path Colab → lokal; tambah delay; perkuat parsing URL download |
| getFileDownload.ipynb | ❌ Tidak siap | Ubah path Windows → lokal; pastikan CSV 21 kolom konsisten; tambah delay |

Sumber data & kode: `putusan3.mahkamahagung.go.id` (bukan SIPP). Menurut proyek
PPW, crawling wajib memakai extractor trafilatura + delay ≥1 dtk + User-Agent
sopan; ketiga notebook di atas menyalahi aturan itu sehingga tidak boleh
dipindahkan apa adanya ke deliverable PPW tanpa revisi etika.