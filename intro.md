# PPW — Web Search & Mining

Proyek praktikum mata kuliah **Information Retrieval / Web Search & Mining**.

Buku ini menyajikan hasil **crawling data berita detik.com** (200 artikel:
100 `sport` + 100 `finance`) beserta alur pengumpulan datanya. Seluruh ekstraksi
teks artikel dilakukan dengan **`trafilatura`**, mengikuti etika crawling yang
berlaku.

## Isi buku

- **Crawling Data detik.com — Sport & Finance** — notebook utama (`crawling_detik.ipynb`,
  kernel `enWebmining`) yang memuat kode crawling, validasi dataset, dan contoh
  hasil artikel.
- **Etika Crawling** — prinsip `robots.txt`, politeness delay, dan batasan
  penggunaan data yang dipatuhi dalam proyek ini.

## Dataset

| Label    | Jumlah | ID     |
|----------|--------|--------|
| `sport`  | 100    | 1–100  |
| `finance`| 100    | 101–200|

Berkas `crawling_detik.csv` dan `crawling_detik.json` menyimpan hasil crawl
dengan kolom `id`, `isi_berita`, `label`, dan `url`.

> Dataset sudah tersedia dan **tidak perlu di-crawl ulang**. Notebook bagian
> bawah memuat hasil dari berkas agar hemat dan aman dari koneksi yang tidak
> stabil.

## Repository

Kode sumber penuh, konfigurasi buku, dan berkas pendukung tersedia di
[https://github.com/rhindottire/PPW](https://github.com/rhindottire/PPW).