#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Demonstration of finding minimum and maximum spanning trees in a directed complete graph.
This script creates a directed complete graph with 50 nodes, finds the minimum and maximum
spanning trees, and visualizes the process.
"""

import os
import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Add the libs directory to the path so we can import edmkit
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "libs"))
from edmkit.graph import chu_liu_edmonds


def create_complete_digraph(n_nodes, seed=42):
    """
    Create a directed complete graph with random edge weights.

    Parameters
    ----------
    n_nodes : int
        Number of nodes in the graph
    seed : int, optional
        Random seed for reproducibility

    Returns
    -------
    np.ndarray
        Adjacency matrix of the graph
    """
    np.random.seed(seed)

    # Create a complete directed graph with random weights
    # For a directed graph, we need edges in both directions
    adj_matrix = np.random.uniform(1, 10, size=(n_nodes, n_nodes))

    # Set diagonal to 0 (no self-loops)
    np.fill_diagonal(adj_matrix, 0)

    return adj_matrix


def adjacency_to_networkx(adj_matrix):
    """
    Convert an adjacency matrix to a NetworkX DiGraph.

    Parameters
    ----------
    adj_matrix : np.ndarray
        Adjacency matrix of the graph

    Returns
    -------
    nx.DiGraph
        NetworkX directed graph
    """
    G = nx.DiGraph()

    # Add nodes
    for i in range(adj_matrix.shape[0]):
        G.add_node(i)

    # Add edges with weights
    for i in range(adj_matrix.shape[0]):
        for j in range(adj_matrix.shape[1]):
            if adj_matrix[i, j] > 0:
                G.add_edge(i, j, weight=adj_matrix[i, j])

    return G


def get_positions(G, layout="spring"):
    """
    Get node positions for visualization.

    Parameters
    ----------
    G : nx.Graph
        NetworkX graph
    layout : str, optional
        Layout algorithm to use

    Returns
    -------
    dict
        Dictionary of node positions
    """
    if layout == "circular":
        return nx.circular_layout(G)
    elif layout == "spring":
        return nx.spring_layout(G, seed=42, iterations=100)
    elif layout == "kamada_kawai":
        return nx.kamada_kawai_layout(G)
    elif layout == "shell":
        return nx.shell_layout(G)
    else:
        return nx.circular_layout(G)


def visualize_graph_and_mst(adj_matrix, mst_min, mst_max, root=0, layout="spring", title="Directed Graph and Spanning Trees"):
    """
    Visualize the original graph, minimum spanning tree, and maximum spanning tree.

    Parameters
    ----------
    adj_matrix : np.ndarray
        Adjacency matrix of the original graph
    mst_min : np.ndarray
        Adjacency matrix of the minimum spanning tree
    mst_max : np.ndarray
        Adjacency matrix of the maximum spanning tree
    title : str, optional
        Title of the figure
    root : int, optional
        Root node for the spanning tree
    layout : str, optional
        Layout algorithm to use for node positioning
    """
    print("Visualizing spanning trees...")
    n_nodes = adj_matrix.shape[0]

    # Create figure with 2 subplots (removing the original graph)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(title, fontsize=16)

    # Set subplot titles
    axes[0].set_title("Minimum Spanning Tree")
    axes[1].set_title("Maximum Spanning Tree")

    # Convert adjacency matrices to NetworkX graphs
    G_min = adjacency_to_networkx(mst_min)
    G_max = adjacency_to_networkx(mst_max)

    # Get positions using the specified layout
    pos = get_positions(G_min, layout=layout)

    # Create a color map for nodes based on their IDs
    colors = plt.cm.viridis(np.linspace(0, 1, n_nodes))
    node_colors = {i: colors[i] for i in range(n_nodes)}

    # Create node lists for drawing
    all_nodes = list(range(n_nodes))
    root_node = [root]

    # Draw the minimum spanning tree
    print("Drawing minimum spanning tree...")
    nx.draw_networkx_nodes(
        G_min,
        pos,
        ax=axes[0],
        nodelist=[n for n in all_nodes if n != root],
        node_color=[node_colors[n] for n in all_nodes if n != root],
        node_size=50,
    )
    nx.draw_networkx_nodes(G_min, pos, ax=axes[0], nodelist=root_node, node_color="red", node_size=100, node_shape="s")
    nx.draw_networkx_edges(G_min, pos, ax=axes[0], edge_color="red", arrows=True)
    nx.draw_networkx_labels(G_min, pos, ax=axes[0], labels={i: str(i) for i in range(n_nodes)}, font_size=8)

    # Draw the maximum spanning tree
    print("Drawing maximum spanning tree...")
    nx.draw_networkx_nodes(
        G_max,
        pos,
        ax=axes[1],
        nodelist=[n for n in all_nodes if n != root],
        node_color=[node_colors[n] for n in all_nodes if n != root],
        node_size=50,
    )
    nx.draw_networkx_nodes(G_max, pos, ax=axes[1], nodelist=root_node, node_color="red", node_size=100, node_shape="s")
    nx.draw_networkx_edges(G_max, pos, ax=axes[1], edge_color="green", arrows=True)
    nx.draw_networkx_labels(G_max, pos, ax=axes[1], labels={i: str(i) for i in range(n_nodes)}, font_size=8)

    # Remove axis ticks
    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.savefig("spanning_trees.png", dpi=300, bbox_inches="tight")


def visualize_algorithm_steps(adj_matrix, root=0, layout="spring"):
    """
    Visualize the steps of the Chu-Liu/Edmonds algorithm.

    Parameters
    ----------
    adj_matrix : np.ndarray
        Adjacency matrix of the graph
    root : int, optional
        Root node for the spanning tree
    layout : str, optional
        Layout algorithm to use for node positioning
    """
    print("Starting algorithm visualization...")
    n_nodes = adj_matrix.shape[0]
    G_original = adjacency_to_networkx(adj_matrix)
    pos = get_positions(G_original, layout=layout)

    # Create a color map for nodes based on their IDs
    colors = plt.cm.viridis(np.linspace(0, 1, n_nodes))
    node_colors = {i: colors[i] for i in range(n_nodes)}

    # Create figure with 3 subplots (removing the original graph)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("Chu-Liu/Edmonds Algorithm Steps", fontsize=16)

    # Set subplot titles
    axes[0].set_title("1. Find Optimal Incoming Edges")
    axes[1].set_title("2. Check for Cycles")
    axes[2].set_title("3. Final Minimum Spanning Tree")

    # Create node lists for drawing
    all_nodes = list(range(n_nodes))
    root_node = [root]

    # 2. Find Optimal Incoming Edges
    # For each node (except root), find the minimum incoming edge
    optimal_edges = {}
    for v in range(n_nodes):
        if v == root:
            continue
        print(f"Step 1: Finding optimal incoming edge for node {v}...")

        # Find the minimum incoming edge
        min_weight = float("inf")
        min_edge = None

        for u in range(n_nodes):
            if adj_matrix[u, v] > 0 and adj_matrix[u, v] < min_weight:
                min_weight = adj_matrix[u, v]
                min_edge = (u, v)

        if min_edge:
            optimal_edges[min_edge] = min_weight

    # Create a graph with only the optimal incoming edges
    G_optimal = nx.DiGraph()
    for i in range(n_nodes):
        G_optimal.add_node(i)

    for edge, weight in optimal_edges.items():
        G_optimal.add_edge(edge[0], edge[1], weight=weight)

    # Draw the graph with optimal incoming edges
    nx.draw_networkx_nodes(
        G_optimal,
        pos,
        ax=axes[0],
        nodelist=[n for n in all_nodes if n != root],
        node_color=[node_colors[n] for n in all_nodes if n != root],
        node_size=50,
    )
    nx.draw_networkx_nodes(G_optimal, pos, ax=axes[0], nodelist=root_node, node_color="red", node_size=100, node_shape="s")
    nx.draw_networkx_edges(G_optimal, pos, ax=axes[0], edge_color="red", arrows=True)
    nx.draw_networkx_labels(G_optimal, pos, ax=axes[0], labels={i: str(i) for i in range(n_nodes)}, font_size=8)

    # 3. Check for Cycles
    # Find cycles in the graph
    print("Step 2: Checking for cycles...")
    cycles = list(nx.simple_cycles(G_optimal))

    if cycles:
        print(f"Found {len(cycles)} cycles: {cycles}")

    # Create a graph highlighting the cycles
    G_cycles = nx.DiGraph()
    for i in range(n_nodes):
        G_cycles.add_node(i)

    cycle_edges = set()
    for cycle in cycles:
        for i in range(len(cycle)):
            u = cycle[i]
            v = cycle[(i + 1) % len(cycle)]
            cycle_edges.add((u, v))

    for edge, weight in optimal_edges.items():
        G_cycles.add_edge(edge[0], edge[1], weight=weight)

    # Draw the graph with cycles highlighted
    edge_colors = ["red" if edge in cycle_edges else "green" for edge in G_cycles.edges()]
    nx.draw_networkx_nodes(
        G_cycles,
        pos,
        ax=axes[1],
        nodelist=[n for n in all_nodes if n != root],
        node_color=[node_colors[n] for n in all_nodes if n != root],
        node_size=50,
    )
    nx.draw_networkx_nodes(G_cycles, pos, ax=axes[1], nodelist=root_node, node_color="red", node_size=100, node_shape="s")
    nx.draw_networkx_edges(G_cycles, pos, ax=axes[1], edge_color=edge_colors, arrows=True)
    nx.draw_networkx_labels(G_cycles, pos, ax=axes[1], labels={i: str(i) for i in range(n_nodes)}, font_size=8)

    # 4. Final Minimum Spanning Tree
    print("Step 3: Computing final minimum spanning tree...")
    mst_min = chu_liu_edmonds(adj_matrix, root, maximize=False)
    G_mst = adjacency_to_networkx(mst_min)

    # Draw the minimum spanning tree
    nx.draw_networkx_nodes(
        G_mst,
        pos,
        ax=axes[2],
        nodelist=[n for n in all_nodes if n != root],
        node_color=[node_colors[n] for n in all_nodes if n != root],
        node_size=50,
    )
    nx.draw_networkx_nodes(G_mst, pos, ax=axes[2], nodelist=root_node, node_color="red", node_size=100, node_shape="s")
    nx.draw_networkx_edges(G_mst, pos, ax=axes[2], edge_color="green", arrows=True)
    nx.draw_networkx_labels(G_mst, pos, ax=axes[2], labels={i: str(i) for i in range(n_nodes)}, font_size=8)

    print("Minimum spanning tree computed successfully!")

    # Remove axis ticks
    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.savefig("algorithm_steps.png", dpi=300, bbox_inches="tight")


def main():
    """Main function to demonstrate the spanning tree algorithms."""
    print("Starting spanning tree demonstration...")
    # Number of nodes in the graph
    n_nodes = 50

    # Create a directed complete graph with random weights
    adj_matrix = create_complete_digraph(n_nodes)

    # Choose a root node
    root = 0
    print(f"Using node {root} as the root node for spanning trees")

    # Find the minimum spanning tree
    print("Computing minimum spanning tree...")
    mst_min = chu_liu_edmonds(adj_matrix, root, maximize=False)

    # Find the maximum spanning tree
    print("Computing maximum spanning tree...")
    mst_max = chu_liu_edmonds(adj_matrix, root, maximize=True)

    # Visualize the graph and spanning trees
    visualize_graph_and_mst(adj_matrix, mst_min, mst_max, root=root, layout="spring")
    print("Generated spanning_trees.png")

    # Visualize the algorithm steps
    # Use a smaller graph for better visualization
    small_adj_matrix = create_complete_digraph(15)
    visualize_algorithm_steps(small_adj_matrix, root=0, layout="kamada_kawai")
    print("Generated algorithm_steps.png")


if __name__ == "__main__":
    main()
