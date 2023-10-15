#在该脚本中会根据船舶在不同时间在不同港口的停泊事件生成船舶的航迹信息；
#对船舶的停泊事件进行计数，得到各个港口的船舶访问量（第一个评价指标）
#生成航迹文件，其中包括船舶IMO、出发港口与国家、到达港口与国家、航程时间、航程里程（从而能够计算港口角度的后两个指标）

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 00:18:11 2023

@author: yuexiang
"""
import csv
from collections import defaultdict
from geopy.distance import geodesic
from datetime import datetime

# 读取 PORT.csv 文件
port_data = {}
with open('PORT.csv', 'r', newline='') as port_file:
    reader = csv.reader(port_file)
    next(reader)  # 跳过表头
    for row in reader:
        port_id, port_name, country_name, latitude, longitude = row[:5]
        port_data[port_id] = (port_name, country_name, float(latitude), float(longitude))

# Step 2: 生成船舶航线信息
def generate_voyage_info():
    voyage_info = {}
    with open('ship_port_visits.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        next(reader)  # 跳过表头
        for row in reader:
            imo, port_id, _, _, timestamp = row[:5]
            if imo not in voyage_info:
                voyage_info[imo] = []
            voyage_info[imo].append((port_id, timestamp))

    with open('voyage_info.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IMO", "Departure Port", "Departure Time", "Departure Country", "Arrival Port", "Arrival Time", "Arrival Country", "Voyage Duration (hours)", "Distance (km)"])
        for imo, ports in voyage_info.items():
            for i in range(len(ports) - 1):
                departure_port, departure_time = ports[i]
                arrival_port, arrival_time = ports[i + 1]
                departure_name, departure_country, departure_latitude, departure_longitude = port_data[departure_port]
                arrival_name, arrival_country, arrival_latitude, arrival_longitude = port_data[arrival_port]
                # 计算航程时间和距离
                voyage_duration, distance = calculate_voyage_info(departure_time, arrival_time, (departure_latitude, departure_longitude), (arrival_latitude, arrival_longitude))
                writer.writerow([imo, departure_name, departure_time, departure_country, arrival_name, arrival_time, arrival_country, voyage_duration, distance])

# 计算航程时间和距离
def calculate_voyage_info(departure_time, arrival_time, departure_coords, arrival_coords):
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    departure_time = datetime.strptime(departure_time, timestamp_format)
    arrival_time = datetime.strptime(arrival_time, timestamp_format)
    voyage_duration = (arrival_time - departure_time).total_seconds() / 3600  # 转换为小时

    distance = geodesic(departure_coords, arrival_coords).kilometers

    return voyage_duration, distance

# 主程序
if __name__ == "__main__":
    generate_voyage_info()
