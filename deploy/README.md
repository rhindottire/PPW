---
title: News Classifier
emoji: 📰
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 6.15.0
app_file: app.py
pinned: false
license: mit
short_description: Klasifikasi berita sport vs finance (skip-gram + naive bayes)
---

# News Classifier

Aplikasi klasifikasi artikel berita ke dalam kategori **sport** atau **finance**.

## Cara pakai

1. Tempel **link artikel** di kolom URL, atau
2. Tempel **teks berita** langsung di kolom teks, lalu tekan Klasifikasi.

Link diambil memakai trafilatura (tanpa bergantung struktur HTML), teks
dibersihkan dengan aturan yang sama persis dengan data latih, diubah menjadi
vektor dengan rata-rata embedding **skip-gram word2vec**, lalu diklasifikasikan
oleh **naive bayes Gaussian**.

## Model

Artefak dilatih pada 200 artikel detik (sport 100, finance 100):

- `models/word2vec.model` — skip-gram word2vec (window 5, dimensi 100)
- `models/gnb.joblib` — Gaussian naive bayes
- `models/protected.json` — daftar nama yang dilindungi saat pembersihan
- `models/labels.json` — urutan kelas classifier

Skor validasi pada 40 dokumen yang tidak pernah menyentuh pelatihan:
akurasi **0.975** (sport F1 0.974, finance F1 0.976).

## Etika crawling

Setiap permintaan jaring sopan: jeda minimal satu detik, user agent jujur, dan
berhenti bila situs menjawab 403/429 — penolakan dicatat, tidak ada jalan
alternatif.