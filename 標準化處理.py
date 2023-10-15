#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 16:42:12 2023

@author: yuexiang
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler

# 读取CSV文件
csv_file = "標準化處理.csv"  # 替换为你的CSV文件路径
df = pd.read_csv(csv_file, encoding="utf-8")

# 初始化标准化处理器
scaler = StandardScaler()

# 对每一列（包括标题行）进行标准化处理
df_standardized = df.copy()  # 复制原始DataFrame以保留原始数据
for column in df.columns:
    df_standardized[column] = scaler.fit_transform(df[[column]])

# 保存处理后的结果到新的CSV文件
output_file = "standardized_data.csv"  # 替换为你想要保存的文件名
df_standardized.to_csv(output_file, index=False, encoding="utf-8")
