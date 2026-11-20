# Deployment Services — Web Mining (PPW)

Direktori ini memuat modul deployment untuk tugas mata kuliah Web Search & Mining (PPW), dirancang portabel untuk dioperasikan pada **Server Warga Laboratorium** maupun **Server Kampus**.

---

## 1. UTM PageRank Research Workbench (Tugas 7)

Aplikasi riset dan analisis keterhubungan web berbasis algoritma PageRank untuk seluruh website dan subdomain di lingkungan **Universitas Trunojoyo Madura** (`*.trunojoyo.ac.id`), dirancang berstandar akademis workbench ilmiah (gaya Gephi / Stanford SNAP / Observable).

### Fitur Utama
- **Topologi Jaringan 2D Terukur**: Visualisasi graf berarah berbasis D3/Canvas dengan radius simpul sebanding skor PageRank, panah arah relasi (*directed edges*), dan isolasi subgraf 1-hop perujuk (*inbound*) dan target (*outbound*).
- **Dekomposisi Skor Matematis**: Rincian formula PageRank per perujuk masuk $d \frac{PR(j)}{k_{\text{out}}(j)}$, bobot basis teleportasi acak $\frac{1-d}{N}$, dan kompensasi simpul buntu (*dead-end*).
- **What-If Link Simulator**: Simulasi penambahan/pemutusan tautan masuk hipotetis untuk memprediksi kenaikan skor ($\Delta PR$) dan perubahan peringkat.
- **Laboratorium Power Iteration**: Stepper langkah-demi-langkah ($r^{(0)} \to r^{(1)} \dots \to r^{(12)}$), kurva konvergensi residual L1 norm error terhadap ambang batas $\epsilon = 10^{-7}$, dan inspeksi matriks transisi kolom-stokastik $M$.
- **Leaderboard & Ekspor Data**: Tabel peringkat otoritas komprehensif dengan fitur filter/pencarian serta tombol unduh CSV dan JSON.
- **Konsol Live Crawler**: Antarmuka pengujian perayapan langsung (*live crawl*) dengan etika jeda sopan $\ge 1$ detik.

### Cara Menjalankan di Server Warga Laboratorium

#### A. Aplikasi Web Utama (FastAPI + D3 Scientific SPA) — Direkomendasikan
Aplikasi web modern berbasis arsitektur SPA dengan tema Dark Slate netral, tipografi monospace tabular, tanpa emoji dekoratif, kanvas graf 2D terukur, stepper iterasi, serta kalkulasi dinamis:
```bash
# Menjalankan langsung via virtualenv
.venv/bin/python deploy/server.py

# Atau menggunakan Uvicorn
.venv/bin/uvicorn deploy.server:app --host 0.0.0.0 --port 8000
```
Buka peramban pada:
- Lokal: `http://localhost:8000`
- Jaringan LAN Laboratorium: `http://<IP_SERVER_LAB>:8000`

#### B. Alternatif Streamlit
```bash
.venv/bin/streamlit run deploy/app_pagerank.py --server.port 8501
```

### Panduan Migrasi ke Server Kampus
Aplikasi FastAPI siap dijalankan secara persisten di server kampus Linux (Ubuntu/Debian/AlmaLinux) menggunakan systemd dan Nginx reverse proxy:

#### A. Konfigurasi Systemd Service
Buat berkas `/etc/systemd/system/pagerank-utm.service`:
```ini
[Unit]
Description=UTM Web Graph and PageRank Intelligence Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/ppw
ExecStart=/var/www/ppw/.venv/bin/uvicorn deploy.server:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Aktifkan service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now pagerank-utm
sudo systemctl status pagerank-utm
```

#### B. Konfigurasi Reverse Proxy Nginx
Tambahkan blok server Nginx pada `/etc/nginx/sites-available/pagerank-utm`:
```nginx
server {
    listen 80;
    server_name pagerank.trunojoyo.ac.id;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 2. News Classifier (Tugas 5)

Aplikasi klasifikasi artikel berita ke dalam kategori **sport** atau **finance** menggunakan representasi rata-rata embedding **skip-gram word2vec** dan pengklasifikasi **Gaussian Naive Bayes**.

### Cara Menjalankan
```bash
python deploy/app.py
```
Aplikasi berjalan pada server lokal Gradio (port default 7860) atau Hugging Face Spaces.
