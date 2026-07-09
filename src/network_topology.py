"""
Project: AgenTwin-Lite - Cyber Digital Twin
Stage 5: Multi-Attack Simulation
"""

import networkx as nx
import matplotlib.pyplot as plt
from random import randint, choice
from datetime import datetime

G = nx.Graph()
event_log = []

# ==================== ساخت شبکه ====================
devices = ["Router", "Server", "IoT1", "IoT2", "Laptop", "PC1", "Tablet1", "Tablet2", "PC2"]

for device in devices:
    G.add_node(device, type='device', status='Healthy', load=randint(20, 75), risk=0)

G.add_node("IDS", type='security', status='Active', risk=0)
G.add_node("Attacker", type='device', status='Malicious', risk=90)

# ارتباطات
edges = [
    ("Router", "Server", 5), ("Router", "IoT1", 2), ("Router", "IoT2", 1),
    ("Router", "Laptop", 6), ("Attacker", "Router", 2), ("Router", "PC1", 3),
    ("PC1", "Tablet1", 1), ("PC1", "Tablet2", 4), ("Router", "PC2", 3)
]
ids_connections = [("IDS", "Router", 10), ("IDS", "Server", 8), 
                   ("IDS", "PC1", 7), ("IDS", "Laptop", 6)]

G.add_weighted_edges_from(edges + ids_connections)

# ==================== توابع ====================
def log_event(event_type, description):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {event_type}: {description}"
    event_log.append(entry)
    print(entry)

def isolate_node(target):
    if target in G.nodes:
        G.nodes[target]['status'] = 'Isolated'
        G.nodes[target]['load'] = 0
        log_event("ISOLATION", f"Device {target} has been isolated")
        print(f"🛡️  {target} قرنطینه شد.")

def simulate_attack(G, attacker, target, intensity="Medium"):
    print(f"\n🔴 حمله از {attacker} به {target} | شدت: {intensity}")
    
    # اعمال حمله
    if intensity == "High":
        damage = randint(70, 95)
        new_status = "Compromised"
    elif intensity == "Medium":
        damage = randint(40, 70)
        new_status = "Warning"
    else:
        damage = randint(10, 40)
        new_status = "Warning"

    G.nodes[target]["status"] = new_status
    G.nodes[target]["risk"] = min(100, G.nodes[target].get("risk", 0) + damage)
    G.nodes[target]["load"] = min(100, G.nodes[target].get("load", 0) + randint(15, 30))

    log_event("ATTACK", f"{attacker} attacked {target} ({intensity})")

    # تشخیص IDS و واکنش
    if G.has_edge("IDS", target) or G.has_edge("IDS", "Router"):
        if randint(1, 100) > 25:
            log_event("IDS", f"Attack detected on {target}")
            print("🟢 IDS حمله را تشخیص داد!")
            if G.nodes[target]["risk"] > 60:
                isolate_node(target)
        else:
            log_event("IDS", f"Failed to detect attack on {target}")

# ==================== شبیه‌سازی چندین حمله ====================
def run_multi_attack_scenario(attacks):
    print("🚀 شروع سناریوی چندین حمله...\n")
    for i, (target, intensity) in enumerate(attacks, 1):
        print(f"\n--- حمله شماره {i} ---")
        simulate_attack(G, "Attacker", target, intensity)
        # کمی تأخیر برای realism
        # time.sleep(0.8)
    
    print("\n" + "="*70)
    print("📋 تاریخچه کامل وقایع:")
    for event in event_log:
        print(event)

# ==================== اجرا ====================
def draw_digital_twin(G, title):
    # (همان تابع قبلی نمایش - برای کوتاه شدن کد اینجا نیاوردم)
    # لطفاً تابع draw_digital_twin از کد قبلی را کپی کن
    pass   # فعلاً خالی - بعداً کامل می‌کنیم

# ==================== اجرای سناریو ====================
attacks_list = [
    ("Server", "High"),
    ("PC1", "Medium"),
    ("IoT1", "Low"),
    ("Laptop", "High")
]

draw_digital_twin(G, "Cyber Digital Twin - Initial State")   # قبل از حملات
run_multi_attack_scenario(attacks_list)
draw_digital_twin(G, "Cyber Digital Twin - After Multiple Attacks")   # بعد از حملات