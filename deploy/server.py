"""FastAPI server for UTM Web Graph and PageRank Intelligence Application.

Provides RESTful API endpoints and serves the modern executive-grade SPA frontend.
Deployable on laboratory and campus servers via Uvicorn.
"""

import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import numpy as np

# Ensure repo root is in sys.path regardless of execution working directory
BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import requests
import uvicorn
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

try:
    from deploy.pagerank_engine import (
        build_adjacency_matrix,
        compute_score_breakdown,
        generate_ranking_table,
        power_iteration,
        simulate_link_modification,
        validate_with_networkx,
    )
except ImportError:
    from pagerank_engine import (  # type: ignore
        build_adjacency_matrix,
        compute_score_breakdown,
        generate_ranking_table,
        power_iteration,
        simulate_link_modification,
        validate_with_networkx,
    )

STATIC_CANDIDATES = [
    BASE_DIR / "static",
    Path("static"),
    Path("deploy/static"),
]
STATIC_DIR = next((p for p in STATIC_CANDIDATES if p.exists()), STATIC_CANDIDATES[0])

DATA_CANDIDATES = [
    REPO_ROOT / "data" / "Web-Mining" / "utm_subdomains_graph.json",
    BASE_DIR / "utm_subdomains_graph.json",
    Path("utm_subdomains_graph.json"),
    Path("data/Web-Mining/utm_subdomains_graph.json"),
]
DATA_FILE = next((p for p in DATA_CANDIDATES if p.exists()), DATA_CANDIDATES[0])

app = FastAPI(
    title="UTM Web Graph & PageRank Intelligence API",
    description="Backend API for UTM Web Crawling, Graph Topology, and PageRank Analysis",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_cached_graph() -> dict[str, Any]:
    """Load pre-crawled UTM subdomains graph dataset."""
    if not DATA_FILE.exists():
        raise HTTPException(
            status_code=500, detail="Dataset utm_subdomains_graph.json not found."
        )
    with open(DATA_FILE, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
        return data


class CalculateRequest(BaseModel):
    damping: float = Field(0.85, ge=0.01, le=0.99, description="Damping factor d")
    tolerance: float = Field(1e-7, ge=1e-10, le=1e-2, description="Convergence epsilon")
    max_iter: int = Field(200, ge=10, le=1000, description="Maximum iterations")


class SimulateRequest(BaseModel):
    target_node: str = Field(..., description="Target node to simulate")
    added_in_links: list[str] = Field(
        default_factory=list, description="Source nodes to add as incoming links"
    )
    removed_in_links: list[str] = Field(
        default_factory=list, description="Source nodes to remove"
    )
    damping: float = Field(0.85, ge=0.01, le=0.99, description="Damping factor d")


class ProbeRequest(BaseModel):
    url: str = Field(..., description="Target URL in UTM ecosystem to crawl")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Service health check endpoint."""
    return {
        "status": "healthy",
        "service": "utm-pagerank-intelligence",
        "version": "2.0.0",
    }


@app.get("/")
def serve_index() -> FileResponse:
    """Serve the modern SPA frontend."""
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend index.html not found.")
    return FileResponse(index_file)


@app.get("/api/graph")
def get_graph() -> JSONResponse:
    """Return nodes, edges, initial stats, and default PageRank leaderboard."""
    data = load_cached_graph()
    nodes: list[str] = data["nodes"]
    edges: list[list[str]] = data["edges"]

    adj, _ = build_adjacency_matrix(nodes, edges)
    res = power_iteration(adj, d=0.85, max_iter=200, tol=1e-7)
    ranks = res["rank_vector"]
    table = generate_ranking_table(nodes, adj, ranks)
    val = validate_with_networkx(nodes, edges, ranks, d=0.85, tol=1e-7)

    # Attach neighbor mapping for instant node inspection in frontend
    in_neighbors: dict[str, list[str]] = {node: [] for node in nodes}
    out_neighbors: dict[str, list[str]] = {node: [] for node in nodes}
    for u, v in edges:
        if u in out_neighbors:
            out_neighbors[u].append(v)
        if v in in_neighbors:
            in_neighbors[v].append(u)

    density = len(edges) / (len(nodes) * (len(nodes) - 1)) if len(nodes) > 1 else 0.0

    rank_map = {item["website"]: item["rank"] for item in table}
    pr_map = {item["website"]: item["pagerank"] for item in table}

    # Clean topological node objects for 2D scientific network visualization
    node_objects = [
        {
            "id": node,
            "name": node,
            "rank": rank_map.get(node, 999),
            "pagerank": round(pr_map.get(node, 0.0), 6),
            "in_degree": len(in_neighbors.get(node, [])),
            "out_degree": len(out_neighbors.get(node, [])),
            "is_dead_end": len(out_neighbors.get(node, [])) == 0,
        }
        for node in nodes
    ]

    # Sample transition matrix M for top 10 nodes for matrix laboratory inspection
    top_items = table[:10]
    top_indices = [nodes.index(item["website"]) for item in top_items]
    top_names = [item["website"] for item in top_items]
    m_sub = res["transition_matrix"][np.ix_(top_indices, top_indices)]
    matrix_sample = {
        "top_names": top_names,
        "matrix": [[round(float(val), 5) for val in row] for row in m_sub],
    }

    payload = {
        "nodes": nodes,
        "node_objects": node_objects,
        "edges": edges,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "density": round(density, 4),
            "iterations": res["iterations"],
            "converged": res["converged"],
            "damping": 0.85,
            "max_error": val["max_error"],
            "is_valid": val["is_valid"],
        },
        "table": table,
        "in_neighbors": in_neighbors,
        "out_neighbors": out_neighbors,
        "diff_history": res["diff_history"],
        "vector_history": res["vector_history"],
        "matrix_sample": matrix_sample,
    }
    return JSONResponse(content=payload)


@app.get("/api/node/{node_name}/breakdown")
def get_node_breakdown(node_name: str, damping: float = 0.85) -> JSONResponse:
    """Return mathematical score decomposition for a specific node."""
    data = load_cached_graph()
    nodes: list[str] = data["nodes"]
    edges: list[list[str]] = data["edges"]
    adj, _ = build_adjacency_matrix(nodes, edges)
    res = power_iteration(adj, d=damping)
    ranks = res["rank_vector"]

    breakdown = compute_score_breakdown(nodes, adj, ranks, node_name, d=damping)
    if "error" in breakdown:
        raise HTTPException(status_code=404, detail=breakdown["error"])
    return JSONResponse(content=breakdown)


@app.post("/api/pagerank/simulate")
def simulate_pagerank(req: SimulateRequest) -> JSONResponse:
    """Simulate hypothetical link modification and project delta PageRank."""
    data = load_cached_graph()
    nodes: list[str] = data["nodes"]
    edges: list[list[str]] = data["edges"]

    result = simulate_link_modification(
        nodes=nodes,
        edges=edges,
        target_node=req.target_node,
        added_in_links=req.added_in_links,
        removed_in_links=req.removed_in_links,
        d=req.damping,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return JSONResponse(content=result)


@app.post("/api/pagerank/calculate")
def recalculate_pagerank(req: CalculateRequest) -> JSONResponse:
    """Dynamically recalculate PageRank with custom damping factor and tolerance."""
    data = load_cached_graph()
    nodes: list[str] = data["nodes"]
    edges: list[list[str]] = data["edges"]

    adj, _ = build_adjacency_matrix(nodes, edges)
    res = power_iteration(adj, d=req.damping, max_iter=req.max_iter, tol=req.tolerance)
    ranks = res["rank_vector"]
    table = generate_ranking_table(nodes, adj, ranks)
    val = validate_with_networkx(nodes, edges, ranks, d=req.damping, tol=req.tolerance)

    payload = {
        "table": table,
        "iterations": res["iterations"],
        "converged": res["converged"],
        "diff_history": res["diff_history"],
        "vector_history": res["vector_history"],
        "val_result": val,
    }
    return JSONResponse(content=payload)


@app.post("/api/crawler/probe")
def probe_crawler(req: ProbeRequest) -> JSONResponse:
    """Live probe crawler endpoint to inspect outbound and internal links on any web portal."""
    target_url = req.url.strip()
    parsed = urlparse(target_url)
    if not parsed.scheme or not parsed.netloc:
        raise HTTPException(
            status_code=400,
            detail="Invalid URL format. Provide http:// or https:// URL.",
        )

    target_host = parsed.netloc.split(":")[0].lower()
    root_host = target_host.removeprefix("www.")

    headers = {
        "User-Agent": "PPW-UTM-PageRankBot/1.0 (+https://trunojoyo.ac.id; student-research)"
    }
    start_time = time.time()
    try:
        resp = requests.get(target_url, headers=headers, timeout=8, verify=False)
        duration_ms = round((time.time() - start_time) * 1000, 1)

        soup = BeautifulSoup(resp.text, "html.parser")
        page_title = (
            soup.title.string.strip()
            if (soup.title and soup.title.string)
            else target_host
        )

        internal_links: set[str] = set()
        external_links: set[str] = set()

        for a in soup.find_all("a", href=True):
            href_val = a.get("href")
            if not isinstance(href_val, str) or not href_val:
                continue
            href_clean = href_val.strip()
            if href_clean.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue

            full_url = urljoin(target_url, href_clean)
            p_full = urlparse(full_url)
            cand_host = p_full.netloc.split(":")[0].lower()

            if cand_host == target_host or (
                cand_host and cand_host.endswith("." + root_host)
            ):
                internal_links.add(full_url)
            elif cand_host:
                external_links.add(full_url)

        payload = {
            "target_url": target_url,
            "target_host": target_host,
            "page_title": page_title,
            "status_code": resp.status_code,
            "duration_ms": duration_ms,
            "internal_links_count": len(internal_links),
            "external_links_count": len(external_links),
            "sample_internal_links": sorted(internal_links)[:15],
            "sample_external_links": sorted(external_links)[:10],
        }
        return JSONResponse(content=payload)
    except (requests.RequestException, OSError) as exc:
        duration_ms = round((time.time() - start_time) * 1000, 1)
        return JSONResponse(
            status_code=502,
            content={
                "target_url": target_url,
                "status_code": 0,
                "duration_ms": duration_ms,
                "error": f"Failed to connect: {exc.__class__.__name__}",
            },
        )


def main():
    """CLI runner for direct execution."""
    import os

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
