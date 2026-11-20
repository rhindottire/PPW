"""Unit tests for deploy/pagerank_engine.py."""

import numpy as np

from deploy.pagerank_engine import (
    build_adjacency_matrix,
    build_stochastic_matrix,
    compute_score_breakdown,
    generate_ranking_table,
    power_iteration,
    simulate_link_modification,
    validate_with_networkx,
)


def test_build_adjacency_matrix():
    nodes = ["a.trunojoyo.ac.id", "b.trunojoyo.ac.id", "c.trunojoyo.ac.id"]
    edges = [
        ["a.trunojoyo.ac.id", "b.trunojoyo.ac.id"],
        ["b.trunojoyo.ac.id", "c.trunojoyo.ac.id"],
        ["c.trunojoyo.ac.id", "a.trunojoyo.ac.id"],
    ]
    adj, node_map = build_adjacency_matrix(nodes, edges)

    assert adj.shape == (3, 3)
    assert adj[node_map["a.trunojoyo.ac.id"], node_map["b.trunojoyo.ac.id"]] == 1
    assert adj[node_map["b.trunojoyo.ac.id"], node_map["c.trunojoyo.ac.id"]] == 1
    assert adj[node_map["c.trunojoyo.ac.id"], node_map["a.trunojoyo.ac.id"]] == 1
    assert adj[node_map["a.trunojoyo.ac.id"], node_map["c.trunojoyo.ac.id"]] == 0


def test_stochastic_matrix_column_sum_and_dead_ends():
    # Node 2 has no outgoing edges (dead end)
    adj = np.array(
        [
            [0, 1, 1],
            [0, 0, 1],
            [0, 0, 0],
        ]
    )
    m = build_stochastic_matrix(adj)

    assert m.shape == (3, 3)
    # Column 0: node 0 has 2 outgoing edges (to 1 and 2), so m[1, 0] = 0.5, m[2, 0] = 0.5
    assert np.isclose(m[1, 0], 0.5)
    assert np.isclose(m[2, 0], 0.5)
    assert np.isclose(m[0, 0], 0.0)

    # Column 2 is a dead end -> each row in column 2 must be 1/3
    assert np.allclose(m[:, 2], 1.0 / 3.0)

    # Every column must sum to exactly 1.0
    col_sums = m.sum(axis=0)
    assert np.allclose(col_sums, 1.0)


def test_power_iteration_and_networkx_validation():
    nodes = ["node1", "node2", "node3", "node4"]
    edges = [
        ["node1", "node2"],
        ["node1", "node3"],
        ["node2", "node4"],
        ["node3", "node1"],
        ["node3", "node4"],
        ["node4", "node1"],
    ]
    adj, _ = build_adjacency_matrix(nodes, edges)
    res = power_iteration(adj, d=0.85, max_iter=200, tol=1e-8)

    assert res["converged"] is True
    ranks = res["rank_vector"]
    assert np.isclose(np.sum(ranks), 1.0)
    assert "vector_history" in res
    assert len(res["vector_history"]) == res["iterations"] + 1

    val = validate_with_networkx(nodes, edges, ranks, d=0.85, tol=1e-8)
    assert val["is_valid"] is True
    assert val["max_error"] < 1e-4


def test_generate_ranking_table():
    nodes = ["alpha", "beta"]
    adj = np.array([[0, 1], [0, 0]])
    ranks = np.array([0.3, 0.7])

    table = generate_ranking_table(nodes, adj, ranks)
    assert len(table) == 2
    assert table[0]["website"] == "beta"
    assert table[0]["rank"] == 1
    assert table[1]["website"] == "alpha"
    assert table[1]["rank"] == 2


def test_compute_score_breakdown():
    nodes = ["a", "b", "c"]
    edges = [["a", "b"], ["b", "c"], ["c", "a"]]
    adj, _ = build_adjacency_matrix(nodes, edges)
    res = power_iteration(adj, d=0.85)
    ranks = res["rank_vector"]

    breakdown = compute_score_breakdown(nodes, adj, ranks, "b", d=0.85)
    assert breakdown["target_node"] == "b"
    assert breakdown["referrers_count"] == 1
    assert breakdown["referrers"][0]["referrer"] == "a"
    assert np.isclose(breakdown["current_pagerank"], 1.0 / 3.0, atol=1e-3)
    assert breakdown["base_teleport"] == (1.0 - 0.85) / 3.0


def test_simulate_link_modification():
    nodes = ["a", "b", "c"]
    edges = [["a", "b"], ["c", "a"]]
    # b is originally only referenced by a. If c also references b, b's PR must increase.
    sim = simulate_link_modification(
        nodes, edges, target_node="b", added_in_links=["c"], d=0.85
    )
    assert sim["target_node"] == "b"
    assert sim["delta_pr"] > 0
    assert sim["new_pagerank"] > sim["original_pagerank"]
