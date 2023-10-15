import pandas as pd

# 读取AIS数据库文件
ais_data_file = "AIS202001.csv"
ais_data = pd.read_csv(ais_data_file, sep="|", header=0)

# 将timestamp列转换为datetime类型
ais_data['timestamp'] = pd.to_datetime(ais_data['timestamp'])

# 删除速度大于1的数据
ais_data = ais_data[ais_data['speed'] <= 1]

# 按照船舶imo进行分组
grouped = ais_data.groupby('imo')

# 函数用于筛选船舶数据
def filter_ship_data(ship_data):
    ship_data = ship_data.sort_values('timestamp')  # 按时间戳升序排序
    ship_data['time_diff'] = ship_data['timestamp'].diff().dt.total_seconds()  # 计算时间差

    # 保留第一条记录和时间差大于3小时的记录
    filtered_data = ship_data[(ship_data['time_diff'].isnull()) | (ship_data['time_diff'] > 10800)]
    filtered_data.drop(columns=['time_diff'], inplace=True)

    return filtered_data

# 对每艘船的数据进行筛选
filtered_ais_data = grouped.apply(filter_ship_data).reset_index(drop=True)

# 生成处理后的AIS数据文件
filtered_ais_data.to_csv("processed_ais_data.csv", sep="|", index=False)
