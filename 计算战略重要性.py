import pandas as pd
import math

# 读取数据，不指定列名，使用默认的列索引
all_distances_df = pd.read_csv('上下游distances.csv')

# 使用0填充空值
all_distances_df[['UpstreamDistance', 'DownstreamDistance']] = all_distances_df[['UpstreamDistance', 'DownstreamDistance']].fillna(0)

# 计算累加所有UpstreamDistance和DownstreamDistance，求均值，a
a = (all_distances_df['UpstreamDistance'] + all_distances_df['DownstreamDistance']).mean()

# 对于每个特定的DeparturePort，选择它所有的UpstreamDistance和DownstreamDistance，求最大的10%的数据的均值，b
def calculate_b(group):
    max_values = group.nlargest(math.ceil(0.1 * len(group)))
    return int(max_values.mean())

b_values = all_distances_df.groupby('DeparturePort')['UpstreamDistance'].apply(calculate_b).reset_index()

# 计算战略重要性指标，b/a
strategic_importance = b_values['UpstreamDistance'] / a

# 创建结果DataFrame
result_df = pd.DataFrame({'PortName': b_values['DeparturePort'], 'StrategicImportance': strategic_importance})

# 保存结果到文件
result_df.to_csv('strategic_importance.csv', index=False)
