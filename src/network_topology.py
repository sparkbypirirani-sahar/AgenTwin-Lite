"""
File: network_topology.py

Description:
Creates the initial Cyber Digital Twin network topology using NetworkX.
The network includes standard devices, an attacker node, and an IDS node.
Weighted edges represent communication links and monitoring connections.
The graph is visualized, and basic topology statistics are displayed.

Author: Sahar Pier
Project: AgenTwin-Lite
"""

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# ==================== نودها ====================
devices = ["Router", "Server", "IoT1", "IoT2", "Laptop", "Attacker", 
           "PC1", "Tablet1", "Tablet2", "PC2"]

for device in devices:
    G.add_node(device, type='device')

# اضافه کردن IDS
G.add_node("IDS", type='security')

# ==================== یال‌ها ====================
edges = [
    ("Router", "Server", 5),
    ("Router", "IoT1", 2),
    ("Router", "IoT2", 1),
    ("Router", "Laptop", 6),
    ("Attacker", "Router", 2),
    ("Router", "PC1", 3),
    ("PC1", "Tablet1", 1),
    ("PC1", "Tablet2", 4),
    ("Router", "PC2", 3),
]

G.add_weighted_edges_from(edges)

# اتصال IDS به دستگاه‌های مهم (نظارت)
ids_connections = [
    ("IDS", "Router", 10),      # IDS مستقیم به روتر وصل است
    ("IDS", "Server", 8),
    ("IDS", "PC1", 7),
    ("IDS", "Laptop", 6),
]

G.add_weighted_edges_from(ids_connections)

# ==================== نمایش ====================
pos = nx.spring_layout(G, seed=42)

# رنگ‌بندی متفاوت
color_map = []
for node in G.nodes():
    if node == "IDS":
        color_map.append('red')
    elif node == "Attacker":
        color_map.append('darkred')
    else:
        color_map.append('lightblue')

nx.draw(G, pos, 
        with_labels=True, 
        node_color=color_map, 
        node_size=2200, 
        font_size=9,
        font_weight='bold',
        edge_color='gray')

# نمایش وزن‌ها
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Cyber Digital Twin - Network Topology + IDS")
plt.axis('off')
plt.show()

# اطلاعات
print("تعداد نودها:", G.number_of_nodes())
print("تعداد یال‌ها:", G.number_of_edges())
print("\nIDS به چه دستگاه‌هایی متصل است؟")
for neighbor in G.neighbors("IDS"):
    weight = G.edges[("IDS", neighbor)]['weight']
    print(f"→ {neighbor} (وزن ارتباط: {weight})")