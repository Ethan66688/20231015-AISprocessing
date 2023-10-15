#由于原始数据量太大，作者的macbook实在是跑不出来，遂放弃了一整个代码完成数据分析的想法，改用分功能分步处理；
#根据船舶在港口停泊的几个指标的优先级，先对优先级最低的指标进行筛选————如果速度不小于1，则直接删除该数据。原数据有100万条左右，删后只有6万多条；
#由于直接进行停泊判断要遍历数据库并且循环很多次，即使用了Numpy之类的库作者的电脑还是没法跑出来，遂先针对每艘船舶的IMO号，对每艘船舶建立一个动态信息库。
#其中每艘船舶的信息由时间戳记的先后顺序排列，由此进行循环判断停泊事件，并删除短时间内多次停留的记录、在多个港口范围内只取最近的

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
