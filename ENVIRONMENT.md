# ENVIRONMENT — Pencarian & Penambangan Web (PPW)

Dokumentasi lengkap tentang *virtual environment* dan seluruh paket Python yang
terpasang untuk proyek ini. Dibuat untuk kebutuhan praktikum **Pencarian &
Penambangan Web** (Web Search & Mining / Information Retrieval).

---

## 1. Informasi Python & Virtual Environment

| Item | Nilai |
|------|-------|
| Direktori proyek | `/home/kreideprinz/Documents/PPW` |
| Lokasi venv | `/home/kreideprinz/Documents/PPW/.venv` |
| Versi Python | **3.14.7** |
| Path Python base | `/usr/bin/python3.14` |
| File konfigurasi | `.venv/pyvenv.cfg` |
| `include-system-site-packages` | `false` (terisolasi total dari system) |

### Cara aktivasi venv
```bash
# Linux / macOS (bash, zsh)
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate

# Cek Python aktif
which python        # -> .../.venv/bin/python
```

Setelah diaktifkan, prompt shell biasanya bertambah prefix `(.venv)`.

### Cara menonaktifkan
```bash
deactivate
```

---

## 2. Struktur Folder `.venv`

```
.venv/
├── bin/              # eksekutabel: python, pip, skrip aktivasi (activate*, Activate.ps1)
├── include/          # header C (jarang disentuh)
├── lib/python3.14/   # situs tempat semua paket ter-install (site-packages)
├── lib64 -> lib      # symlink (Linux)
└── pyvenv.cfg        # penanda venv + konfigurasi
```

> `.gitignore` di dalam `.venv/` otomatis membuat folder venv tidak ikut ter-commit ke git.

---

## 3. Jupyter Kernel — `enwebmining` (aturan kelas)

Agar semua paket di venv ini tersedia di **Jupyter Notebook**, venv ini telah
didaftarkan sebagai **kernel Jupyter** bernama `enwebmining`.

> **PENTING (perbaikan):** Kernel default `python3` JupyterLab sebelumnya
> menunjuk ke Python **sistem** (`/usr/lib/python3.14`), sehingga `trafilatura`
> tidak ditemukan. Kini kernel `python3` telah diarahkan ke venv ini lewat
> file `.venv/share/jupyter/kernels/python3/kernel.json`. Jadi default JupyterLab
> dan kernel `enWebmining` sama-sama menggunakan venv.

### Perintah yang dijalankan (saat setup)
```bash
python -m ipykernel install --user --name=enwebmining --display-name="enWebmining"
```

| Argumen | Arti |
|---------|------|
| `python -m ipykernel` | jalankan modul ipykernel |
| `install` | daftarkan kernel ke Jupyter |
| `--user` | daftar untuk user saat ini (tanpa perlu akses root) |
| `--name=enwebmining` | ID internal kernel (unik, tanpa spasi) |
| `--display-name="enWebmining"` | nama yang tampil di dropdown Jupyter |

Lokasi registrasi: `~/.local/share/jupyter/kernels/enwebmining`

### Cara menggunakan kernel
1. Jalankan `jupyter notebook` (atau `jupyter lab`) dari terminal.
2. Saat membuat notebook baru: **Kernel → Change kernel → pilih `enWebmining`.**
3. Semua paket di bawah (trafilatura, scrapy, torch, dll.) langsung bisa di-import.

### Verifikasi kernel terdaftar
```bash
python -m jupyter kernelspec list
```
Output menunjukkan `enwebmining` di daftar.

### Menghapus kernel (jika perlu)
```bash
python -m jupyter kernelspec uninstall enwebmining
```

---

## 4. Daftar Paket Python Terpasang

Versi di bawah adalah **versi ter-pin** yang aktif di venv. Daftar diregenerate
kapan pun dengan: `.venv/bin/pip freeze`.

### Grup A — Prioritas Kelas (Ekstraksi Konten Web)

| Package | Versi | Fungsi | Alasan dipasang |
|---------|-------|--------|-----------------|
| `trafilatura` | 2.2.0 | Ekstraksi teks utama & metadata dari halaman web/artikel secara otomatis | **Wajib (aturan kelas)**. Memuat konten bersih dari halaman tanpa tag HTML/sampah. Sekaligus membawa `justext`, `courlan`, `htmldate` sebagai pendukung. |

### Grup B — Fondasi Web Scraping & Data

| Package | Versi | Fungsi | Alasan dipasang |
|---------|-------|--------|-----------------|
| `requests` | 2.34.2 | HTTP client untuk mengambil halaman web | Dasar scraping: mengambil sumber HTML. |
| `beautifulsoup4` | 4.15.0 | Parsing & navigasi struktur HTML/XML | Menyaring elemen-elemen dari HTML yang diambil. |
| `lxml` | 6.1.3 | Parser HTML/XML berkecepatan tinggi | Backend parsing bs4, jauh lebih cepat & stabil. |
| `pandas` | 3.0.5 | Manipulasi data tabular (DataFrame) | Perantara menyimpan/membersihkan hasil scraping. |
| `numpy` | 2.5.2 | Komputasi numerik berbasis array | Fondasi semua perhitungan & dependensi banyak library. |

### Grup C — Jupyter / Kernel

| Package | Versi | Fungsi | Alasan dipasang |
|---------|-------|--------|-----------------|
| `ipykernel` | 7.3.0 | Jembatan Python ↔ Jupyter | **Wajib (aturan kelas)** untuk mendaftarkan venv sebagai kernel. |
| `ipython` | 9.17.1 | Interpreter interaktif | Kernel Jupyter berjalan di atas IPython. |
| `jupyterlab` | 4.6.3 | Antarmuka Jupyter Notebook modern | Tempat kerja utama untuk tugas (notebook `crawling_detik.ipynb`). |

### Grup D — Crawling & Scraping Lanjutan

| Package | Versi | Fungsi | Alasan dipasang |
|---------|-------|--------|-----------------|
| `scrapy` | 2.18.0 | Framework crawler/scraper berskala besar | Crawling multi-halaman dengan pipeline & scheduling (mirip mesin pencari). |
| `selenium` | 4.48.0 | Otomasi browser | Scraping situs dinamis (JavaScript) yang tak bisa diambil `requests`. |
| `webdriver-manager` | 4.1.2 | Kelola driver browser otomatis | Men-download & men-setting chromedriver tanpa install manual. |

### Grup E — Information Retrieval & Text Mining

| Package | Versi | Fungsi | Alasan dipasang |
|---------|-------|--------|-----------------|
| `rank-bm25` | 0.2.2 | Implementasi algoritma ranking BM25 | Ranking dokumen standar di Information Retrieval. |
| `scikit-learn` | 1.9.0 | Machine learning umum | `TfidfVectorizer`, clustering, klasifikasi teks. |
| `scipy` | 1.18.1 | Komputasi ilmiah | Dependensi scikit-learn & operasi matriks. |
| `nltk` | 3.10.3 | NLP klasik | Tokenisasi, stemming, stopword. |
| `spacy` | 3.8.16 | NLP modern & cepat | Tokenisasi, POS tagging, entity recognition, model bahasa. |
| `wordcloud` | 1.9.6 | Visualisasi frekuensi kata | Membuat wordcloud dari hasil mining. (membawa `matplotlib`, `pillow`) |

### Grup F — NLP Bahasa Indonesia

| Package | Versi | Fungsi | Alasan dipasang |
|---------|-------|--------|-----------------|
| `Sastrawi` | 1.0.1 | Stemmer Bahasa Indonesia | **Konteks praktikum Indonesia**: stemming kata berbahasa Indonesia. |

### Grup G — Deep Learning

| Package | Versi | Fungsi | Alasan dipasang |
|---------|-------|--------|-----------------|
| `torch` | 2.14.0+cu130 | Framework deep learning (PyTorch) | Deep learning & pattern recognition pada data teks/gambar hasil mining. |
| `torchvision` | 0.29.0+cu130 | Vision library untuk PyTorch (dataset, transformasi) | Pendukung model visi/CNN bila materi menyentuh gambar. |

> Grup ini membawa banyak dependensi CUDA/NVIDIA (`nvidia-cublas`, `cudnn`,
> `cuda-toolkit`, `triton`, dll.) otomatis.

### Dependensi otomatis (terpasang sebagai turunan)

`courlan`, `justext`, `htmldate` (dari trafilatura); `joblib`, `threadpoolctl`
(dari sklearn); `thinc`, `blis`, `cymem`, `preshed`, `murmurhash`, `wasabi`,
`srsly` (dari spacy); `lxml`, `js2py`-pendukung scrapy dsb. Tidak perlu
di-uninstall manual — pip mengelolanya otomatis.

---

## 5. Deep Learning — Status & Panduan

### Status saat setup
- **PyTorch (torch)**: **TERPASANG** — versi `2.14.0+cu130` (dengan dukungan CUDA).
- **torchvision**: **TERPASANG** — versi `0.29.0+cu130`.
- CUDA tersedia (`torch.cuda.is_available()` = `True`).

Verifikasi:
```bash
.venv/bin/python -c "import torch, torchvision; print(torch.__version__, torchvision.__version__, torch.cuda.is_available())"
```

> Catatan: instalasi awal beberapa kali gagal karena ukuran wheel (554 MB) +
> koneksi lambat. Berhasil saat jaringan stabil. Jika perlu ulang install:
> ```bash
> source .venv/bin/activate
> pip install torch torchvision
> ```

### Framework alternatif (opsional, TIDAK terpasang)
```bash
# TensorFlow — hanya pilih SATU framework (torch ATAU tf), bukan keduanya.
pip install tensorflow
```

---

## 6. Manajemen Paket (Workflow Developer)

### Install semua isi requirements.txt
```bash
pip install -r requirements.txt
```

### Menambah paket baru
```bash
pip install <nama-paket>
```

### Melihat daftar paket terpasang & versinya
```bash
pip list
```

### Synchronize versi ke requirements (regenerate pin)
```bash
pip freeze > requirements.txt
```
> `requirements.txt` di proyek ini disusun **manual per topik** agar mudah
> dibaca. Gunakan `pip freeze` bila ingin daftar mentah (termasuk dependensi).

### Lihat detail paket
```bash
pip show trafilatura
```

---

## 7. Contoh Penggunaan Dasar — trafilatura (prioritas kelas)

```python
import trafilatura

# 1) Ambil HTML dari sebuah halaman
downloaded = trafilatura.fetch_url("https://id.wikipedia.org/wiki/Data_mining")

# 2) Ekstrak teks utama tanpa tag HTML
text = trafilatura.extract(downloaded)
print(text)
```

Fungsi inti lain yang berguna:
- `trafilatura.extract(html, output_format="json")` — output berstruktur.
- `trafilatura.extract(html, with_metadata=True)` — sertakan metadata/header.
- `trafilatura.bare_extraction(html)` — objek berisi teks + judul + tanggal dll.

---

## 8. Tugas Crawling detik.com

### Deskripsi
Mengumpulkan **200 data berita** dari detik.com:
- 100 data pertama: kategori **sport** (label `sport`)
- 100 data berikutnya: kategori **finance** (label `finance`)

### Kolom data wajib
| Kolom | Isi |
|-------|-----|
| `id` | nomor urut integer 1–200 (1–100 = sport, 101–200 = finance) |
| `isi_berita` | teks utama artikel hasil ekstraksi `trafilatura` |
| `label` | kategori berita (`sport` atau `finance`) |

### Cara menjalankan
```bash
# 1) Aktifkan venv
source .venv/bin/activate

# 2) Buka JupyterLab
jupyter lab

# 3) Buka notebook crawling_detik.ipynb, pilih kernel "enWebmining",
#    lalu jalankan semua sel (Kernel -> Restart Kernel and Run All Cells).
```

### Status hasil crawl
> **Sudah selesai dicrawl** — `crawling_detik.csv` & `crawling_detik.json` berisi
> **200 baris** (100 sport + 100 finance). Notebook memuat hasil dari file ini
> (Bagian B) sehingga **tidak perlu meng-crawl ulang**. Crawl ulang opsional
> tersedia di Bagian C (aktifkan `_re_crawl = True`), atau via `run_crawl.py`:
> ```bash
> source .venv/bin/activate
> python run_crawl.py
> ```

### Alur notebook `crawling_detik.ipynb`
- **Bagian A (referensi)** — kode/kegunaan: kumpulkan URL dari sitemap, crawl
  isi via trafilatura. Tidak dijalankan otomatis (agar tidak meng-crawl ulang).
- **Bagian B (utama)** — memuat hasil dari `crawling_detik.csv`/`.json`,
  memeriksa kolom wajib & distribusi label, menampilkan contoh isi berita.
- **Bagian C (opsional)** — crawl ulang 200 artikel bila `_re_crawl = True`.

Alur teknik crawling (untuk referensi ringkas):
1. **Kumpulkan URL** — membaca `sitemap.xml` kanal & `sitemap_news.xml` sub-kanal detik,
   menggabungkan hingga ≥100 URL unik per kategori (tidak melanggar `*/indeks/`).
2. **Crawl isi** — `trafilatura.fetch_url` + `trafilatura.extract` per artikel (dengan retry).
3. **Bangun DataFrame** — kolom wajib `id`, `isi_berita`, `label`.
4. **Ekspor** — simpan `crawling_detik.csv` & `crawling_detik.json`.

### Etika
detik.com mengizinkan crawling (`User-agent: * Allow: /`). Notebook menggunakan
sitemap resmi dan memberikan jeda antar-request. Gunakan semata untuk pembelajaran/tugas.

---

*Terakhir diperbarui: 2026-09-03 · Dibuat otomatis saat setup environment.*
