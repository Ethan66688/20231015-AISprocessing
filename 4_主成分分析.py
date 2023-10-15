#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 16:26:37 2023

@author: yuexiang
"""

import pandas as pd
from sklearn.decomposition import PCA

# 讀取CSV文件，替換為你的CSV文件路徑
csv_file = "standardized_data.csv"
df = pd.read_csv(csv_file, encoding="utf-8")

# 創建PCA模型，指定要保留的主成分數為6
pca = PCA(n_components=6)  # 這裡設為6

# 提取數據（不包含港口名稱列）
data = df.iloc[:, 1:]  # 假設港口名稱列在第一列，所以我們提取第2列到最後一列

# 適配模型並轉換數據
pca_result = pca.fit_transform(data)

# 主成分的特徵值
explained_variance = pca.explained_variance_

# 主成分的解釋方差比例
explained_variance_ratio = pca.explained_variance_ratio_

# 創建一個新DataFrame來保存PCA結果
pca_df = pd.DataFrame(pca_result, columns=["PCA_Component_" + str(i) for i in range(1, 7)])

# 將PCA結果連接到原始數據中（包括港口名稱）
result_df = pd.concat([df["PORT"], pca_df], axis=1)

# 保存帶有PCA結果的新CSV文件
output_file = "pca_result.csv"  # 替換為你想要保存的文件名
result_df.to_csv(output_file, index=False, encoding="utf-8")

# 打印主成分分析結果
print("PCA Result:")
print(pca_result)

# 打印主成分的特徵值
print("\nExplained Variance:")
print(explained_variance)

# 打印主成分的解釋方差比例
print("\nExplained Variance Ratio:")
print(explained_variance_ratio)

# 获取主成分的特征向量
components = pca.components_

# 打印特征向量
print("Principal Components (Feature Vectors):")
print(components)
