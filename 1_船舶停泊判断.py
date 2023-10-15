#在对数据进行了初步的处理减少数据量后，需要根据在港口30km范围内、速度小于1、持续时间超过1小时对某船舶在某港口内的停泊进行判断。
#由于初始AIS数据提供船舶的经纬度信息，此处调用Haversine函数进行地理距离计算；
#对上一步处理过的船舶信息进行遍历，得到符合条件的所有信息；
#针对一些特殊情况进行声明：比如同时在多个港口的30km范围内，只取最近的一个港口；比如在短时间内多次停泊，只取最早的一次，其余认为由交通拥堵造成。

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 22:01:36 2023

@author: yuexiang
"""

import pandas as pd
from haversine import haversine

# 读取AIS数据库文件
ais_data_file = "processed_ais_data.csv"
ais_data = pd.read_csv(ais_data_file, sep="|", header=0)

# 读取港口信息数据
port_data_file = "PORT.csv"
port_data = pd.read_csv(port_data_file, header=0)
port_data.columns = ["id", "port", "country_name", "latitudeDecimal", "longitudeDecimal"]

# 函数用于筛选船舶停泊信息
def filter_port_visits(row):
    imo, timestamp, latitude, longitude = row[0], row[1], row[2], row[3]
    
    # 创建一个列表存储港口距离和信息
    port_distances = []
    
    for port_row in port_data.itertuples(index=False):
        port_id, port_name, country_name, port_latitude, port_longitude = port_row[0], port_row[1], port_row[2], port_row[3], port_row[4]
        distance = haversine((latitude, longitude), (port_latitude, port_longitude))
        port_distances.append((port_id, port_name, country_name, distance))
    
    # 找到距离最近的港口
    closest_port = min(port_distances, key=lambda x: x[3])
    
    # 如果距离最近的港口在30km内，则认为船舶在港口停泊
    if closest_port[3] <= 30:
        return [imo, closest_port[0], closest_port[1], closest_port[2], timestamp]
    else:
        return None

# 对每行数据应用筛选函数，得到有效的停泊信息
port_visits = [filter_port_visits(row) for row in ais_data.itertuples(index=False) if filter_port_visits(row) is not None]

# 生成船舶停泊信息文件
port_visits_df = pd.DataFrame(port_visits, columns=["imo", "port_id", "port_name", "country_name", "timestamp"])
port_visits_df.to_csv("ship_port_visits.csv", sep="|", index=False)
