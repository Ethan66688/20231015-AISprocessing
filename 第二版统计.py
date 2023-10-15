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
    voyage_info = defaultdict(list)
    with open('ship_port_visits.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        next(reader)  # 跳过表头
        previous_imo = None
        previous_port = None
        previous_time = None
        for row in reader:
            imo, port_id, port_name, country_name, timestamp = row[:5]
            if imo != previous_imo:
                previous_imo = imo
                previous_port = port_id
                previous_time = timestamp
            else:
                departure_port = previous_port
                departure_time = previous_time
                arrival_port = port_id
                arrival_time = timestamp
                voyage_info[imo].append((departure_port, departure_time, arrival_port, arrival_time))
                previous_port = port_id
                previous_time = timestamp

    with open('voyage_info.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IMO", "Departure Port", "Departure Time", "Arrival Port", "Arrival Time"])
        for imo, voyages in voyage_info.items():
            for voyage in voyages:
                departure_port, departure_time, arrival_port, arrival_time = voyage
                writer.writerow([imo, departure_port, departure_time, arrival_port, arrival_time])

# Step 3: 计算港口连通性
def calculate_port_connectivity():
    port_connectivity = defaultdict(set)
    with open('voyage_info.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 跳过表头
        for row in reader:
            _, departure_port, _, arrival_port, _ = row
            port_connectivity[departure_port].add(arrival_port)

    with open('port_connectivity.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Port ID", "Connected Ports"])
        for departure_port, connected_ports in port_connectivity.items():
            writer.writerow([departure_port, ', '.join(connected_ports)])

# 主程序
if __name__ == "__main__":
    calculate_port_visits()
    generate_voyage_info()
    calculate_port_connectivity()
