#由于在生成航迹文件到计算战略重要性的过程中发现港口对应的上下游距离不明确，遂单独生成了一个上下游文件。

import pandas as pd

# 读取数据，不指定列名，使用默认的列索引
all_distances_df = pd.read_csv('all_distances.csv')

# 添加上游距离和下游距离列
all_distances_df['UpstreamDistance'] = all_distances_df.groupby('IMO')['Distance'].shift()
all_distances_df['DownstreamDistance'] = all_distances_df['Distance']

# 获取每艘船舶的第一行的索引
first_row_indices = all_distances_df.groupby('IMO').head(1).index

# 将第一行的上游距离设置为 NaN
all_distances_df.loc[first_row_indices, 'UpstreamDistance'] = None

# 选择所需的列并保存到文件
result_df = all_distances_df[['IMO', 'DeparturePort', 'DepartureCountry', 'UpstreamDistance', 'DownstreamDistance']]
result_df.to_csv('output_file.csv', index=False)
