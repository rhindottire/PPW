"""Gradio app for sport/finance news classification."""

import time
import urllib.error
import urllib.request
from urllib.parse import urlparse

import gradio as gr
import spaces
import trafilatura
from serve import classify, describe, sentence_tokens

USER_AGENT = "NewsClassifier-PPW/0.1 (+academic course work)"
BASE_LIMITS = {
    "policy": "at least one second between requests, honest user agent, "
    "stop on 403/429 and record the refusal",
    "delay_seconds": 1.0,
}


def fetch_text(url):
    if not urlparse(url).scheme:
        return None, "URL harus diawali http:// atau https://."
    time.sleep(BASE_LIMITS["delay_seconds"])
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            if response.status in (403, 429):
                return None, (
                    f"Situs menolak akses (HTTP {response.status}). "
                    "Penolakan dicatat; tidak ada jalan alternatif."
                )
            html = response.read()
    except urllib.error.HTTPError as error:
        if error.code in (403, 429):
            return None, (
                f"Situs menolak akses (HTTP {error.code}). "
                "Penolakan dicatat; tidak ada jalan alternatif."
            )
        return None, f"Gagal mengambil halaman (HTTP {error.code})."
    except urllib.error.URLError as error:
        return None, f"Gagal mengambil halaman ({error.reason})."
    text = trafilatura.extract(html, include_comments=False, with_metadata=False)
    if not text:
        return None, "Konten artikel tidak ditemukan pada halaman."
    return text, None


def build_result(value, source):
    label, scores = classify_gpu(value)
    stats = describe(value)
    lines = [
        f"**Kategori: {label}**",
        f"- Sport: {scores.get('sport'):.3f}",
        f"- Finance: {scores.get('finance'):.3f}",
        (
            f"- Sumber: {source} | kalimat {stats['sentences']}, "
            f"token {stats['tokens']}, dikenali kosakata {stats['words in vocabulary']}"
        ),
        "",
        (
            f"Model skip-gram + naive bayes dipakai untuk teks bersih "
            f"{len(sentence_tokens(value))} kalimat."
        ),
    ]
    return "\n".join(lines)


@spaces.GPU(duration=10)
def classify_gpu(value):
    return classify(value)


def predict(url, text):
    if url.strip() and not text.strip():
        content, message = fetch_text(url)
        if content is None:
            return message
        return build_result(content, "URL")
    if text.strip():
        return build_result(text.strip(), "teks tempel")
    return "Isi salah satu kolom: URL berita atau teks yang ditempel."


with gr.Blocks(title="News Classifier") as demo:
    gr.Markdown(
        "# Klasifikasi Berita Sport vs Finance\n"
        "Tempel link artikel (diambil dengan trafilatura) atau tempel langsung "
        "teksnya. Model: skip-gram word2vec + naive bayes, "
        "fokus pada berita detik."
    )
    with gr.Row():
        url_box = gr.Textbox(label="URL berita", lines=2)
        text_box = gr.Textbox(label="Teks berita (tempel)", lines=8)
    button = gr.Button("Klasifikasi")
    output = gr.Markdown(label="Hasil")
    ethics = gr.Markdown(
        f"Etika crawling: {BASE_LIMITS['policy']}. Data pribadi tidak dikumpulkan."
    )
    button.click(predict, inputs=[url_box, text_box], outputs=output)

if __name__ == "__main__":
    demo.launch()
