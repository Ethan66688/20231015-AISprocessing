import csv
from collections import defaultdict
from geopy.distance import geodesic
from datetime import datetime

# Step 1: 计算港口访问量
def calculate_port_visits():
    port_visits = defaultdict(int)
    with open('ship_port_visits.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        next(reader)  # 跳过表头
        for row in reader:
            port_id, port_name, country_name, _ = row[1:5]
            port_visits[(port_id, port_name, country_name)] += 1

    sorted_port_visits = sorted(port_visits.items(), key=lambda x: x[1], reverse=True)

    with open('port_visits.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Port ID", "Port Name", "Country", "Total Visits"])
        writer.writerows([(port_id, port_name, country_name, visits) for (port_id, port_name, country_name), visits in sorted_port_visits])

# Step 2: 生成船舶航线信息
def generate_voyage_info():
    voyage_info = {}
    with open('ship_port_visits.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        next(reader)  # 跳过表头
        for row in reader:
            imo, port_id, port_name, country_name, timestamp = row[:5]
            if imo not in voyage_info:
                voyage_info[imo] = []
            voyage_info[imo].append((port_id, port_name, country_name, timestamp))

    with open('voyage_info.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IMO", "Departure Port", "Departure Time", "Departure Country", "Arrival Port", "Arrival Time", "Arrival Country", "Voyage Duration (hours)", "Distance (km)"])
        for imo, ports in voyage_info.items():
            for i in range(len(ports) - 1):
                departure_port, departure_name, departure_country, departure_time = ports[i]
                arrival_port, arrival_name, arrival_country, arrival_time = ports[i + 1]
                # 计算航程时间和距离
                voyage_duration, distance = calculate_voyage_info(departure_time, arrival_time, departure_port, arrival_port)
                writer.writerow([imo, departure_name, departure_time, departure_country, arrival_name, arrival_time, arrival_country, voyage_duration, distance])

# Step 3: 计算港口连通性
def calculate_port_connectivity():
    port_connectivity = defaultdict(set)
    with open('voyage_info.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳过表头
        for row in reader:
            _, departure_port, _, _, arrival_port, _, arrival_country, _, _ = row
            port_connectivity[departure_port].add(arrival_country)

    with open('port_connectivity.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Port ID", "Port Name", "Port Country", "Connected Countries"])
        for departure_port, connected_countries in port_connectivity.items():
            writer.writerow([departure_port, '', '', len(connected_countries)])

# 计算航程时间和距离
def calculate_voyage_info(departure_time, arrival_time, departure_port, arrival_port):
    timestamp_format = "%Y-%m-%d %H:%M:%S"
    departure_time = datetime.strptime(departure_time, timestamp_format)
    arrival_time = datetime.strptime(arrival_time, timestamp_format)
    voyage_duration = (arrival_time - departure_time).total_seconds() / 3600  # 转换为小时

    departure_coords = get_coordinates(departure_port)
    arrival_coords = get_coordinates(arrival_port)
    distance = geodesic(departure_coords, arrival_coords).kilometers

    return voyage_duration, distance

# 获取港口的地理坐标 (使用合适的坐标数据)
def get_coordinates(port_id):
    # 实现根据港口id获取坐标的逻辑
    # 返回格式为 (latitude, longitude)
    pass

# 主程序
if __name__ == "__main__":
    calculate_port_visits()
    generate_voyage_info()
    calculate_port_connectivity()
