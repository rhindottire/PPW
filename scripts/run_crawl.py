# run_crawl.py
# Crawling data detik.com — sport (100) + finance (100) = 200 artikel
# Kolom output: id, isi_berita, label, url
from pathlib import Path

import re
import time
import requests
import pandas as pd
import trafilatura

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
}
POLITE_DELAY = 1.0  # jeda antar-request (detik)
RETRY = 3  # coba ulang bila koneksi drop
BACKOFF = [1, 2, 4]  # jeda eksponensial per retry (detik)


def log(msg):
    print(msg, flush=True)


def get_urls_from_sitemap(sitemap_url):
    r = requests.get(sitemap_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return re.findall(r"<loc>\s*<!\[CDATA\[\s*([^\]]+?)\s*\]\]>\s*</loc>", r.text)


def collect_article_urls(kanal, limit=100):
    base = f"https://{kanal}.detik.com"
    idx = requests.get(f"{base}/sitemap.xml", headers=HEADERS, timeout=30)
    idx.raise_for_status()
    news_sitemaps = re.findall(r"https?://[^\s<\[]+?sitemap_news\.xml", idx.text)

    urls = set()
    for sm in news_sitemaps:
        try:
            for u in get_urls_from_sitemap(sm):
                urls.add(u)
        except Exception as e:
            log(f"  [skip sitemap] {sm} -> {e}")
        if len(urls) >= limit:
            break
        time.sleep(POLITE_DELAY)
    return list(urls)[:limit]


def crawl_article(url):
    """Ambil teks artikel dengan trafilatura, pakai retry ringan."""
    for attempt in range(RETRY):
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded, include_comments=False)
                if text:
                    return text
        except Exception as e:
            log(f"    [retry {attempt + 1}] {url} -> {str(e)[:60]}")
        if attempt < RETRY - 1:
            time.sleep(BACKOFF[attempt])
    return None


def crawl_many(urls, label):
    results = []
    ok = 0
    for i, url in enumerate(urls, start=1):
        isi = crawl_article(url)
        results.append({"url": url, "isi_berita": isi, "label": label})
        if isi:
            ok += 1
        if i % 10 == 0 or i == len(urls):
            log(f"  [{label}] {i}/{len(urls)} selesai (sukses={ok})")
        time.sleep(POLITE_DELAY)
    return results


def main():
    N = 100
    log("Mengumpulkan URL sport...")
    sport_urls = collect_article_urls("sport", limit=N)
    log(f"  sport: {len(sport_urls)} URL")

    log("Mengumpulkan URL finance...")
    finance_urls = collect_article_urls("finance", limit=N)
    log(f"  finance: {len(finance_urls)} URL")

    log("Crawl sport...")
    sport_rows = crawl_many(sport_urls, "sport")
    log("Crawl finance...")
    finance_rows = crawl_many(finance_urls, "finance")

    all_rows = sport_rows + finance_rows
    df = pd.DataFrame(all_rows)
    df.insert(0, "id", range(1, len(df) + 1))
    df = df[["id", "isi_berita", "label", "url"]]

    # Hapus baris yang gagal (isi_berita None)
    df_clean = df.dropna(subset=["isi_berita"]).reset_index(drop=True)

    log(f"\n=== HASIL ===")
    log(f"Total di-crawl : {len(df)}")
    log(f"Valid (ada isi): {len(df_clean)}")
    log(f"Gagal          : {len(df) - len(df_clean)}")
    log("\nDistribusi label:\n" + str(df_clean["label"].value_counts().to_string()))

    df_clean.to_csv(DATA_DIR / "crawling_detik.csv", index=False, encoding="utf-8")
    df_clean.to_json(
        DATA_DIR / "crawling_detik.json",
        orient="records",
        force_ascii=False,
        indent=2,
    )
    log(f"\nFile tersimpan: {DATA_DIR}/crawling_detik.csv dan crawling_detik.json")


if __name__ == "__main__":
    main()
