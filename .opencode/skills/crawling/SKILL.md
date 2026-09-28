---
name: crawling
description: Polite web crawling workflow with trafilatura. Step-by-step collection of article data from websites.
---

## Yang saya lakukan
- Mengumpulkan URL dari sitemap atau halaman indeks
- Mengekstrak konten teks dari halaman web menggunakan trafilatura
- Menyimpan hasil ke DataFrame (kolom: id, isi_berita, label, url)
- Mengekspor ke CSV/JSON

## Saat menggunakan saya
Gunakan skill ini saat kamu perlu crawl data dari web, mengumpulkan artikel, atau scraping konten.

## Workflow Standar

### 1. Aktifkan venv
```bash
source .venv/bin/activate
```

### 2. Kumpulkan URL dari Sitemap
```python
import re
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PPWCrawler/1.0)"}
POLITE_DELAY = 1.0  # minimal 1 detik antar request

def get_urls_from_sitemap(sitemap_url):
    r = requests.get(sitemap_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return re.findall(r"<loc>\s*<!\[CDATA\[\s*([^\]]+?)\s*\]\]>\s*</loc>", r.text)
```

### 3. Crawl Konten dengan trafilatura
```python
import trafilatura
import time

def crawl_article(url, retry=3, backoff=(1, 2, 4)):
    for attempt in range(retry):
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(
                    downloaded, with_metadata=True, include_comments=False
                )
                if text:
                    return text
        except Exception:
            pass
        if attempt < retry - 1:
            time.sleep(backoff[attempt])
    return None
```

### 4. Simpan ke DataFrame
```python
import pandas as pd

df = pd.DataFrame(results)
df.insert(0, "id", range(1, len(df) + 1))
df = df[["id", "isi_berita", "label", "url"]]
df.to_csv("hasil_crawl.csv", index=False)
```

## Tips Penting
- Skrip kanonik untuk ulang-crawl: `scripts/run_crawl.py` — jaga workflow ini tetap sinkron dengan skrip tersebut
- Selalu beri jeda minimal 1 detik antar request (polite crawling)
- Gunakan retry dengan backoff eksponensial
- Sertakan User-Agent yang sopan
- Cek robots.txt sebelum crawl
- Simpan juga URL asli untuk referensi
