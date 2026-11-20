"""PageRank computational engine and mathematical verification module.

Provides:
- Adjacency matrix construction
- Column-stochastic transition matrix M with dead-end handling
- Manual power iteration algorithm with damping factor d
- Numerical validation against networkx.pagerank
"""

from typing import Any, cast

import networkx as nx
import numpy as np


def build_adjacency_matrix(
    nodes: list[str], edges: list[list[str]]
) -> tuple[np.ndarray, dict[str, int]]:
    """Build directed adjacency matrix A where A[i, j] = 1 represents edge i -> j."""
    node_to_idx = {name: idx for idx, name in enumerate(nodes)}
    n = len(nodes)
    adj = np.zeros((n, n), dtype=int)
    for u, v in edges:
        if u in node_to_idx and v in node_to_idx:
            adj[node_to_idx[u], node_to_idx[v]] = 1
    return adj, node_to_idx


def build_stochastic_matrix(adj: np.ndarray) -> np.ndarray:
    """Build column-stochastic transition matrix M.

    M[i, j] represents probability of transitioning from node j to node i.
    Handles dead ends (k_out = 0) by distributing uniform probability 1/N across the column.
    """
    n = adj.shape[0]
    out_degrees = adj.sum(axis=1)  # sum of row i is out-degree of i
    m = np.zeros((n, n), dtype=float)

    for j in range(n):
        k_out = out_degrees[j]
        if k_out > 0:
            # Transition probability from j to i is adj[j, i] / k_out
            m[:, j] = adj[j, :] / k_out
        else:
            # Dead-end handling: teleport equally to all nodes
            m[:, j] = 1.0 / n

    return m


def power_iteration(
    adj: np.ndarray,
    d: float = 0.85,
    max_iter: int = 200,
    tol: float = 1e-7,
) -> dict[str, Any]:
    """Calculate PageRank vector using Power Iteration method.

    Formula:
        r^(k+1) = ((1 - d) / N) * e + d * M * r^(k)
    """
    n = adj.shape[0]
    if n == 0:
        return {
            "rank_vector": np.array([]),
            "iterations": 0,
            "converged": True,
            "diff_history": [],
        }

    m = build_stochastic_matrix(adj)
    r = np.full(n, 1.0 / n, dtype=float)
    teleport = ((1.0 - d) / n) * np.ones(n, dtype=float)

    diff_history: list[float] = []
    vector_history: list[list[float]] = [[round(float(x), 6) for x in r]]
    converged = False
    iterations = 0

    for it in range(1, max_iter + 1):
        r_next = teleport + d * np.dot(m, r)
        diff = float(np.sum(np.abs(r_next - r)))
        diff_history.append(diff)
        vector_history.append([round(float(x), 6) for x in r_next])
        r = r_next
        iterations = it

        if diff < tol:
            converged = True
            break

    # Normalize vector to ensure sum is strictly 1.0
    r_sum = float(np.sum(r))
    if r_sum > 0:
        r = r / r_sum

    return {
        "rank_vector": r,
        "iterations": iterations,
        "converged": converged,
        "diff_history": diff_history,
        "vector_history": vector_history,
        "transition_matrix": m,
    }


def validate_with_networkx(
    nodes: list[str],
    edges: list[list[str]],
    manual_ranks: np.ndarray,
    d: float = 0.85,
    tol: float = 1e-7,
) -> dict[str, Any]:
    """Validate numerical accuracy against NetworkX implementation."""
    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    for u, v in edges:
        g.add_edge(u, v)

    nx_pr = cast(dict[str, float], nx.pagerank(g, alpha=d, tol=tol, max_iter=500))
    nx_vector = np.array([nx_pr[node] for node in nodes])

    abs_diff = np.abs(manual_ranks - nx_vector)
    max_error = float(np.max(abs_diff)) if len(abs_diff) > 0 else 0.0
    mean_error = float(np.mean(abs_diff)) if len(abs_diff) > 0 else 0.0

    return {
        "networkx_ranks": nx_pr,
        "max_error": max_error,
        "mean_error": mean_error,
        "is_valid": max_error < 1e-4,
    }


def generate_ranking_table(
    nodes: list[str],
    adj: np.ndarray,
    ranks: np.ndarray,
) -> list[dict[str, Any]]:
    """Generate structured ranking table sorted by PageRank score."""
    out_degrees = adj.sum(axis=1)
    in_degrees = adj.sum(axis=0)

    items = []
    for idx, node in enumerate(nodes):
        items.append(
            {
                "website": node,
                "in_degree": int(in_degrees[idx]),
                "out_degree": int(out_degrees[idx]),
                "pagerank": float(ranks[idx]),
            }
        )

    # Sort descending by PageRank score
    items.sort(key=lambda x: x["pagerank"], reverse=True)
    for rank_idx, item in enumerate(items, start=1):
        item["rank"] = rank_idx

    return items


def compute_score_breakdown(
    nodes: list[str],
    adj: np.ndarray,
    ranks: np.ndarray,
    target_node: str,
    d: float = 0.85,
) -> dict[str, Any]:
    """Decompose PageRank score into teleportation and referrer link contributions.

    Formula:
        PR(i) = (1 - d)/N + sum_{j in dead_ends} (d * PR(j) / N) + sum_{j -> i} (d * PR(j) / k_out(j))
    """
    if target_node not in nodes:
        return {"error": f"Node '{target_node}' not found in graph."}

    target_idx = nodes.index(target_node)
    n = len(nodes)
    if n == 0:
        return {"error": "Empty node list."}

    current_pr = float(ranks[target_idx])
    base_teleport = (1.0 - d) / n

    out_degrees = adj.sum(axis=1)
    dead_end_sum = 0.0
    for j in range(n):
        if out_degrees[j] == 0:
            dead_end_sum += d * float(ranks[j]) / n

    referrers: list[dict[str, Any]] = []
    referrers_sum = 0.0

    for j in range(n):
        if adj[j, target_idx] == 1:
            k_out = int(out_degrees[j])
            raw_contrib = d * float(ranks[j]) / k_out if k_out > 0 else 0.0
            referrers_sum += raw_contrib
            percentage = (raw_contrib / current_pr * 100.0) if current_pr > 0 else 0.0
            referrers.append(
                {
                    "referrer": nodes[j],
                    "referrer_pr": float(ranks[j]),
                    "referrer_out_degree": k_out,
                    "contribution": float(raw_contrib),
                    "percentage": round(percentage, 2),
                    "is_bidirectional": bool(adj[target_idx, j] == 1),
                }
            )

    referrers.sort(key=lambda x: x["contribution"], reverse=True)

    return {
        "target_node": target_node,
        "current_pagerank": current_pr,
        "base_teleport": float(base_teleport),
        "dead_end_teleport": float(dead_end_sum),
        "referrers_contribution_sum": float(referrers_sum),
        "referrers_count": len(referrers),
        "referrers": referrers,
        "damping_factor": d,
    }


def simulate_link_modification(
    nodes: list[str],
    edges: list[list[str]],
    target_node: str,
    added_in_links: list[str] | None = None,
    removed_in_links: list[str] | None = None,
    d: float = 0.85,
) -> dict[str, Any]:
    """Simulate link addition/removal and project the new PageRank score and rank."""
    if target_node not in nodes:
        return {"error": f"Node '{target_node}' not found."}

    added_in_links = added_in_links or []
    removed_in_links = removed_in_links or []

    # Original PageRank calculation
    orig_adj, _ = build_adjacency_matrix(nodes, edges)
    orig_res = power_iteration(orig_adj, d=d)
    orig_ranks = orig_res["rank_vector"]
    orig_ranking = generate_ranking_table(nodes, orig_adj, orig_ranks)

    target_orig_info = next(
        item for item in orig_ranking if item["website"] == target_node
    )
    orig_pr = target_orig_info["pagerank"]
    orig_rank = target_orig_info["rank"]

    # Build modified edge list
    mod_edges_set = {tuple(e) for e in edges}
    for src in added_in_links:
        if src in nodes and src != target_node:
            mod_edges_set.add((src, target_node))

    for src in removed_in_links:
        mod_edges_set.discard((src, target_node))

    mod_edges = [list(e) for e in mod_edges_set]

    # Recompute on modified graph
    mod_adj, _ = build_adjacency_matrix(nodes, mod_edges)
    mod_res = power_iteration(mod_adj, d=d)
    mod_ranks = mod_res["rank_vector"]
    mod_ranking = generate_ranking_table(nodes, mod_adj, mod_ranks)

    target_mod_info = next(
        item for item in mod_ranking if item["website"] == target_node
    )
    new_pr = target_mod_info["pagerank"]
    new_rank = target_mod_info["rank"]

    delta_pr = new_pr - orig_pr
    delta_percentage = (delta_pr / orig_pr * 100.0) if orig_pr > 0 else 0.0
    rank_change = (
        orig_rank - new_rank
    )  # positive means improved rank (e.g. 5 -> 3 = +2)

    return {
        "target_node": target_node,
        "original_pagerank": orig_pr,
        "original_rank": orig_rank,
        "new_pagerank": new_pr,
        "new_rank": new_rank,
        "delta_pr": delta_pr,
        "delta_percentage": round(delta_percentage, 2),
        "rank_change": rank_change,
        "added_in_links": added_in_links,
        "removed_in_links": removed_in_links,
        "iterations": mod_res["iterations"],
    }
