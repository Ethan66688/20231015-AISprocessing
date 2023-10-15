#在这一步中根据上述生成的船舶航迹文件进行读取和计算，得到每个港口能直达的国家数量，即得到港口连通性指标

import csv
from collections import defaultdict

# 读取 PORT.csv 文件，创建港口与国家的映射字典
port_data = {}
with open('PORT.csv', 'r', newline='') as port_file:
    reader = csv.reader(port_file)
    next(reader)  # 跳过表头
    for row in reader:
        port_id, port_name, country_name, _, _ = row[:5]
        port_data[port_name] = (port_id, country_name)

# 读取 voyage_info.csv 文件，计算港口连通性
port_connectivity = defaultdict(set)
with open('voyage_info.csv', 'r', newline='') as voyage_file:
    reader = csv.reader(voyage_file)
    next(reader)  # 跳过表头
    for row in reader:
        _, departure_port, _, _, arrival_port, _, arrival_country, _, _ = row
        port_connectivity[departure_port].add(arrival_country)

# 计算每个港口的连通性指标
connectivity_result = []
for port_name, countries in port_connectivity.items():
    port_id, country_name = port_data.get(port_name, ('Unknown', 'Unknown'))
    connectivity_index = len(countries)
    connectivity_result.append((port_id, port_name, country_name, connectivity_index))

# 写入结果到输出文件
with open('port_connectivity.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["Port ID", "Port Name", "Port Country", "Connectivity"])
    writer.writerows(connectivity_result)
