# Log Kerja Tugas IE

Catatan kerja internal matakuliah IE (Information Extraction). Bukan deliverable
dan bukan bagian web book. Isinya: status, artefak, keputusan, dan jebakan yang
sudah pernah kena, supaya sesi berikutnya tidak membaca ulang notebook, PDF, dan
data hanya untuk tahu di mana posisi pekerjaan.

## Cara Pakai

- Baca file ini SEBELUM mengerjakan tugas IE, sebelum membuka notebook.
- Perbarui di akhir setiap tugas IE: status, tanggal verifikasi, item terbuka.
- Bagian "Angka Volatil" gampang basi. Cek ulang dari output notebook yang
  dieksekusi, jangan percaya catatan ini.

## Status

| Tugas | Notebook | Artefak lokal (`data/IE/`, tidak dilacak git) | Status | Sisa |
|---|---|---|---|---|
| T1 Scraping | `notebook/IE/01-Scraping-230411100197.ipynb` | `IE-Scraping-230411100197.pdf`; `PN-Ngawi/` (CSV 208×21, `html/`, `robots.txt`, `listURL-*.txt`, `candidateURL-*.json`) | selesai, verifikasi 2026-10-01 | — |
| T2 Rule-based | `notebook/IE/02-RuleBased-IE-230411100197.ipynb` | `IE-RuleBased-230411100197.pdf`, `IE-RuleBased-Hasil-230411100197.pdf`; `rule-based/` (`HASIL/courtHistory-PN-Ngawi.csv` 6×15, `PDF/`, `TXT/`) | selesai, verifikasi 2026-10-05 | — |
| T3 Machine Learning | `notebook/IE/03-MachineLearning-IE-230411100197.ipynb` | `IE-coba-ML1-230411100197.pdf`, `IE-coba-ML2-230411100197.pdf`, `IE-modif-ML-230411100197.pdf`; `ML2-work/*.pkl`; `PN-Ngawi/IE-ml-dataset-230411100197.csv` | selesai, verifikasi 2026-10-14 | label `JUG` (ditunda, lihat Item Terbuka) |
| T4 Dataset | `notebook/IE/04-Dataset-230411100197.ipynb` | `IE-Dataset-230411100197.pdf`; `dataset/` (`PN-NGW-230411100197.csv` + `.txt`, `pemeriksa.txt`, `PDF/`, `TXT/`, `unduh/daftar-unduhan.csv`) | selesai, verifikasi 2026-10-21 | kirim CSV+TXT ke GCR |

Ringkasan tiap tugas untuk pembaca (halaman web book) ada di `notebook/IE.md`
seksi `## Task N`, ditutup baris `Proses pengerjaan: [Task N](...)`.

## Fakta Tetap

Jangan di-derive ulang tiap sesi.

- Identitas: Achmad Ridho Fa'iz, NIM 230411100197, Kelas B.
- Pengadilan: **Pengadilan Negeri Ngawi** ("PN Ngw"). Waktu scraping: 25 September 2026.
- Scope: PN Ngawi dibagi 5 orang dan tiap orang dapat bagian halaman (kita
  halaman 1–11 dari 179 putusan). Karena itu dokumen kita tidak boleh sama
  dengan milik orang lain, dan bukti "korpus = jatah sendiri" ditanam di
  notebook 04 seksi C.1.
- Skema label kanonik 12 entitas + `O`, format IOB (`B_`/`I_`):
  VERN, DEFN, CRIA, ARTV, PENA, PUNI, TIMV, JUDP, JUDG, REGI, PROS, ADVO.
  `JUDP` = hakim ketua, `JUDG` = hakim anggota. Dosen memakai 12 kelas ini
  (rujukan: `resource/IE/ML/ML1/NER-200-WithPosPrevNext.ipynb`).
- Kolom CSV dataset anotasi (T4): `doc,sentence,token,tag`.
- Kernel notebook: `enWebmining` (venv `.venv`); pipeline Orange: `.venv-orange`.
- Etika crawl: `robots.txt` situs menolak akses otomatis, jadi tidak ada
  pengambilan otomatis dan tidak ada upaya bypass. Notebook mencatat status
  izin, bukan cara menembus pemblokiran.
- Toolchain: `jupyter nbconvert --to webpdf` jalan (playwright/chromium), LaTeX
  tidak terpasang sehingga `--to pdf` gagal. Perintah lengkap ada di bagian
  Perintah Verifikasi.
- Git: `data/IE/` di-ignore penuh (memuat data personal), jadi deliverable
  lokal tidak dilacak. `graphify-out/` juga di-ignore. `resource/IE/NOTES/`
  dilacak dan berisi catatan verifikasi berkas dosen, bukan log ini.
- Pola nama PDF deliverable: `data/IE/IE-<Tugas>-230411100197.pdf`.

## Keputusan dan Alasan

- **T1 Scraping** — input dari `listURL-PN-Ngawi.txt` + `candidateURL-PN-Ngawi.json`,
  keluaran metadata 208 putusan × 21 kolom. `IE-PN-Ngawi-230411100197-raw.csv`
  adalah salinan CSV final.
- **T2 Rule-based** — ekstraksi regex pada TXT cache → `courtHistory-PN-Ngawi.csv`
  (15 kolom, 6 baris contoh) dan versi PDF/TXT.
- **T3 Machine Learning** — dataset token-level `doc,fragment,token,label,pos`
  (`PN-Ngawi/IE-ml-dataset-230411100197.csv`); model CRF 600 dok disimpan di
  `ML2-work/`.
- **T4 Dataset**
  - Kolom tetap `doc,sentence,token,tag` (bukan `word`/`pos` seperti referensi
    dosen) karena tugas hanya mewajibkan bentuk CSV dengan "skema IOB pada kolom
    `tag`", dan notebook 03 sendiri memakai `token`.
  - Kalau entitas terpotong batas fragmen (`;`), penanda dimulai ulang `B_` di
    fragmen berikutnya.
  - Corpus check di seksi C.1 adalah bukti jatah sendiri, bukan indikator
    penilaian; angkanya objek volatil.
  - `dataset/unduh/` menyimpan halaman daftar unduhan + `daftar-unduhan.csv`
    (kolom `nomor,url,tahun,tipe,unduh`), sumber tunggal untuk verifikasi korpus.
  - Nama kedua pemeriksa dataset dibaca notebook dari
    `dataset/pemeriksa.txt` (lokal, tidak dilacak), bukan ditulis di sel
    notebook. Alasannya: notebook 04 ikut terbit di web book, sedangkan nama
    orang tidak boleh tampil di halaman publik. Output notebook hanya menyebut
    nama berkas dan jumlah baris.
  - Pelabelan ADVO/PROS ditambah karena audit 2026-10-21 menunjukkan cakupan
    jauh di bawah kenyataan teks. ADVO memakai penanda `DIDAMPINGI (OLEH)?`,
    `ADVOKAT`, `PENGACARA`, dan `PENASIAT/PENASEHAT/PENASIHAT HUKUM`, dengan
    kata peran di antara penanda dan nama dilewati. PROS diambil dari badan
    teks hanya bila nama dari metadata tidak ketemu di teks.
  - Kata peran (`HAKIM`, `ANGGOTA`, `PANITERA`, `PENGGANTI`, `PENUNTUT`,
    `JAKSA`, `SAKSI`, dst.) masuk daftar henti ADVO/PROS. Ini yang membuat
    cakupan ADVO turun dari angka semu 179 ke 66 dokumen; penanda ADVO sering
    muncul pada kalimat hak ("Terdakwa tidak ... untuk didampingi oleh Penasihat
    Hukum") yang tidak diikuti nama, sehingga aturan lama menyerobot kata peran
    di blok berikutnya.
  - Legenda tag ditulis di dua tempat agar pembaca tidak menebak singkatan:
    tabel `### Tag Legend` (tag, entitas, sumber) pada sel B notebook, dan blok
    "Arti tag" pada berkas TXT. Catatan di sel B juga dikoreksi: cadangan
    (`fallback_spans`) hanya ada untuk VERN, DEFN, dan PROS, bukan PENA/PUNI.
  - Sisa entitas yang belum lengkap dibiarkan apa adanya dengan alasan yang
    terukur: PENA/JUDP yang hilang memang tidak punya kalimat pendukung di teks
    (nama hakim ketua tidak ada di 18 berkas), ARTV hilang persis pada 21
    dokumen tanpa PDF, dan bentuk vonis yang tidak berpola `PIDANA PENJARA
    SELAMA ...` tidak dipaksakan.

## Jebakan yang Sudah Pernah Kena

- Nomor perkara di badan putusan sering ter-redaksi sebagian (`XXX/PID.SUS/2025/PN`)
  dan sebagian penuh. Pola longgar seperti `NOMOR X` menghitung 17 berkas;
  yang benar-benar ter-redaksi jauh lebih sedikit. Untuk angka redaksi, pakai
  potongan judul yang ketat, jangan pola longgar.
- Berkas PDF lebih banyak dari putusan unik (195 berkas vs 187 putusan) karena
  ada grup berkas ganda; isi tiap grup sudah diperiksa identik via hash.
- Satu berkas pidana khusus tidak memuat kata "PN Ngw" sama sekali, identitasnya
  dipastikan dari metadata.
- Tabel 12 entitas pada PDF tugas tersimpan sebagai gambar, teksnya tidak bisa
  diekstrak langsung; perlu OCR render halaman.
- Notebook 03 memakai 11 label (menyimpang dari skema 12) — jangan menyalin
  daftar label dari notebook 03.
- `resource/IE/` adalah materi dosen dan read-only: verifikasi lewat salinan di
  `/tmp`, jangan sunting berkas aslinya.
- Notebook 04 pernah dibangun lewat skrip builder di `/tmp` yang bisa hilang
  kapan saja. Sumber kebenaran tetap notebook-nya sendiri, jadi untuk perubahan
  berikutnya sunting notebook langsung.
- Cek urutan IOB harus per (`doc`, `sentence`). Menghitungnya pada seluruh
  dokumen membuat penanda `I_` di awal fragmen dianggap pelanggaran: pernah
  terbaca 9.572 "pelanggaran" padahal aturan sel [23] melaporkan 0.
- Cakupan entitas jangan diukur dengan pola "penanda + nama" saja. Ukur ulang
  kenapa tiap dokumen gagal terlabel (kata peran, redaksi, atau teks yang
  memang tidak memuat), karena penyebabnya menentukan apakah aturan perlu
  diubah atau tidak.
- Uji mutu label entitas orang dengan matriks kekhasan peran: bandingkan token
  span terhadap kolom peran metadata (`hakim_ketua`, `hakim_anggota`,
  `panitera`, `penuntut_umum`, `terdakwa`). Rentang nama yang menyerobot blok
  peran berikutnya langsung ketahuan: ADVO sebelum diperbaiki 66% span-nya
  memuat token hakim, padahal label lain hanya 1–2%.

## Perintah Verifikasi

```bash
# jalankan ulang notebook deliverable (kernel enWebmining)
# NB = nomor tugas, mis. 04-Dataset-230411100197.ipynb
cd notebook/IE && ../../.venv/bin/jupyter nbconvert --to notebook --execute \
  --inplace --ExecutePreprocessor.kernel_name=enwebmining \
  --ExecutePreprocessor.timeout=900 <NB>.ipynb

# PDF hasil
cd notebook/IE && ../../.venv/bin/jupyter nbconvert --to webpdf \
  --output-dir ../../data/IE --output IE-<Tugas>-230411100197 <NB>.ipynb

# cek statis (dari root proyek)
.venv/bin/ruff check scripts notebook
.venv/bin/ruff format --check scripts
.venv/bin/pyright scripts
.venv/bin/pyrefly check
```

Cek tambahan sebelum menyerahkan: satu output per sel kode ber-print, tidak ada
nama orang atau nomor perkara di output notebook yang di-publish, heading
maksimal level 3 dan maksimal 4 kata.

## Angka Volatil

Diverifikasi dari notebook 04 yang dieksekusi 2026-10-21 (setelah perbaikan
ADVO/PROS); angka bisa berubah kalau korpus atau anotasi diubah, jadi selalu
cek ulang dari output.

- 208 putusan (Pid.B 134, Pid.Sus 68, Pid.C 6); 187 ber-text PDF + 21 dari
  metadata; dataset anotasi 1.223.429 baris × 4 kolom; token `O` 1.183.973
  (96,77%).
- Berkas: 195 PDF (187 unik, 8 grup ganda identik), 187 TXT cache. PDF
  deliverable `IE-Dataset-230411100197.pdf`: 16 halaman.
- Cakupan entitas dari 208 dokumen: VERN 208, DEFN 208, JUDG 208, TIMV 207,
  REGI 206, PROS 204, CRIA 192, JUDP 190, ARTV 187, PUNI 182, ADVO 66,
  PENA 154. Sebelum perbaikan ADVO/PROS angkanya 51 dan 172; angka ADVO 179
  pernah muncul tetapi gugur saat verifikasi (lihat jebakan matriks peran).

## Item Terbuka

- **Pengiriman T4 ke GCR** belum dilakukan; yang dikirim hanya
  `dataset/PN-NGW-230411100197.csv` (42 MB) dan
  `dataset/PN-NGW-230411100197.txt`. Nama kedua pemeriksa ada di TXT itu dan di
  `dataset/pemeriksa.txt`, tidak di berkas yang dilacak git.
- Notebook 03 masih memakai label `JUG`; menyelaraskan ke `JUDG` belum
  dikerjakan karena di luar lingkup Tugas 04.
- Peringatan statis pra-ada di `scripts/run_crawl.py:112` (di luar lingkup IE).
