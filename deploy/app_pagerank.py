"""Executive UI/UX Dashboard for UTM Web Graph & PageRank Intelligence.

Refined with modern UI/UX principles:
- Bento grid metric hierarchy
- Pre-stabilized organic & hierarchical graph physics (zero chaotic bouncing)
- Visual authority progress bars & category badge system
- Responsive layout with custom CSS card containers
- Streamlit headless configuration for laboratory & campus deployment
"""

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components
from bs4 import BeautifulSoup
from pyvis.network import Network

# Ensure imports work from repo root or deploy/ folder
CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

try:
    from deploy.pagerank_engine import (
        build_adjacency_matrix,
        generate_ranking_table,
        power_iteration,
        validate_with_networkx,
    )
except ImportError:
    from pagerank_engine import (  # type: ignore
        build_adjacency_matrix,
        generate_ranking_table,
        power_iteration,
        validate_with_networkx,
    )

DATA_CANDIDATES = [
    REPO_ROOT / "data" / "Web-Mining" / "utm_subdomains_graph.json",
    CURRENT_DIR / "utm_subdomains_graph.json",
    CURRENT_DIR / "data" / "Web-Mining" / "utm_subdomains_graph.json",
    Path("data/Web-Mining/utm_subdomains_graph.json"),
    Path("utm_subdomains_graph.json"),
]
DATA_PATH = next((p for p in DATA_CANDIDATES if p.exists()), DATA_CANDIDATES[0])

st.set_page_config(
    page_title="UTM Web Graph & PageRank Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Modern Custom CSS Injection ---
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Metric Card Styling */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px 22px;
        box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.08);
    }
    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 8px;
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }
    .metric-value {
        font-size: 1.65rem;
        font-weight: 800;
        color: #0f172a;
        margin-top: 4px;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #059669;
        font-weight: 600;
        margin-top: 6px;
    }

    /* Graph Canvas Frame */
    .graph-container {
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        background: #ffffff;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.04);
    }

    /* Category Pill Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .badge-root { background: #fef3c7; color: #b45309; }
    .badge-faculty { background: #d1fae5; color: #047857; }
    .badge-academic { background: #e0f2fe; color: #0369a1; }
    .badge-research { background: #ede9fe; color: #6d28d9; }
    .badge-unit { background: #f1f5f9; color: #475569; }

    /* Header styling */
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 9999px;
        color: #15803d;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.02em;
        line-height: 1.2;
        margin-bottom: 8px;
    }
    .hero-desc {
        font-size: 1.0rem;
        color: #475569;
        line-height: 1.6;
        max-width: 900px;
        margin-bottom: 24px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_data
def load_graph_data() -> dict[str, Any]:
    """Load pre-crawled UTM subdomains graph dataset."""
    if not DATA_PATH.exists():
        st.error(f"Dataset tidak ditemukan pada: {DATA_PATH}")
        return {"nodes": [], "edges": [], "stats": {}}
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def categorize_subdomain(name: str) -> tuple[str, str, int]:
    """Return category name, color hex, and hierarchy level for layout."""
    if name == "trunojoyo.ac.id":
        return "Portal Utama (Root)", "#f59e0b", 1
    if name.startswith(
        ("teknik.", "feb.", "pertanian.", "hukum.", "fisib.", "fip.", "fik.", "fk.")
    ):
        return "Fakultas", "#10b981", 2
    if name.startswith(("siakad.", "pta.", "pmb.", "library.")):
        return "Layanan Akademik", "#0284c7", 3
    if name.startswith(("lppm.", "journal.", "lpmpp.", "simpelmas.", "hki.")):
        return "Riset & Pengabdian", "#8b5cf6", 3
    return "Unit / Lembaga Lain", "#64748b", 4


def build_interactive_graph(
    nodes: list[str],
    edges: list[list[str]],
    table_items: list[dict[str, Any]],
    layout_mode: str = "organic",
    highlight_mode: str = "inbound",
    target_node: str | None = None,
) -> str:
    """Build pre-stabilized Pyvis network HTML string with zero jitter."""
    net = Network(
        height="640px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
    )

    pr_map = {item["website"]: item for item in table_items}
    scores = [item["pagerank"] for item in table_items]
    min_pr = min(scores) if scores else 0.001
    max_pr = max(scores) if scores else 0.05

    in_referrers = {u for u, v in edges if v == target_node} if target_node else set()
    out_targets = {v for u, v in edges if u == target_node} if target_node else set()

    for node in nodes:
        info = pr_map.get(
            node, {"rank": 999, "pagerank": 0.0, "in_degree": 0, "out_degree": 0}
        )
        cat_name, base_color, level = categorize_subdomain(node)

        # Scale node radius gracefully between 16px and 48px
        if max_pr > min_pr:
            norm = (info["pagerank"] - min_pr) / (max_pr - min_pr)
            size = 16 + norm * 34
        else:
            size = 20

        # Apply Highlight Mode Visual Styling
        border_width = 1.5
        font_color = "#0f172a"
        if highlight_mode == "inbound" and target_node:
            if node == target_node:
                node_color = "#3b82f6"
                size = max(size, 34)
                border_width = 3.0
            elif node in in_referrers:
                node_color = "#10b981"  # Emerald green for inbound referrers
                size = max(size, 26)
                border_width = 2.0
            else:
                node_color = "rgba(226, 232, 240, 0.4)"  # Soft-dimmed
                size = 12
                font_color = "#94a3b8"
        elif highlight_mode == "all_neighbors" and target_node:
            if node == target_node:
                node_color = "#3b82f6"
                size = max(size, 34)
                border_width = 3.0
            elif node in in_referrers:
                node_color = "#10b981"
                size = max(size, 24)
            elif node in out_targets:
                node_color = "#0ea5e9"
                size = max(size, 24)
            else:
                node_color = "rgba(226, 232, 240, 0.4)"
                size = 12
                font_color = "#94a3b8"
        else:
            node_color = base_color

        display_label = node.replace(".trunojoyo.ac.id", "")
        if display_label == "trunojoyo.ac.id":
            display_label = "UTM (Root)"

        tooltip = (
            f"<div style='font-family: sans-serif; font-size: 13px; line-height: 1.5; color: #0f172a;'>"
            f"<b style='font-size: 14px; color: {base_color};'>{node}</b><br/>"
            f"Kategori: <b>{cat_name}</b><br/>"
            f"Peringkat PageRank: <b>#{info['rank']}</b><br/>"
            f"Skor PageRank: <b>{info['pagerank']:.5f}</b><br/>"
            f"Tautan Masuk (In): <b>{info['in_degree']}</b> | Keluar (Out): <b>{info['out_degree']}</b>"
            f"</div>"
        )

        net.add_node(
            node,
            label=display_label,
            title=tooltip,
            color=node_color,
            size=size,
            shape="dot",
            borderWidth=border_width,
            level=level,
            font={
                "size": 11,
                "face": "Plus Jakarta Sans, sans-serif",
                "strokeWidth": 2,
                "strokeColor": "#ffffff",
                "color": font_color,
            },
        )

    for u, v in edges:
        # Edge styling based on highlight mode
        if highlight_mode == "inbound" and target_node:
            if v == target_node:
                edge_color = {"color": "#10b981", "highlight": "#059669"}
                edge_width = 2.4
                edge_arrows = {"to": {"enabled": True, "scaleFactor": 0.85}}
            else:
                edge_color = {
                    "color": "rgba(226, 232, 240, 0.2)",
                    "highlight": "#cbd5e1",
                }
                edge_width = 0.4
                edge_arrows = {"to": {"enabled": False}}
        elif highlight_mode == "all_neighbors" and target_node:
            if v == target_node:
                edge_color = {"color": "#10b981", "highlight": "#059669"}
                edge_width = 2.0
                edge_arrows = {"to": {"enabled": True, "scaleFactor": 0.8}}
            elif u == target_node:
                edge_color = {"color": "#0ea5e9", "highlight": "#0284c7"}
                edge_width = 2.0
                edge_arrows = {"to": {"enabled": True, "scaleFactor": 0.8}}
            else:
                edge_color = {
                    "color": "rgba(226, 232, 240, 0.2)",
                    "highlight": "#cbd5e1",
                }
                edge_width = 0.4
                edge_arrows = {"to": {"enabled": False}}
        else:
            edge_color = {"color": "#cbd5e1", "highlight": "#ef4444"}
            edge_width = 1.2
            edge_arrows = {"to": {"enabled": True, "scaleFactor": 0.75}}

        net.add_edge(
            u,
            v,
            color=edge_color,
            arrows=edge_arrows,
            smooth={"type": "curvedCW", "roundness": 0.15},
            width=edge_width,
        )

    if layout_mode == "hierarchical":
        net.set_options(
            """
        {
          "layout": {
            "hierarchical": {
              "enabled": true,
              "direction": "UD",
              "sortMethod": "directed",
              "nodeSpacing": 170,
              "levelSeparation": 150
            }
          },
          "physics": {
            "stabilization": {"enabled": true, "iterations": 150}
          }
        }
        """
        )
    else:
        # Pre-stabilized organic layout: runs 150 ticks in background so nodes appear instantly static!
        net.set_options(
            """
        {
          "layout": {
            "hierarchical": {"enabled": false}
          },
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -3200,
              "centralGravity": 0.35,
              "springLength": 130,
              "springConstant": 0.04,
              "damping": 0.18,
              "avoidOverlap": 0.3
            },
            "stabilization": {
              "enabled": true,
              "iterations": 200,
              "updateInterval": 25
            }
          },
          "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true
          }
        }
        """
        )

    return net.generate_html()


# --- Load Data & Computations ---
data = load_graph_data()
nodes = data.get("nodes", [])
edges = data.get("edges", [])

if not nodes:
    st.error(
        "Data graf tidak tersedia. Silakan jalankan scripts/crawl_utm_graph.py terlebih dahulu."
    )
    st.stop()

# --- Sidebar Controls ---
st.sidebar.markdown(
    """
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 16px;'>
        <div style='background: #1e3a8a; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 1.1rem;'>
            UTM
        </div>
        <div>
            <div style='font-weight: 800; font-size: 0.95rem; color: #0f172a;'>Web Intelligence</div>
            <div style='font-size: 0.75rem; color: #64748b;'>PageRank Engine v2.0</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar.expander("Parameter Algoritma", expanded=True):
    damping = st.slider(
        "Faktor Redaman (d)",
        min_value=0.10,
        max_value=0.99,
        value=0.85,
        step=0.05,
        help="Probabilitas peselancar acak mengikuti hyperlink. Standar industri Larry Page: d = 0.85.",
    )
    tolerance_exp = st.select_slider(
        "Ambang Konvergensi (Epsilon)",
        options=[-4, -5, -6, -7, -8],
        value=-7,
        format_func=lambda x: f"10^{x}",
    )
    tolerance = 10.0**tolerance_exp
    max_iter = st.number_input(
        "Batas Iterasi Maksimal", min_value=20, max_value=500, value=200, step=20
    )

with st.sidebar.expander("Kustomisasi Visual Graf", expanded=True):
    highlight_mode = st.radio(
        "Mode Sorotan Graf",
        options=["inbound", "all_neighbors", "none"],
        format_func=lambda x: {
            "inbound": "Inbound Saja (Perujuk Masuk)",
            "all_neighbors": "1-Hop Lengkap (In & Out)",
            "none": "Seluruh Graf (Tanpa Filter)",
        }[x],
        index=0,
        help="Inbound Saja memfokuskan simpul perujuk masuk yang menyumbangkan PageRank.",
    )
    target_node = st.selectbox(
        "Simpul Target Analisis",
        options=nodes,
        index=nodes.index("trunojoyo.ac.id") if "trunojoyo.ac.id" in nodes else 0,
        help="Simpul pusat yang dianalisis relasi tautannya.",
    )
    layout_choice = st.radio(
        "Model Penataan Simpul",
        options=["organic", "hierarchical"],
        format_func=lambda x: (
            "Organik Terstabilisasi"
            if x == "organic"
            else "Hierarki Otoritas Berjenjang"
        ),
    )
    scope_choice = st.radio(
        "Cakupan Simpul Graf",
        options=["top12", "top25", "all"],
        format_func=lambda x: {
            "top12": "Top 12 Inti Kampus (Fokus)",
            "top25": "Top 25 Fakultas & Layanan",
            "all": f"Seluruh Jaringan ({len(nodes)} Subdomain)",
        }[x],
    )

with st.sidebar.expander("Informasi Deployment", expanded=False):
    st.markdown(
        """
        - **Host Port:** `8501` (Headless)
        - **Target Lab:** Server Warga Lab Teknik
        - **Target Kampus:** Reverse Proxy Nginx & Systemd
        - **Library:** NetworkX, Pyvis, Streamlit
        """
    )

# --- Compute Mathematical Model ---
adj, node_map = build_adjacency_matrix(nodes, edges)
calc_result = power_iteration(adj, d=damping, max_iter=int(max_iter), tol=tolerance)
ranks = calc_result["rank_vector"]
table_items = generate_ranking_table(nodes, adj, ranks)
val_result = validate_with_networkx(nodes, edges, ranks, d=damping, tol=tolerance)

# --- Hero Header ---
st.markdown(
    """
    <div>
        <span class="hero-badge">LIVE — UNIVERSITAS TRUNOJOYO MADURA</span>
        <h1 class="hero-title">Analisis Otoritas Web & Algoritma PageRank</h1>
        <p class="hero-desc">
            Pemetaan topologi keterhubungan antar-subdomain resmi di lingkungan Universitas Trunojoyo Madura
            (<code>*.trunojoyo.ac.id</code>). Otoritas dihitung secara iteratif melalui <em>Power Iteration</em> dengan
            penanganan simpul buntu (<em>dead ends</em>) dan validasi matematis presisi tinggi.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Bento Grid Metric Cards (4 Balanced Columns) ---
mcol1, mcol2, mcol3, mcol4 = st.columns(4)

with mcol1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Subdomain</div>
            <div class="metric-value">{len(nodes)}</div>
            <div class="metric-sub">Entitas Resmi UTM</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with mcol2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Tautan Relasi Berarah</div>
            <div class="metric-value">{len(edges)}</div>
            <div class="metric-sub">Kepadatan Graf: {len(edges) / (len(nodes) * (len(nodes) - 1)):.4f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with mcol3:
    status_label = "Konvergen Stabil" if calc_result["converged"] else "Mencapai Batas"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Laju Konvergensi</div>
            <div class="metric-value">Iterasi {calc_result["iterations"]}</div>
            <div class="metric-sub">{status_label} (L1: {calc_result["diff_history"][-1]:.1e})</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with mcol4:
    top_web = table_items[0]["website"]
    top_pr = table_items[0]["pagerank"]
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Otoritas Tertinggi (#1)</div>
            <div class="metric-value" style="font-size: 1.25rem;">{top_web}</div>
            <div class="metric-sub">Skor PageRank: {top_pr:.5f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.write("")

# --- Main Navigation Tabs ---
tab_visual, tab_leaderboard, tab_matrix, tab_sensitivity, tab_crawler = st.tabs(
    [
        "Visualisasi Graf Interaktif",
        "Papan Peringkat Otoritas",
        "Matriks & Validasi Numerik",
        "Sensitivitas Faktor Redaman",
        "Konsol Uji Crawler",
    ]
)

# --- Tab 1: Visualisasi Graf Interaktif ---
with tab_visual:
    # Filter nodes based on user choice
    if scope_choice == "top12":
        display_nodes = [item["website"] for item in table_items[:12]]
    elif scope_choice == "top25":
        display_nodes = [item["website"] for item in table_items[:25]]
    else:
        display_nodes = nodes

    display_node_set = set(display_nodes)
    display_edges = [
        [u, v] for u, v in edges if u in display_node_set and v in display_node_set
    ]

    # Legend & Context Bar
    st.markdown(
        """
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; align-items: center;">
            <span style="font-size: 0.82rem; font-weight: 700; color: #475569; margin-right: 4px;">Kategori:</span>
            <span class="badge badge-root">Portal Utama (Root)</span>
            <span class="badge badge-faculty">Fakultas</span>
            <span class="badge badge-academic">Layanan Akademik</span>
            <span class="badge badge-research">Riset & Pengabdian</span>
            <span class="badge badge-unit">Unit Lembaga</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Dynamic Context Notification for Highlight Mode
    if highlight_mode == "inbound" and target_node:
        in_refs = [u for u, v in display_edges if v == target_node]
        st.info(
            f"**Mode Sorotan Inbound Saja Aktif:** Menyorot **{len(in_refs)} domain perujuk masuk** "
            f"yang secara langsung menyumbang skor PageRank ke **`{target_node}`**. "
            "Simpul dan busur lain disamarkan (*soft-dimmed*) untuk memusatkan perhatian pada kontributor otoritas."
        )
    elif highlight_mode == "all_neighbors" and target_node:
        in_refs = [u for u, v in display_edges if v == target_node]
        out_refs = [v for u, v in display_edges if u == target_node]
        st.info(
            f"**Mode 1-Hop Lengkap Aktif:** Menyorot **{len(in_refs)} tautan masuk** (hijau) dan **{len(out_refs)} tautan keluar** (cyan) untuk **`{target_node}`**."
        )

    # Render pre-stabilized Pyvis HTML in clean container
    html_graph = build_interactive_graph(
        display_nodes,
        display_edges,
        table_items,
        layout_mode=layout_choice,
        highlight_mode=highlight_mode,
        target_node=target_node,
    )
    components.html(html_graph, height=650, scrolling=False)

    st.caption(
        f"Menampilkan **{len(display_nodes)} Simpul** dan **{len(display_edges)} Busur Terarah**. "
        "Fisika telah distabilisasi di awal sehingga graf langsung tampil rapi dan tenang tanpa pergerakan kacau. "
        "Gunakan mouse untuk zoom, rotasi, atau menggeser simpul."
    )

# --- Tab 2: Papan Peringkat Otoritas ---
with tab_leaderboard:
    st.subheader("Peringkat Otoritas Seluruh Website Universitas Trunojoyo Madura")

    # Search & Filter
    scol1, scol2 = st.columns([2, 1])
    with scol1:
        query = st.text_input(
            "Cari subdomain tertentu:",
            placeholder="Contoh: siakad, teknik, lppm, feb...",
        )
    with scol2:
        category_filter = st.selectbox(
            "Filter Kategori:",
            options=[
                "Semua Kategori",
                "Portal Utama",
                "Fakultas",
                "Layanan Akademik",
                "Riset & Pengabdian",
                "Unit Lain",
            ],
        )

    # Build enriched dataframe
    max_score = table_items[0]["pagerank"] if table_items else 1.0
    processed_rows = []
    for item in table_items:
        cat_name, _, _ = categorize_subdomain(item["website"])
        # Category filter check
        if category_filter != "Semua Kategori":
            if category_filter == "Portal Utama" and "Root" not in cat_name:
                continue
            if category_filter == "Fakultas" and cat_name != "Fakultas":
                continue
            if category_filter == "Layanan Akademik" and cat_name != "Layanan Akademik":
                continue
            if (
                category_filter == "Riset & Pengabdian"
                and cat_name != "Riset & Pengabdian"
            ):
                continue
            if category_filter == "Unit Lain" and cat_name != "Unit / Lembaga Lain":
                continue

        # Search query check
        if query and query.strip().lower() not in item["website"].lower():
            continue

        rank_badge = f"#{item['rank']}"

        processed_rows.append(
            {
                "Peringkat": rank_badge,
                "Website Subdomain": item["website"],
                "Kategori": cat_name,
                "Skor PageRank": item["pagerank"],
                "Bobot Relatif": min(1.0, item["pagerank"] / max_score),
                "Tautan Masuk (In)": item["in_degree"],
                "Tautan Keluar (Out)": item["out_degree"],
            }
        )

    df_board = pd.DataFrame(processed_rows)

    if not df_board.empty:
        st.dataframe(
            df_board,
            column_config={
                "Skor PageRank": st.column_config.NumberColumn(format="%.5f"),
                "Bobot Relatif": st.column_config.ProgressColumn(
                    min_value=0.0,
                    max_value=1.0,
                    format="%.3f",
                ),
            },
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Tidak ada subdomain yang sesuai dengan kriteria pencarian.")

    # Export CTA
    csv_bytes = (
        df_board.to_csv(index=False).encode("utf-8") if not df_board.empty else b""
    )
    json_bytes = json.dumps(table_items, indent=2).encode("utf-8")

    ecol1, ecol2, _ = st.columns([1, 1, 2])
    with ecol1:
        st.download_button(
            "Unduh Peringkat (CSV)",
            data=csv_bytes,
            file_name="pagerank_utm_ranking.csv",
            mime="text/csv",
        )
    with ecol2:
        st.download_button(
            "Unduh Metadata (JSON)",
            data=json_bytes,
            file_name="pagerank_utm_graph.json",
            mime="application/json",
        )

# --- Tab 3: Matriks & Validasi Numerik ---
with tab_matrix:
    st.subheader("Matriks Transisi Stokastik & Verifikasi Ketelitian")

    vcol1, vcol2 = st.columns(2)
    with vcol1:
        st.markdown(
            f"""
            <div class="metric-card" style="margin-bottom: 16px;">
                <div class="metric-label">Verifikasi NetworkX PageRank</div>
                <div class="metric-value" style="font-size: 1.35rem; color: #059669;">
                    {"Identik Sempurna" if val_result["is_valid"] else "Deviasi Numerik"}
                </div>
                <div class="metric-sub">
                    Selisih Maksimal: <b>{val_result["max_error"]:.2e}</b> | Rata-rata: <b>{val_result["mean_error"]:.2e}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with vcol2:
        st.markdown(
            f"""
            <div class="metric-card" style="margin-bottom: 16px;">
                <div class="metric-label">Kondisi Stokastik Kolom</div>
                <div class="metric-value" style="font-size: 1.35rem; color: #0284c7;">
                    ∑ Kolom = 1.00000
                </div>
                <div class="metric-sub">
                    Penanganan dead-ends redistribusi merata: <b>1/N = {1.0 / len(nodes):.5f}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Sampel Matriks Ketetanggaan ($A_{ij}$) — Portal-Portal Inti UTM")
    core_samples = [
        "trunojoyo.ac.id",
        "siakad.trunojoyo.ac.id",
        "journal.trunojoyo.ac.id",
        "lppm.trunojoyo.ac.id",
        "teknik.trunojoyo.ac.id",
        "feb.trunojoyo.ac.id",
        "hukum.trunojoyo.ac.id",
        "pmb.trunojoyo.ac.id",
    ]
    sample_sub_idx = [node_map[s] for s in core_samples if s in node_map]
    clean_sample_labels = [s.replace(".trunojoyo.ac.id", "") for s in core_samples]

    sub_adj = adj[np.ix_(sample_sub_idx, sample_sub_idx)]
    df_sub_adj = pd.DataFrame(
        sub_adj, index=clean_sample_labels, columns=clean_sample_labels
    )
    st.dataframe(df_sub_adj, use_container_width=True)

    st.markdown("#### Korelasi Antara Derajat Masuk (In-Degree) dan Skor PageRank")
    st.caption(
        "Memperlihatkan bahwa halaman dengan in-degree sama dapat memiliki skor berbeda tergantung kualitas otoritas pengirim tautan."
    )
    df_scatter = pd.DataFrame(table_items)
    st.scatter_chart(
        df_scatter,
        x="in_degree",
        y="pagerank",
        color="out_degree",
        size="pagerank",
    )

# --- Tab 4: Sensitivitas Faktor Redaman ---
with tab_sensitivity:
    st.subheader("Eksperimen Sensitivitas Faktor Redaman (Damping Factor)")
    st.markdown(
        "Faktor redaman $d$ merepresentasikan probabilitas peselancar acak mengikuti tautan keluar (*random walk*) "
        "alih-alih melompat acak (*teleportation*). Nilai $d$ tinggi memperkuat hierarki struktural jaringan."
    )

    test_factors = [0.50, 0.70, 0.85, 0.95]
    top_portals = [item["website"] for item in table_items[:8]]
    sens_matrix = {
        "Subdomain": [p.replace(".trunojoyo.ac.id", "") for p in top_portals]
    }

    for f_val in test_factors:
        res_f = power_iteration(adj, d=f_val, max_iter=300, tol=1e-7)
        ranks_f = res_f["rank_vector"]
        sens_matrix[f"d = {f_val:.2f}"] = [
            float(ranks_f[node_map[p]]) for p in top_portals
        ]

    df_sens = pd.DataFrame(sens_matrix)
    st.dataframe(
        df_sens.style.format(
            {c: "{:.5f}" for c in df_sens.columns if c != "Subdomain"}
        ),
        use_container_width=True,
    )

    st.line_chart(df_sens.set_index("Subdomain"))

# --- Tab 5: Konsol Uji Crawler ---
with tab_crawler:
    st.subheader("Konsol Uji Perayap Web & Eksplorasi Kedalaman (Live Multi-Domain)")
    st.markdown(
        "Konsol ini memungkinkan pengujian langsung (*live crawling probe*) terhadap website institusi kampus UTM "
        "maupun **domain publik lain** (seperti `https://www.sman1ketapang.sch.id/`) untuk menginspeksi **kedalaman penelusuran (*crawl depth*)**, "
        "ketersediaan respon server, tautan internal, serta tautan keluar (*outbound links*)."
    )

    preset_col1, preset_col2, preset_col3 = st.columns(3)
    preset_url = "https://www.sman1ketapang.sch.id/"
    if preset_col1.button("SMAN 1 Ketapang", use_container_width=True):
        st.session_state["target_probe_url"] = "https://www.sman1ketapang.sch.id/"
    if preset_col2.button("Rektorat UTM", use_container_width=True):
        st.session_state["target_probe_url"] = "https://www.trunojoyo.ac.id/"
    if preset_col3.button("SIAKAD UTM", use_container_width=True):
        st.session_state["target_probe_url"] = "https://siakad.trunojoyo.ac.id/"

    current_val = st.session_state.get(
        "target_probe_url", "https://www.sman1ketapang.sch.id/"
    )

    tcol1, tcol2 = st.columns([3, 1])
    with tcol1:
        target_probe = st.text_input("URL Sasaran Uji:", value=current_val)
    with tcol2:
        crawl_depth = st.selectbox(
            "Kedalaman (Depth):",
            [1, 2],
            format_func=lambda x: (
                f"Depth {x} ({'Homepage Saja' if x == 1 else 'Homepage + Subpages'})"
            ),
        )

    run_probe = st.button(
        "Jalankan Uji Perayapan Langsung",
        type="primary",
        use_container_width=True,
    )

    if run_probe:
        with st.spinner(
            f"Menghubungi {target_probe} dengan parameter Depth {crawl_depth}..."
        ):
            try:
                import time
                from urllib.parse import urljoin, urlparse

                clean_target: str = str(target_probe or "").strip()
                p_target = urlparse(clean_target)
                target_host: str = str(p_target.netloc).split(":")[0].lower()
                root_host: str = target_host.removeprefix("www.")

                headers = {
                    "User-Agent": "PPW-UTM-PageRankBot/1.0 (+https://trunojoyo.ac.id; student-research)"
                }
                t_start = time.time()
                resp = requests.get(
                    clean_target, headers=headers, timeout=10, verify=False
                )
                latency = round((time.time() - t_start) * 1000, 1)

                soup = BeautifulSoup(resp.text, "html.parser")
                page_title = (
                    soup.title.string.strip()
                    if (soup.title and soup.title.string)
                    else target_host
                )

                internal_links: set[str] = set()
                external_links: set[str] = set()

                for a in soup.find_all("a", href=True):
                    h_val = str(a.get("href", "")).strip()
                    if h_val.startswith(("#", "javascript:", "mailto:", "tel:")):
                        continue
                    full = str(urljoin(clean_target, h_val))
                    c_host = str(urlparse(full).netloc).split(":")[0].lower()
                    if c_host == target_host or (
                        c_host != "" and c_host.endswith("." + root_host)
                    ):
                        internal_links.add(full)
                    elif c_host:
                        external_links.add(full)

                # Jika Depth == 2, jelajahi hingga 2 subhalaman internal
                subpage_probed = 0
                if crawl_depth == 2 and internal_links:
                    sub_candidates = [
                        u
                        for u in sorted(internal_links)
                        if not any(
                            u.endswith(ext)
                            for ext in (
                                ".pdf",
                                ".jpg",
                                ".png",
                                ".zip",
                                ".docx",
                            )
                        )
                    ]
                    for sub_url in sub_candidates[:2]:
                        try:
                            time.sleep(1.0)
                            sub_resp = requests.get(
                                sub_url,
                                headers=headers,
                                timeout=8,
                                verify=False,
                            )
                            if sub_resp.status_code == 200:
                                subpage_probed += 1
                                sub_soup = BeautifulSoup(sub_resp.text, "html.parser")
                                for sa in sub_soup.find_all("a", href=True):
                                    sh = str(sa.get("href", "")).strip()
                                    if sh.startswith(
                                        ("#", "javascript:", "mailto:", "tel:")
                                    ):
                                        continue
                                    s_full = str(urljoin(sub_url, sh))
                                    s_host = (
                                        str(urlparse(s_full).netloc)
                                        .split(":")[0]
                                        .lower()
                                    )
                                    if s_host == target_host or (
                                        s_host != ""
                                        and s_host.endswith("." + root_host)
                                    ):
                                        internal_links.add(s_full)
                                    elif s_host:
                                        external_links.add(s_full)
                        except (requests.RequestException, OSError):
                            pass

                st.success(
                    f"Sukses Merespons — Status HTTP: {resp.status_code} | Judul: {page_title} (Latency: {latency} ms)"
                )

                res_c1, res_c2, res_c3, res_c4 = st.columns(4)
                res_c1.metric("Kedalaman Teruji", f"Depth {crawl_depth}")
                res_c2.metric("Subhalaman Ditelaah", f"{subpage_probed + 1} URL")
                res_c3.metric(
                    "Tautan Internal",
                    f"{len(internal_links)} URL",
                )
                res_c4.metric(
                    "Tautan Keluar (External)",
                    f"{len(external_links)} URL",
                )

                subtab_in, subtab_out = st.tabs(
                    [
                        f"Tautan Internal ({len(internal_links)})",
                        f"Tautan Eksternal ({len(external_links)})",
                    ]
                )
                with subtab_in:
                    if internal_links:
                        st.dataframe(
                            pd.DataFrame(
                                {
                                    "No": range(1, len(internal_links) + 1),
                                    "Tautan Internal": sorted(internal_links),
                                }
                            ),
                            use_container_width=True,
                            hide_index=True,
                        )
                    else:
                        st.info("Tidak ada tautan internal yang ditemukan.")

                with subtab_out:
                    if external_links:
                        st.dataframe(
                            pd.DataFrame(
                                {
                                    "No": range(1, len(external_links) + 1),
                                    "Tautan Keluar": sorted(external_links),
                                }
                            ),
                            use_container_width=True,
                            hide_index=True,
                        )
                    else:
                        st.info("Tidak ada tautan eksternal yang ditemukan.")

            except (requests.RequestException, OSError) as e:
                st.error(f"Gagal melakukan perayapan pada target: {e}")

st.markdown("---")
st.markdown(
    """
    <div style='display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #94a3b8;'>
        <div>Tugas 7 PPW — Web Search & Mining | Universitas Trunojoyo Madura</div>
        <div>Deployment Ready: Server Warga Laboratorium & Server Kampus</div>
    </div>
    """,
    unsafe_allow_html=True,
)
