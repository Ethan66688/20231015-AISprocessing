#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 15:25:22 2023

@author: yuexiang
"""

import pandas as pd
import networkx as nx

# 創建一個空的無向圖
G = nx.Graph()

# 讀取包含港口對的CSV文件
csv_file = "港口對.csv"  # 替換為你的CSV文件路徑
df = pd.read_csv(csv_file)

# 迭代CSV文件中的每一行，將港口對添加為邊
for index, row in df.iterrows():
    port1 = row['港口1列名']  # 替換為CSV文件中港口1的列名
    port2 = row['港口2列名']  # 替換為CSV文件中港口2的列名
    G.add_edge(port1, port2)

# 計算中心性
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

# 將中心性數據轉換為DataFrame
centrality_data = pd.DataFrame({
    '港口': list(degree_centrality.keys()),
    '度中心性': list(degree_centrality.values()),
    '接近度中心性': list(closeness_centrality.values()),
    '介入度中心性': list(betweenness_centrality.values())
})

# 保存中心性數據到CSV文件
output_file = "港口中心性.csv"  # 替換為你想要保存的文件名
centrality_data.to_csv(output_file, index=False)
