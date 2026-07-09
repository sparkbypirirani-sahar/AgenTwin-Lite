"""
File: network_state_attack_simulation.py

Description:
This file extends the Cyber Digital Twin model by adding dynamic state
changes caused by cybersecurity events.

Previous version:
- Created a static network topology.
- Added device attributes such as status, load, and risk.

Current version:
- Introduces an attack simulation mechanism.
- Allows an attacker node to affect a target device.
- Updates the target device security state after an attack.
- Increases the risk level based on the simulated event.
- Visualizes the Digital Twin before and after the attack.

Main components:
1. Network creation:
   - Defines physical and security entities as graph nodes.
   - Creates communication links with weighted edges.

2. Device state modeling:
   - Each device contains operational and security attributes:
     status, resource load, and risk level.

3. Attack simulation:
   - Simulates a cyber event between attacker and target nodes.
   - Updates the Digital Twin state after the event.

4. Visualization:
   - Displays network topology.
   - Uses different colors to represent device security conditions.

This version represents the transition from a static Cyber Digital Twin
to a dynamic Digital Twin capable of reflecting security events.

Project: AgenTwin-Lite
Author: Sahar Pier
"""

import networkx as nx
import matplotlib.pyplot as plt
from random import choice


# ==================== ساخت گراف ====================
G = nx.Graph()


# ==================== نودها + ویژگی‌های اولیه ====================
devices = [
    "Router",
    "Server",
    "IoT1",
    "IoT2",
    "Laptop",
    "PC1",
    "Tablet1",
    "Tablet2",
    "PC2"
]


for device in devices:
    G.add_node(
        device,
        type='device',
        status='Healthy',      # Healthy, Warning, Compromised
        load=choice([30, 45, 60, 75]),  # درصد بار
        risk=0                # سطح ریسک 0-100
    )


# اضافه کردن IDS
G.add_node(
    "IDS",
    type='security',
    status='Active',
    risk=0
)


# اضافه کردن Attacker
G.add_node(
    "Attacker",
    type='device',
    status='Malicious',
    risk=85
)



# ==================== ارتباطات ====================
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


# ارتباطات IDS
ids_connections = [
    ("IDS", "Router", 10),
    ("IDS", "Server", 8),
    ("IDS", "PC1", 7),
    ("IDS", "Laptop", 6)
]


G.add_weighted_edges_from(edges + ids_connections)



# ==================== تابع شبیه سازی حمله ====================
def simulate_attack(G, attacker, target):

    print(f"{attacker} attacks {target}")

    # تغییر وضعیت قربانی
    G.nodes[target]["status"] = "Warning"

    # افزایش ریسک
    G.nodes[target]["risk"] = 60

    print(
        f"{target} status changed to:",
        G.nodes[target]["status"]
    )

    print(
        f"{target} risk level:",
        G.nodes[target]["risk"]
    )



# ==================== تابع نمایش Digital Twin ====================
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



    # رسم گراف
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=color_map,
        node_size=2200,
        font_size=9,
        font_weight='bold',
        edge_color='gray'
    )


    # نمایش وزن یال‌ها
    edge_labels = nx.get_edge_attributes(
        G,
        'weight'
    )


    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=8
    )


    plt.title(title)

    plt.axis('off')

    plt.show()



# ==================== اجرای Digital Twin ====================

# وضعیت اولیه
draw_digital_twin(
    G,
    "Cyber Digital Twin - Initial State"
)


print("\nBefore Attack:")
print(G.nodes["Router"])



# اجرای حمله
simulate_attack(
    G,
    "Attacker",
    "Router"
)



print("\nAfter Attack:")
print(G.nodes["Router"])



# وضعیت بعد از حمله
draw_digital_twin(
    G,
    "Cyber Digital Twin - After Attack"
)