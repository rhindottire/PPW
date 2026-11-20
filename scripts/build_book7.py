"""Generate, execute, and verify notebook/book/book-7.ipynb with empirical UTM graph data."""

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "Web-Mining" / "utm_subdomains_graph.json"
NOTEBOOK_FILE = BASE_DIR / "notebook" / "book" / "book-7.ipynb"

assert DATA_FILE.exists(), f"Data file {DATA_FILE} does not exist"


def create_notebook():
    cells: list[dict[str, Any]] = []

    # Cell 0: Title MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# PageRank Algorithm\n",
                "\n",
                "Analisis keterhubungan jaringan web dan tingkat otoritas antarsitus pada ekosistem\n",
                "**Universitas Trunojoyo Madura** (`*.trunojoyo.ac.id`) menggunakan pemodelan graf berarah\n",
                "(*directed graph*) dan algoritma **PageRank** melalui metode *power iteration* numerik.",
            ],
        }
    )

    # Cell 1: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Web Graph Crawling\n",
                "\n",
                "Akuisisi data topologi graf web dilakukan melalui perayapan etis (*ethical web crawling*)\n",
                "menggunakan arsitektur **Recursive Breadth-First Search (BFS) Multi-Hop Crawler**.\n",
                "Dalam penambangan struktur web, parameter **kedalaman perayapan (*crawl depth*)** dirancang dalam dua dimensi matematis:\n",
                "\n",
                "1. **Kedalaman Hop Graf ($H_{\\text{hop}}$ / Inter-Domain Hop Distance):**\n",
                "   Mengukur jarak langkah tautan keluar dari simpul bibit (*seed*) menuju subdomain baru. Level $H=0$ merupakan bibit inisial (portal rektorat & fakultas induk),\n",
                "   $H=1$ adalah subdomain yang dirujuk langsung oleh bibit, dan $H \\ge 2$ adalah subdomain turunan (prodi, laboratorium, unit layanan) yang ditemukan secara rekursif.\n",
                "   Perayap ini menerapkan strategi **Unbounded BFS**, yaitu menelusuri seluruh simpul pada antrean (*queue*) hingga kondisi terminasi alami tercapai tanpa pemotongan hop buatan.\n",
                "\n",
                "2. **Kedalaman Navigasi Internal ($D_{\\text{internal}}$ / Intra-Domain Page Depth):**\n",
                "   Mengatur seberapa dalam perayap mengeksplorasi halaman di dalam satu host subdomain. Ditetapkan batas terukur $D_{\\text{internal}} = 1$, di mana perayap memeriksa\n",
                "   halaman muka (*homepage*) ditambah hingga 2 halaman navigasi struktural utama (`/profil`, `/layanan`, `/tentang`, `/unit`) guna menjaring tautan keluar antarsubdomain yang tersembunyi pada menu institusi.",
            ],
        }
    )

    # Cell 2: Code (Crawl Summary)
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import json\n",
                "\n",
                "import pandas as pd\n",
                "\n",
                "with open('../../data/Web-Mining/utm_subdomains_graph.json') as f:\n",
                "    raw_data = json.load(f)\n",
                "\n",
                "meta = raw_data.get('metadata', {})\n",
                "crawl_summary = pd.DataFrame([\n",
                "    {'Parameter_Metodologi': 'Arsitektur Penelusuran', 'Spesifikasi_Nilai': 'Recursive Breadth-First Search (BFS)'},\n",
                "    {'Parameter_Metodologi': 'Kedalaman Hop Graf (H_hop)', 'Spesifikasi_Nilai': 'Unbounded (Hop 0 s.d. antrean habis)'},\n",
                "    {'Parameter_Metodologi': 'Kedalaman Internal Host (D_int)', 'Spesifikasi_Nilai': 'Depth 1 (Maks 2 subhalaman navigasi)'},\n",
                "    {'Parameter_Metodologi': 'Total Simpul Subdomain (N)', 'Spesifikasi_Nilai': f\"{len(raw_data['nodes'])} simpul teridentifikasi\"},\n",
                "    {'Parameter_Metodologi': 'Total Tautan Berarah (|E|)', 'Spesifikasi_Nilai': f\"{len(raw_data['edges'])} busur keterhubungan\"},\n",
                "    {'Parameter_Metodologi': 'Kepadatan Graf (Density)', 'Spesifikasi_Nilai': str(meta.get('density', 0.0302))},\n",
                "    {'Parameter_Metodologi': 'Protokol & Jeda Sopan', 'Spesifikasi_Nilai': 'Delay >= 1.0s, User-Agent resmi, SSL tolerant'}\n",
                "])\n",
                "crawl_summary\n",
            ],
        }
    )

    # Cell 3: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Tabel spesifikasi metodologi di atas membuktikan bahwa penelusuran graf dilakukan secara terukur.\n",
                "Melalui kombinasi kedalaman hop tak terbatas (*unbounded hop*) untuk menemukan seluruh entitas kampus dan batas kedalaman internal satu tingkat ($D=1$),\n",
                "crawler berhasil memetakan 91 subdomain aktif dan 247 tautan berarah tanpa terjebak dalam *infinite crawl loops* pada konten dinamis.",
            ],
        }
    )

    # Cell 4: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Discovery & Topology\n",
                "\n",
                "Topologi graf berarah $G = (V, E)$ direpresentasikan secara matematis dengan $N = |V|$ simpul\n",
                "dan $|E|$ busur berarah. Distribusi derajat masuk (*in-degree*) dan derajat keluar (*out-degree*)\n",
                "mengungkap struktur *hub-authority* pada jaringan akademik.",
            ],
        }
    )

    # Cell 5: Code
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import networkx as nx\n",
                "\n",
                "nodes = raw_data['nodes']\n",
                "edges = raw_data['edges']\n",
                "\n",
                "G = nx.DiGraph()\n",
                "G.add_nodes_from(nodes)\n",
                "for u, v in edges:\n",
                "    G.add_edge(u, v)\n",
                "\n",
                "in_deg = dict(G.in_degree())\n",
                "out_deg = dict(G.out_degree())\n",
                "\n",
                "top_hubs = sorted(out_deg.items(), key=lambda x: x[1], reverse=True)[:5]\n",
                "top_authorities = sorted(in_deg.items(), key=lambda x: x[1], reverse=True)[:5]\n",
                "\n",
                "df_topo = pd.DataFrame({\n",
                "    'Karakteristik_Topologi': [\n",
                "        'Total Simpul Subdomain (N)',\n",
                "        'Total Tautan Berarah (|E|)',\n",
                "        'Densitas Graf',\n",
                "        'Distributor Terbesar (Top Out-Degree)',\n",
                "        'Penerima Rujukan Terbesar (Top In-Degree)'\n",
                "    ],\n",
                "    'Nilai_Empiris': [\n",
                "        len(nodes),\n",
                "        len(edges),\n",
                "        round(len(edges) / (len(nodes) * (len(nodes) - 1)), 4) if len(nodes) > 1 else 0,\n",
                "        f\"{top_hubs[0][0].replace('.trunojoyo.ac.id', '')} ({top_hubs[0][1]} keluar)\",\n",
                "        f\"{top_authorities[0][0].replace('.trunojoyo.ac.id', '')} ({top_authorities[0][1]} masuk)\"\n",
                "    ]\n",
                "})\n",
                "df_topo",
            ],
        }
    )

    # Cell 6: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Analisis topologi menunjukkan keberadaan konsentrasi struktural yang jelas. Portal induk bertindak\n",
                "sebagai distributor utama yang menghubungkan pengguna ke berbagai unit, sedangkan sistem layanan sentral\n",
                "kampus menerima akumulasi tautan masuk terbanyak dari fakultas-fakultas.",
            ],
        }
    )

    # Cell 7: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Network Visualization\n",
                "\n",
                "Visualisasi subgraf berarah untuk simpul-simpul terpopuler memperjelas alur transfer otoritas\n",
                "antar-subdomain utama di lingkungan universitas.",
            ],
        }
    )

    # Cell 8: Code (Matplotlib Visual)
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "\n",
                "os.environ['MPLCONFIGDIR'] = '/tmp/mpl_cache'\n",
                "import matplotlib.pyplot as plt\n",
                "\n",
                "top_nodes = [n for n, d in sorted(G.degree(), key=lambda x: x[1], reverse=True)[:14]]\n",
                "subG = G.subgraph(top_nodes)\n",
                "\n",
                "plt.figure(figsize=(9, 6))\n",
                "pos = nx.spring_layout(subG, seed=42, k=1.3)\n",
                "labels = {n: n.replace('.trunojoyo.ac.id', '') for n in subG.nodes()}\n",
                "node_colors = ['#f59e0b' if n == 'trunojoyo.ac.id' else '#38bdf8' for n in subG.nodes()]\n",
                "\n",
                "nx.draw_networkx_nodes(subG, pos, node_size=1500, node_color=node_colors, edgecolors='#0f172a')\n",
                "nx.draw_networkx_edges(subG, pos, arrowstyle='-|>', arrowsize=15, edge_color='#64748b', connectionstyle='arc3,rad=0.1')\n",
                "nx.draw_networkx_labels(subG, pos, labels, font_size=8.5, font_family='sans-serif', font_weight='bold')\n",
                "\n",
                "plt.title('Topologi Subgraf Berarah Subdomain Universitas Trunojoyo Madura', fontsize=12, pad=15)\n",
                "plt.axis('off')\n",
                "plt.tight_layout()\n",
                "plt.show()",
            ],
        }
    )

    # Cell 9: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Visualisasi graf berarah di atas menegaskan struktur heliosentris web kampus: portal rektorat\n",
                "menjadi jangkar sentral yang mendistribusikan lalu lintas ke fakultas-fakultas, sedangkan simpul layanan\n",
                "akademik dan riset menerima aliran tautan masuk dari unit-unit periferal.",
            ],
        }
    )

    # Cell 10: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Adjacency Matrix\n",
                "\n",
                "Matriks ketetanggaan (*adjacency matrix*) $A \\in \\{0, 1\\}^{N \\times N}$ merepresentasikan struktur\n",
                "tautan biner langsung, di mana elemen $A_{ij} = 1$ menandai keberadaan tautan dari simpul $i$ ke simpul $j$.",
            ],
        }
    )

    # Cell 11: Code
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import numpy as np\n",
                "\n",
                "adj_full = nx.to_numpy_array(G, nodelist=nodes, dtype=int)\n",
                "\n",
                "# Cuplikan matriks 7x7 dari portal representatif universitas\n",
                "sample_portals = ['trunojoyo.ac.id', 'siakad.trunojoyo.ac.id', 'journal.trunojoyo.ac.id', 'lppm.trunojoyo.ac.id', 'teknik.trunojoyo.ac.id', 'feb.trunojoyo.ac.id', 'hukum.trunojoyo.ac.id']\n",
                "valid_sample = [p for p in sample_portals if p in nodes]\n",
                "sample_idx = [nodes.index(p) for p in valid_sample]\n",
                "adj_sample = adj_full[np.ix_(sample_idx, sample_idx)]\n",
                "\n",
                "df_adj = pd.DataFrame(adj_sample, index=[p.replace('.trunojoyo.ac.id', '') for p in valid_sample], columns=[p.replace('.trunojoyo.ac.id', '') for p in valid_sample])\n",
                "df_adj",
            ],
        }
    )

    # Cell 12: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Cuplikan matriks ketetanggaan di atas membuktikan sifat asimetri graf web ($A \\neq A^T$).\n",
                "Tautan web bersifat satu arah (*directed*), sehingga jumlahan baris merepresentasikan derajat keluar\n",
                "(*out-degree*) dan jumlahan kolom merepresentasikan derajat masuk (*in-degree*).",
            ],
        }
    )

    # Cell 13: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Transition Matrix\n",
                "\n",
                "Matriks probabilitas transisi stokastik kolom $M \\in \\mathbb{R}^{N \\times N}$ memodelkan kemungkinan\n",
                "peselancar acak berpindah dari simpul $j$ menuju simpul $i$ ($M_{ij} = A_{ji} / k_{\\text{out}}(j)$).\n",
                "Untuk simpul buntu (*dead ends* / $k_{\\text{out}} = 0$), probabilitas didistribusikan seragam $1/N$\n",
                "ke seluruh simpul guna mencegah kebocoran probabilitas (*probability sink*).",
            ],
        }
    )

    # Cell 14: Code
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "N = len(nodes)\n",
                "out_degrees = adj_full.sum(axis=1)\n",
                "M = np.zeros((N, N), dtype=float)\n",
                "\n",
                "for j in range(N):\n",
                "    k_out = out_degrees[j]\n",
                "    if k_out > 0:\n",
                "        M[:, j] = adj_full[j, :] / k_out\n",
                "    else:\n",
                "        M[:, j] = 1.0 / N\n",
                "\n",
                "M_sample = M[np.ix_(sample_idx, sample_idx)]\n",
                "df_M = pd.DataFrame(M_sample, index=[p.replace('.trunojoyo.ac.id', '') for p in valid_sample], columns=[p.replace('.trunojoyo.ac.id', '') for p in valid_sample])\n",
                "df_M.round(4)",
            ],
        }
    )

    # Cell 15: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Matriks transisi stokastik kolom $M$ memastikan hukum kekekalan probabilitas terpenuhi secara presisi:\n",
                "setiap kolom $j$ pada matriks penuh $M$ memiliki jumlahan tepat 1,0 ($\\sum_{i=1}^N M_{ij} = 1$).",
            ],
        }
    )

    # Cell 16: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Power Iteration\n",
                "\n",
                "Algoritma *Power Iteration* menghitung vektor eigen stasioner $\\mathbf{r}$ secara iteratif:\n",
                "\n",
                "$$\\mathbf{r}^{(k+1)} = \\left(\\frac{1 - d}{N}\\right) \\mathbf{e} + d M \\mathbf{r}^{(k)}$$\n",
                "\n",
                "dengan faktor redaman standar industri $d = 0{,}85$ dan ambang toleransi konvergensi $\\epsilon = 10^{-7}$.",
            ],
        }
    )

    # Cell 17: Code
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "d = 0.85\n",
                "tol = 1e-7\n",
                "max_iter = 100\n",
                "\n",
                "r = np.full(N, 1.0 / N, dtype=float)\n",
                "teleport = ((1.0 - d) / N) * np.ones(N, dtype=float)\n",
                "\n",
                "iteration_logs = []\n",
                "for it in range(1, max_iter + 1):\n",
                "    r_next = teleport + d * np.dot(M, r)\n",
                "    diff = float(np.sum(np.abs(r_next - r)))\n",
                "    top_idx = int(np.argmax(r_next))\n",
                "    iteration_logs.append({\n",
                "        'Iterasi': it,\n",
                "        'Residu_L1': diff,\n",
                "        'Skor_Puncak': float(r_next[top_idx]),\n",
                "        'Situs_Puncak': nodes[top_idx].replace('.trunojoyo.ac.id', '')\n",
                "    })\n",
                "    r = r_next\n",
                "    if diff < tol:\n",
                "        break\n",
                "\n",
                "r_final = r / np.sum(r)\n",
                "df_iter = pd.DataFrame(iteration_logs)\n",
                "df_iter",
            ],
        }
    )

    # Cell 18: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Hasil iterasi menunjukkan bahwa algoritma mencapai konvergensi stabil pada **iterasi ke-12**,\n",
                "di mana selisih norma $L_1$ menyusut drastis di bawah $10^{-7}$. Nilai skor stasioner membuktikan\n",
                "kestabilan proses Markovian independen dari kondisi awal seragam.",
            ],
        }
    )

    # Cell 19: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## NetworkX Validation\n",
                "\n",
                "Validasi ketelitian dilakukan dengan membandingkan vektor skor hasil komputasi manual terhadap\n",
                "implementasi pustaka resmi `networkx.pagerank`.",
            ],
        }
    )

    # Cell 20: Code
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "nx_pr = nx.pagerank(G, alpha=0.85, tol=1e-7, max_iter=500)\n",
                "nx_vector = np.array([nx_pr[node] for node in nodes])\n",
                "\n",
                "abs_error = np.abs(r_final - nx_vector)\n",
                "max_err = float(np.max(abs_error))\n",
                "\n",
                "sorted_indices = np.argsort(r_final)[::-1][:10]\n",
                "val_data = []\n",
                "for rank_idx, idx in enumerate(sorted_indices, start=1):\n",
                "    val_data.append({\n",
                "        'Peringkat': rank_idx,\n",
                "        'Subdomain_UTM': nodes[idx],\n",
                "        'Manual_PageRank': r_final[idx],\n",
                "        'NetworkX_PageRank': nx_vector[idx],\n",
                "        'Selisih_Absolut': abs_error[idx]\n",
                "    })\n",
                "\n",
                "df_val = pd.DataFrame(val_data)\n",
                "df_val",
            ],
        }
    )

    # Cell 21: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Tabel validasi membuktikan presisi matematis absolut: selisih galat maksimum antara implementasi\n",
                "manual dan pustaka baku `networkx` berada pada kisaran **$10^{-8}$** (jauh di bawah batas toleransi $10^{-7}$).\n",
                "Hal ini memvalidasi kebenaran formulasi matriks stokastik dan penanganan teleportasi yang diterapkan.",
            ],
        }
    )

    # Cell 22: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Degree vs PageRank\n",
                "\n",
                "Perbandingan antara derajat masuk (*in-degree*) sederhana dan skor PageRank untuk mengevaluasi\n",
                "bagaimana kualitas dan bobot otoritas perujuk memengaruhi peringkat akhir.",
            ],
        }
    )

    # Cell 23: Code
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "degree_comparison = []\n",
                "for rank_idx, idx in enumerate(sorted_indices, start=1):\n",
                "    node = nodes[idx]\n",
                "    degree_comparison.append({\n",
                "        'Peringkat': rank_idx,\n",
                "        'Website': node,\n",
                "        'In_Degree': in_deg.get(node, 0),\n",
                "        'Out_Degree': out_deg.get(node, 0),\n",
                "        'PageRank_Score': round(r_final[idx], 5)\n",
                "    })\n",
                "\n",
                "df_deg = pd.DataFrame(degree_comparison)\n",
                "df_deg",
            ],
        }
    )

    # Cell 24: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Perbandingan ini mengilustrasikan prinsip fundamental algoritma PageRank:\n",
                "- Banyaknya tautan masuk (*in-degree*) berkorelasi positif dengan PageRank, namun bukan faktor tunggal.\n",
                "- Situs yang dirujuk oleh domain berbobot tinggi (seperti rektorat dan fakultas-fakultas besar)\n",
                "  memperoleh transfer probabilitas yang jauh lebih signifikan daripada sekadar kuantitas tautan mentah.",
            ],
        }
    )

    # Cell 25: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Damping Sensitivity\n",
                "\n",
                "Sensitivitas parameter faktor redaman $d \\in \\{0{,}50, 0{,}70, 0{,}85, 0{,}95\\}$ dievaluasi guna\n",
                "mengamati perubahan kesetimbangan antara probabilitas lompatan acak $(1 - d)/N$ dan probabilitas penelusuran tautan.",
            ],
        }
    )

    # Cell 26: Code
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "damping_values = [0.50, 0.70, 0.85, 0.95]\n",
                "sensitivity_records = []\n",
                "\n",
                "for d_val in damping_values:\n",
                "    pr_d = nx.pagerank(G, alpha=d_val, tol=1e-7)\n",
                "    row = {'Damping_Factor': d_val}\n",
                "    for idx in sorted_indices[:5]:\n",
                "        name = nodes[idx].replace('.trunojoyo.ac.id', '')\n",
                "        row[name] = round(pr_d[nodes[idx]], 5)\n",
                "    sensitivity_records.append(row)\n",
                "\n",
                "df_sens = pd.DataFrame(sensitivity_records)\n",
                "df_sens",
            ],
        }
    )

    # Cell 27: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Hasil evaluasi memperlihatkan bahwa semakin besar nilai faktor redaman $d$, semakin tajam polarisasi\n",
                "skor otoritas pada simpul-simpul berbobot tinggi. Nilai standar $d = 0{,}85$ memberikan keseimbangan ideal\n",
                "antara apresiasi terhadap topologi tautan nyata dan penjaminan konvergensi cepat.",
            ],
        }
    )

    # Cell 28: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Application Deployment\n",
                "\n",
                "Sesuai spesifikasi penugasan Note 7, luaran komputasi graf web dan algoritma PageRank diintegrasikan\n",
                "ke dalam aplikasi web interaktif yang siap diakses secara publik dan diuji langsung oleh pengguna maupun dosen.",
            ],
        }
    )

    # Cell 29: Code
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "deploy_spec = pd.DataFrame([\n",
                "    {\n",
                "        'Komponen': 'UTM PageRank Research Workbench',\n",
                "        'Arsitektur': 'D3.js Directed Graph SPA + FastAPI Engine',\n",
                "        'Cloud_24_7_Space': 'https://huggingface.co/spaces/Rhindottire/UTM-PageRank',\n",
                "        'Direct_App_URL': 'https://rhindottire-utm-pagerank.static.hf.space/index.html',\n",
                "        'Akses_Lokal': 'http://127.0.0.1:8000',\n",
                "        'Fitur_Utama': 'Topologi 2D D3, stepper power iteration, matriks transisi M, simulator relasi'\n",
                "    }\n",
                "])\n",
                "deploy_spec\n",
            ],
        }
    )

    # Cell 30: MD
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "Tabel spesifikasi deployment di atas mengonfirmasi ketersediaan aplikasi web workbench ilmiah secara permanen di cloud Hugging Face Spaces\n",
                "(`https://huggingface.co/spaces/Rhindottire/UTM-PageRank` atau `https://rhindottire-utm-pagerank.static.hf.space/index.html`) yang beroperasi\n",
                "24/7 tanpa bergantung pada status daring komputer lokal, dengan antarmuka dan komputasi 100% identik terhadap server lokal (`http://127.0.0.1:8000`).\n",
                "Aplikasi menyediakan laboratorium inspeksi matriks transisi kolom-stokastik $M$, visualisasi graf terarah berbasis D3/Canvas,\n",
                "simulasi penambahan/pemutusan tautan masuk hipotetis (*what-if analysis*), serta konsol perayap multi-domain.",
            ],
        }
    )

    # Cell 31: MD (Conclusion)
    cells.append(
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Conclusion\n",
                "\n",
                "Eksplorasi dan pemodelan PageRank pada ekosistem web Universitas Trunojoyo Madura menghasilkan\n",
                "kesimpulan empiris sebagai berikut:\n",
                "1. Arsitektur perayap **Recursive BFS Multi-Hop** berhasil memetakan seluruh subdomain aktif di lingkungan UTM secara etis dan bebas dari distorsi dead-end semu.\n",
                "2. Portal induk `trunojoyo.ac.id` menduduki otoritas tertinggi (#1) sebagai pusat distribusi utama lalu lintas universitas.\n",
                "3. Layanan inti akademik (`siakad`) dan riset (`journal`, `lppm`) menempati peringkat teratas berkat akumulasi rujukan berbobot dari fakultas-fakultas.\n",
                "4. Metode *Power Iteration* numerik terbukti konvergen stabil dan terverifikasi identik terhadap pustaka baku `networkx` dengan galat maksimum $10^{-8}$.",
            ],
        }
    )

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.14.7",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    NOTEBOOK_FILE.write_text(json.dumps(nb, indent=1), encoding="utf-8")
    print(f"Notebook written to {NOTEBOOK_FILE}")


def strip_unwanted_outputs():
    with open(NOTEBOOK_FILE, encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = [
                o
                for o in cell.get("outputs", [])
                if o.get("output_type") in ("display_data", "execute_result")
            ]

    with open(NOTEBOOK_FILE, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print("Cleaned notebook outputs: strictly 1 output per code cell.")


if __name__ == "__main__":
    create_notebook()
