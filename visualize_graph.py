#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import networkx as nx
import matplotlib.pyplot as plt
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize_graph.py <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 全ての発言者（ノード）を収集
    speakers = set()
    for category in ["questions", "agreements", "negative_questions"]:
        for speaker, targets in data.get(category, {}).items():
            speakers.add(speaker)
            speakers.update(targets.keys())

    # 有向マルチグラフを作成
    G = nx.MultiDiGraph()
    G.add_nodes_from(speakers)

    # 各種相互作用をエッジとして追加（重み＝回数）
    for category in ["questions", "agreements", "negative_questions"]:
        for speaker, targets in data.get(category, {}).items():
            for target, count in targets.items():
                G.add_edge(speaker, target, interaction=category, weight=count)

    # ノード配置を計算（spring layout）
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10, 8))
    # ノード描画
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="lightyellow", edgecolors="black")
    nx.draw_networkx_labels(G, pos, font_size=12)

    # カテゴリごとにエッジの色分け
    colors = {
        "questions": "red",
        "agreements": "green",
        "negative_questions": "blue"
    }

    # 各カテゴリのエッジを描画
    for category, color in colors.items():
        edges = [(u, v, d) for u, v, d in G.edges(data=True) if d.get("interaction") == category]
        if edges:
            nx.draw_networkx_edges(
                G, pos,
                edgelist=[(u, v) for u, v, d in edges],
                arrowstyle="->",
                arrowsize=20,
                edge_color=color,
                width=2,
                label=category
            )
            # エッジラベルとして「発話回数」を表示
            edge_labels = {(u, v): d.get("weight", 1) for u, v, d in edges}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color=color)

    plt.title("議論における発言者間の相互作用")
    plt.axis("off")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
