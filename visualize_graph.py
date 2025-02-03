#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import matplotlib.pyplot as plt
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize_bar_chart.py <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 各カテゴリーごとの発話回数を集計
    categories = ["questions", "agreements", "negative_questions"]
    category_counts = {category: 0 for category in categories}

    for category in categories:
        for speaker, targets in data.get(category, {}).items():
            for target, count in targets.items():
                category_counts[category] += count

    # 棒グラフの作成
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = {"questions": "red", "agreements": "green", "negative_questions": "blue"}
    bars = ax.bar(category_counts.keys(), category_counts.values(),
                  color=[colors[cat] for cat in categories])
    
    ax.set_xlabel("相互作用の種類")
    ax.set_ylabel("発話回数"
    ax.set_title("議論における発言者間の相互作用（合計）")

    # 棒に回数を表示
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{int(height)}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
