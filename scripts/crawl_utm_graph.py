"""Recursive BFS Multi-Hop Crawler for UTM Subdomains Graph.

Complies with PPW ethics:
- User-Agent identification
- Polite delay >= 1.0s between requests
- Resilient SSL & timeout handling
- Unbounded queue-based exploration of all discovered *.trunojoyo.ac.id subdomains
- Outputs directed edge graph to data/Web-Mining/utm_subdomains_graph.json
"""

import json
import re
import time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "Web-Mining" / "utm_subdomains_graph.json"

USER_AGENT = "PPW-UTM-PageRankBot/1.0 (+https://trunojoyo.ac.id; student-research)"
HEADERS = {"User-Agent": USER_AGENT}
TIMEOUT = 7
REQUEST_DELAY = 1.0
MAX_INTERNAL_PAGES_PER_HOST = 2  # Homepage + up to 2 shallow navigation pages

INITIAL_SEEDS = [
    "https://www.trunojoyo.ac.id/",
    "https://teknik.trunojoyo.ac.id/",
    "https://feb.trunojoyo.ac.id/",
    "https://pertanian.trunojoyo.ac.id/",
    "https://hukum.trunojoyo.ac.id/",
    "https://fisib.trunojoyo.ac.id/",
    "https://fip.trunojoyo.ac.id/",
    "https://fik.trunojoyo.ac.id/",
    "https://fk.trunojoyo.ac.id/",
    "https://siakad.trunojoyo.ac.id/",
    "https://lppm.trunojoyo.ac.id/",
    "https://lpmpp.trunojoyo.ac.id/",
    "https://library.trunojoyo.ac.id/",
    "https://pmb.trunojoyo.ac.id/",
    "https://pta.trunojoyo.ac.id/",
    "https://journal.trunojoyo.ac.id/",
    "https://tik.trunojoyo.ac.id/",
    "https://karir.trunojoyo.ac.id/",
    "https://asrama.trunojoyo.ac.id/",
    "https://pusatbahasa.trunojoyo.ac.id/",
    "https://spi.trunojoyo.ac.id/",
    "https://jdih.trunojoyo.ac.id/",
    "https://ppid.trunojoyo.ac.id/",
]


def normalize_domain(netloc: str) -> str:
    """Normalize domain name by stripping ports and www prefixes."""
    host = netloc.split(":")[0].lower().strip()
    if host.startswith(("www.", "www2.")):
        host = host.split(".", 1)[1]
    return host


def is_utm_domain(host: str) -> bool:
    """Check if host belongs to trunojoyo.ac.id ecosystem and is a functional web domain."""
    if not (host == "trunojoyo.ac.id" or host.endswith(".trunojoyo.ac.id")):
        return False
    if re.search(
        r"^(cdn|mail|webmail|static|ns\d*|cpanel|webdisk|autodiscover)\.", host
    ):
        return False
    # Avoid IP-based or malformed domains
    return not any(c in host for c in (" ", "/", ":", "@", "%"))


def fetch_url(session: requests.Session, url: str) -> tuple[int, str, str]:
    """Fetch URL with HTTPS first and HTTP fallback, returning (status, text, final_url)."""
    try:
        resp = session.get(
            url, headers=HEADERS, timeout=TIMEOUT, verify=False, allow_redirects=True
        )
        return resp.status_code, resp.text, resp.url
    except (requests.RequestException, OSError):
        # If https failed, attempt plain http
        if url.startswith("https://"):
            http_url = "http://" + url[8:]
            try:
                resp = session.get(
                    http_url,
                    headers=HEADERS,
                    timeout=TIMEOUT,
                    verify=False,
                    allow_redirects=True,
                )
                return resp.status_code, resp.text, resp.url
            except (requests.RequestException, OSError):
                pass
        return 0, "", url


def parse_page_links(
    source_host: str, source_url: str, html_content: str
) -> tuple[set[str], list[str]]:
    """Extract external UTM subdomains and candidate internal navigation URLs."""
    external_targets: set[str] = set()
    internal_candidates: list[str] = []

    soup = BeautifulSoup(html_content, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        href_val = a_tag.get("href")
        if (
            not isinstance(href_val, str)
            or not href_val
            or href_val.startswith(("#", "javascript:", "mailto:", "tel:"))
        ):
            continue

        resolved = urljoin(source_url, href_val)
        parsed = urlparse(resolved)
        if parsed.scheme not in ("http", "https"):
            continue

        target_host = normalize_domain(parsed.netloc)
        if is_utm_domain(target_host):
            if target_host != source_host:
                external_targets.add(target_host)
            else:
                # Internal link on the same host: filter for informative navigation pages
                path_lower = parsed.path.lower()
                is_nav_path = any(
                    k in path_lower
                    for k in (
                        "profil",
                        "tentang",
                        "layanan",
                        "link",
                        "tautan",
                        "fakultas",
                        "kontak",
                        "unit",
                        "panduan",
                    )
                )
                is_not_binary = not any(
                    resolved.endswith(ext)
                    for ext in (".pdf", ".jpg", ".png", ".zip", ".docx")
                )
                if (
                    is_nav_path
                    and resolved not in internal_candidates
                    and is_not_binary
                ):
                    internal_candidates.append(resolved)

    return external_targets, internal_candidates


def save_graph_checkpoint(nodes: set[str], edges: set[tuple[str, str]]) -> None:
    """Save graph data to JSON file."""
    sorted_nodes = sorted(nodes)
    sorted_edges = sorted([[u, v] for u, v in edges if u in nodes and v in nodes])

    node_indices = {name: idx for idx, name in enumerate(sorted_nodes)}
    n = len(sorted_nodes)
    adj_matrix = [[0] * n for _ in range(n)]
    for u, v in sorted_edges:
        adj_matrix[node_indices[u]][node_indices[v]] = 1

    graph_data = {
        "nodes": sorted_nodes,
        "edges": sorted_edges,
        "adjacency_matrix": adj_matrix,
        "metadata": {
            "node_count": n,
            "edge_count": len(sorted_edges),
            "density": round(len(sorted_edges) / (n * (n - 1)), 4) if n > 1 else 0.0,
            "crawled_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "crawler": "Recursive BFS Multi-Hop Crawler",
        },
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2)


def crawl_utm_network() -> dict:
    """Execute Unbounded Multi-Hop BFS crawl across all discovered UTM subdomains."""
    session = requests.Session()

    queue: deque[str] = deque()
    discovered_hosts: set[str] = set()
    crawled_hosts: set[str] = set()
    edges: set[tuple[str, str]] = set()

    # Seed initial queue
    for seed in INITIAL_SEEDS:
        host = normalize_domain(urlparse(seed).netloc)
        if is_utm_domain(host) and host not in discovered_hosts:
            discovered_hosts.add(host)
            queue.append(host)

    print(f"=== Starting Unbounded BFS Crawl ===\nInitial seeds in queue: {len(queue)}")

    iteration = 0
    while queue:
        current_host = queue.popleft()
        if current_host in crawled_hosts:
            continue

        iteration += 1
        crawled_hosts.add(current_host)
        home_url = f"https://{current_host}/"
        print(
            f"[{iteration}] Crawling {current_host} (Queue: {len(queue)} | Nodes: {len(discovered_hosts)} | Edges: {len(edges)})"
        )

        status, html, final_url = fetch_url(session, home_url)
        time.sleep(REQUEST_DELAY)

        if status == 200 and html:
            ext_targets, internal_pages = parse_page_links(
                current_host, final_url, html
            )

            # Crawl up to MAX_INTERNAL_PAGES_PER_HOST shallow navigation pages on same host
            for int_url in internal_pages[:MAX_INTERNAL_PAGES_PER_HOST]:
                sub_status, sub_html, sub_final = fetch_url(session, int_url)
                time.sleep(REQUEST_DELAY)
                if sub_status == 200 and sub_html:
                    sub_ext_targets, _ = parse_page_links(
                        current_host, sub_final, sub_html
                    )
                    ext_targets.update(sub_ext_targets)

            # Record directed edges and enqueue newly discovered hosts
            new_hosts_found = 0
            for target_host in ext_targets:
                edges.add((current_host, target_host))
                if target_host not in discovered_hosts:
                    discovered_hosts.add(target_host)
                    queue.append(target_host)
                    new_hosts_found += 1

            print(
                f"  -> {current_host}: {len(ext_targets)} out-links to other subdomains (+{new_hosts_found} new subdomains enqueued)"
            )
        else:
            print(f"  -> {current_host}: Inactive/unresponsive (HTTP {status})")

        # Periodically save checkpoint every 5 subdomains
        if iteration % 5 == 0:
            save_graph_checkpoint(discovered_hosts, edges)

    # Final save
    save_graph_checkpoint(discovered_hosts, edges)
    print("\n=== Unbounded BFS Crawl Completed ===")
    print(f"Total Discovered Subdomains: {len(discovered_hosts)}")
    print(f"Total Crawled Subdomains: {len(crawled_hosts)}")
    print(f"Total Directed Edges: {len(edges)}")

    with open(OUTPUT_FILE, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    crawl_utm_network()
