"""
Project: AgenTwin-Lite - Cyber Digital Twin
Stage 3: Advanced Attack Simulation + IDS Detection
"""

import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import time

# ==================== ساخت گراف ====================
# Creating the graph
G = nx.Graph()

# ==================== نودها + ویژگی‌های اولیه ====================
# Nodes + Initial attributes
devices = ["Router", "Server", "IoT1", "IoT2", "Laptop", "PC1", "Tablet1", "Tablet2", "PC2"]

for device in devices:
    G.add_node(device, 
               type='device', 
               status='Healthy',      # Healthy, Warning, Compromised
               load=randint(20, 75),  # Load percentage
               risk=0)                # Risk level 0-100

# اضافه کردن IDS
# Adding IDS
G.add_node("IDS", type='security', status='Active', risk=0)

# اضافه کردن Attacker
# Adding Attacker
G.add_node("Attacker", type='device', status='Malicious', risk=90)

# ==================== ارتباطات ====================
# Network connections
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
# IDS monitoring connections
ids_connections = [
    ("IDS", "Router", 10),
    ("IDS", "Server", 8),
    ("IDS", "PC1", 7),
    ("IDS", "Laptop", 6)
]

G.add_weighted_edges_from(edges + ids_connections)

# ==================== تابع نمایش ====================
# Visualization function
def draw_digital_twin(G, title="Cyber Digital Twin"):
    pos = nx.spring_layout(G, seed=42)

    # رنگ‌بندی بر اساس وضعیت
    # Color coding based on device status
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
    # Display edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title(title)
    plt.axis('off')
    plt.show()

# ==================== تابع شبیه‌سازی حمله ====================
# Attack simulation function
def simulate_attack(G, attacker, target, intensity="Medium"):
    print(f"\n🔴 حمله از {attacker} به {target} شروع شد | شدت: {intensity}")
    print(f"🔴 Attack from {attacker} to {target} started | Intensity: {intensity}")

    # محاسبه آسیب بر اساس شدت حمله
    # Calculate damage based on attack intensity
    if intensity == "High":
        damage = randint(70, 95)
        new_status = "Compromised"
    elif intensity == "Medium":
        damage = randint(40, 70)
        new_status = "Warning"
    else:
        damage = randint(10, 40)
        new_status = "Warning"

    # اعمال حمله روی هدف
    # Apply attack to target
    G.nodes[target]["status"] = new_status
    G.nodes[target]["risk"] = min(100, G.nodes[target]["risk"] + damage)
    G.nodes[target]["load"] = min(100, G.nodes[target]["load"] + randint(15, 30))

    # تشخیص توسط IDS
    # IDS Detection
    detected = False
    if G.has_edge("IDS", target) or G.has_edge("IDS", "Router"):
        if randint(1, 100) > 25:   # 75% detection chance
            detected = True
            G.nodes["IDS"]["status"] = "Alert"
            print(f"🟢 IDS حمله را تشخیص داد و هشدار داد!")
            print(f"🟢 IDS detected the attack and raised alert!")
        else:
            print(f"⚠️  IDS حمله را تشخیص نداد!")
            print(f"⚠️  IDS failed to detect the attack!")
    else:
        print(f"⚠️  IDS حمله را تشخیص نداد!")
        print(f"⚠️  IDS failed to detect the attack!")

    print(f"→ {target} وضعیت: {new_status} | ریسک: {G.nodes[target]['risk']}%")
    print(f"→ {target} Status: {new_status} | Risk: {G.nodes[target]['risk']}%")

    return detected

# ==================== اجرای شبیه‌سازی ====================
# Running the simulation
draw_digital_twin(G, "Cyber Digital Twin - Initial State")
# Initial State Visualization

print("\n" + "="*60)

# اجرای حمله
# Execute attack
simulate_attack(G, "Attacker", "Server", intensity="High")

print("\n" + "="*60)

draw_digital_twin(G, "Cyber Digital Twin - After Attack")
# Visualization After Attack