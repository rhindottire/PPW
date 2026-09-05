# Etika Crawling

Pengumpulan data dalam proyek ini mematuhi prinsip *polite crawling* dan
ketentuan `robots.txt` situs target.

## detik.com `robots.txt`

detik.com mengizinkan crawling (`User-agent: * Allow: /`) dengan beberapa
larangan tertentu (misalnya `*/indeks/`, `*&sortby`). Oleh karena itu notebook
ini **memanfaatkan sitemap resmi detik** untuk mengumpulkan URL artikel, bukan
menebak URL secara acak.

## Politeness delay

Setiap permintaan ke server diberi **jeda minimal 1 detik** (variabel
`POLITE_DELAY` di notebook) dan menggunakan **User-Agent yang sopan**, agar tidak
membebani server detik.com.

## Batasan penggunaan

- Data digunakan **hanya untuk kepentingan pembelajaran / tugas kuliah**.
- Hasil crawl sudah tersedia di `crawling_detik.csv` / `.json`; kode **crawl
  ulang dinonaktifkan** secara bawaan (`_re_crawl = False`) di notebook agar
  tidak mengirim ulang ~200 permintaan tanpa alasan.
- Tidak dilarang meng-crawl, tetapi kami tetap memilih pendekatan yang hemat
  dan ramah terhadap server.

## Ringkasan aturan dalam proyek ini

| Aturan | Penerapan |
|--------|-----------|
| Mematuhi `robots.txt` | Pakai sitemap resmi, hindari halaman terlarang |
| Jeda antar-request | `>= 1 detik` |
| User-Agent sopan | Header User-Agent browser asli |
| Tanpa data ulang | Dataset dibaca dari berkas, re-crawl opsional & nonaktif |
| Untuk pembelajaran | Digunakan untuk kebutuhan tugas kuliah saja |