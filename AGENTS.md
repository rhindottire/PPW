# PPW — Pencarian & Penambangan Web

## Project Info
- Mata kuliah praktikum Information Retrieval / Web Search & Mining
- Python 3.14.7, virtual environment di `.venv/`
- Kernel Jupyter: `enWebmining`

## Perintah Penting
- Aktifkan venv: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Jalankan Jupyter: `jupyter lab`
- Crawl ulang: `python run_crawl.py`

## Konvensi Kode
- Semua kode Python, bukan TypeScript/JavaScript
- Gunakan `trafilatura` untuk ekstraksi konten web (bukan requests+bs4 untuk ekstraksi utama)
- Format output DataFrame: kolom `id`, `isi_berita`, `label`, `url`
- Jangan crawl tanpa jeda (polite delay minimal 1 detik)
- Data sudah tersedia di `crawling_detik.csv` — jangan crawl ulang kecuali diminta
- Selalu gunakan `with_metadata=True` atau `include_comments=False` pada trafilatura

## Struktur Project
- `crawling_detik.ipynb` — notebook utama (kernel: enWebmining)
- `run_crawl.py` — script crawling standalone
- `crawling_detik.csv/.json` — hasil crawl 200 artikel (100 sport + 100 finance)
- `requirements.txt` — daftar paket ter-pin
- `ENVIRONMENT.md` — dokumentasi lengkap environment

## Library Utama
- `trafilatura` — ekstraksi teks dari web
- `pandas` — manipulasi data
- `scikit-learn` — TF-IDF, clustering
- `nltk` / `spacy` — NLP
- `Sastrawi` — stemming bahasa Indonesia
- `rank-bm25` — ranking dokumen
- `wordcloud` — visualisasi frekuensi kata
- `torch` — deep learning (CUDA-enabled)

## Aturan Kelas
- Kernel Jupyter wajib `enWebmining` (bukan python3 default)
- Tidak boleh menghapus data crawl yang sudah ada tanpa izin
- Gunakan User-Agent yang sopan saat crawling
- Sertakan etika crawling di setiap notebook
