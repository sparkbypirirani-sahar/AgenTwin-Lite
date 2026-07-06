import networkx as nx
import matplotlib.pyplot as plt

# ساخت گراف
G = nx.Graph()

# اضافه کردن نودها (دستگاه‌ها)
devices = ["Router", "Server", "IoT1", "Attacker", "PC1", "Tablet1", "Tablet2"]
for device in devices:
    G.add_node(device, type='device')

# اضافه کردن ارتباطات (یال‌ها) با وزن
edges = [
    ("Router", "Server", 5),
    ("Router", "IoT1", 2),
    ("Router", "Attacker",2),
    ("Router", "PC1", 3),
    ("PC1", "Tablet1", 1),
    ("PC1", "Tablet2", 4)
]
G.add_weighted_edges_from(edges)

# نمایش گراف
pos = nx.spring_layout(G, seed=42)   #  seed=42 فقط برای این است که هر بار گراف یک شکل ثابت نمایش داده شود.
nx.draw(G, pos, 
        with_labels=True, 
        node_color='lightblue', 
        node_size=2200, 
        font_size=9,
        font_weight='bold',
        edge_color='gray')

# نمایش وزن یال‌ها
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Cyber Digital Twin - Network Topology")
plt.axis('off')
plt.show()

# اطلاعات گراف
print("تعداد نودها:", G.number_of_nodes())
print("تعداد یال‌ها:", G.number_of_edges())
print("\nوزن یال‌ها:")
for u, v, w in G.edges(data='weight'):
    print(f"{u} -- {v} : وزن = {w}")