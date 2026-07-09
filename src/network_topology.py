"""
File: network_state_model.py

Description:
Extends the initial Cyber Digital Twin network topology by introducing
dynamic device states and security attributes.

Compared with the previous version, this implementation adds:
- Device health status modeling (Healthy, Warning, Compromised)
- Resource utilization/load estimation for network devices
- Risk level assignment for cybersecurity analysis
- IDS and attacker entities with specific security roles
- A state-aware visualization mechanism based on device conditions

This version represents the first step toward a dynamic Cyber Digital Twin,
where network entities are modeled not only by their connections but also
by their operational and security states.

Author: Sahar Pier
Project: AgenTwin-Lite
"""
import networkx as nx
import matplotlib.pyplot as plt
from random import choice

# ==================== ساخت گراف ====================
G = nx.Graph()

# نودها + ویژگی‌های اولیه
devices = ["Router", "Server", "IoT1", "IoT2", "Laptop", "PC1", "Tablet1", "Tablet2", "PC2"]

for device in devices:
    G.add_node(device, 
               type='device',
               status='Healthy',      # Healthy, Warning, Compromised
               load=choice([30, 45, 60, 75]),  # هر بار اجرا به صورت رندوم یک عدد می دهد choice  درصد بار درصد استفاده از منابع دستگاه را نشان می‌دهد.
               risk=0)                # سطح ریسک 0-100

G.add_node("IDS", type='security', status='Active', risk=0)
G.add_node("Attacker", type='device', status='Malicious', risk=85)

# ==================== ارتباطات ====================
edges = [
    ("Router", "Server", 5), ("Router", "IoT1", 2), ("Router", "IoT2", 1),
    ("Router", "Laptop", 6), ("Attacker", "Router", 2), ("Router", "PC1", 3),
    ("PC1", "Tablet1", 1), ("PC1", "Tablet2", 4), ("Router", "PC2", 3),
]

ids_connections = [("IDS", "Router", 10), ("IDS", "Server", 8), 
                   ("IDS", "PC1", 7), ("IDS", "Laptop", 6)]

G.add_weighted_edges_from(edges + ids_connections)

# ==================== تابع نمایش ====================
def draw_digital_twin(G, title="Cyber Digital Twin"):
    pos = nx.spring_layout(G, seed=42)
    
    # رنگ‌بندی بر اساس وضعیت
    color_map = []
    for node in G.nodes():
        status = G.nodes[node].get('status')
        if status == 'Compromised':
            color_map.append('darkred')
        elif status == 'Warning':
            color_map.append('orange')
        elif status == 'Malicious':
            color_map.append('purple')
        elif node == 'IDS':
            color_map.append('red')
        else:
            color_map.append('lightblue')
    
    nx.draw(G, pos, with_labels=True, node_color=color_map, 
            node_size=2200, font_size=9, font_weight='bold', edge_color='gray')
    
    # نمایش وزن یال‌ها
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title(title)
    plt.axis('off')
    plt.show()

# نمایش اولیه
draw_digital_twin(G, "Cyber Digital Twin - Initial State")