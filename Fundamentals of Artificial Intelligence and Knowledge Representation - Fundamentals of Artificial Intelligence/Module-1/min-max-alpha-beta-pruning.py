import matplotlib.pyplot as plt
import networkx as nx

def draw_game_tree():
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Define node positions manually for a balanced tree layout
    # Levels: 0 (Root), 1, 2, 3, 4 (Leaves)
    # y-coordinates
    y_levels = [4, 3, 2, 1, 0]
    
    # x-coordinates
    # 16 leaves, spread from x=0 to x=15
    # Parent x is average of children x
    
    pos = {}
    labels = {}
    node_colors = []
    
    # Level 4 (Leaves) - 16 nodes
    l4_values = [-6, 34, 79, -84, -46, 30, -36, 69, -87, -65, -65, -67, 71, 98, -4, 81]
    # Note: -65 repeated for visualization of visited leaf, -67 and rest are technically there
    
    for i in range(16):
        pos[f'4_{i}'] = (i * 1.5, y_levels[4])
        labels[f'4_{i}'] = str(l4_values[i])

    # Level 3 (MIN) - 8 nodes
    # Structure: 0-1, 2-3, 4-5, 6-7, etc.
    l3_vals = [-6, -84, -46, -36, -87, -65, 0, 0] # 0 for pruned/unvisited
    for i in range(8):
        child_idx = i * 2
        pos[f'3_{i}'] = ((pos[f'4_{child_idx}'][0] + pos[f'4_{child_idx+1}'][0]) / 2, y_levels[3])
        labels[f'3_{i}'] = str(l3_vals[i]) if i < 6 else ""

    # Level 2 (MAX) - 4 nodes
    l2_vals = [-6, -36, -65, 0]
    for i in range(4):
        child_idx = i * 2
        pos[f'2_{i}'] = ((pos[f'3_{child_idx}'][0] + pos[f'3_{child_idx+1}'][0]) / 2, y_levels[2])
        labels[f'2_{i}'] = str(l2_vals[i]) if i < 3 else ""

    # Level 1 (MIN) - 2 nodes
    l1_vals = [-36, -65]
    for i in range(2):
        child_idx = i * 2
        pos[f'1_{i}'] = ((pos[f'2_{child_idx}'][0] + pos[f'2_{child_idx+1}'][0]) / 2, y_levels[1])
        labels[f'1_{i}'] = str(l1_vals[i])

    # Level 0 (Root MAX)
    pos['0_0'] = ((pos['1_0'][0] + pos['1_1'][0]) / 2, y_levels[0])
    labels['0_0'] = "-36"

    # Draw Edges
    # Regular edges
    edges = []
    # 0 -> 1
    edges.append(('0_0', '1_0'))
    edges.append(('0_0', '1_1'))
    # 1 -> 2
    for i in range(2):
        edges.append((f'1_{i}', f'2_{i*2}'))
        edges.append((f'1_{i}', f'2_{i*2+1}'))
    # 2 -> 3
    for i in range(4):
        edges.append((f'2_{i}', f'3_{i*2}'))
        edges.append((f'2_{i}', f'3_{i*2+1}'))
    # 3 -> 4
    for i in range(8):
        edges.append((f'3_{i}', f'4_{i*2}'))
        edges.append((f'3_{i}', f'4_{i*2+1}'))

    # Draw lines
    for u, v in edges:
        color = 'black'
        width = 1.5
        style = 'solid'
        
        # Grey out pruned branches
        # Pruned subtree at Level 2 right side (Node 2_3 and children)
        if v == '2_3' or u == '2_3' or (u.startswith('3') and int(u.split('_')[1]) >= 6):
             color = 'lightgrey'
             style = 'dashed'
        # Pruned leaf -67 (Node 4_11)
        if v == '4_11':
             color = 'lightgrey'
             style = 'dashed'

        plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=color, linewidth=width, linestyle=style, zorder=1)

    # Draw Nodes
    box_props = dict(boxstyle="square,pad=0.4", fc="white", ec="black", lw=1.5)
    leaf_props = dict(boxstyle="square,pad=0.4", fc="#e6ffe6", ec="lime", lw=2) # Green border for leaves like original
    
    for node, (x, y) in pos.items():
        if labels[node] == "": continue # Skip empty pruned nodes labels
        
        props = box_props
        if node.startswith('4'): # Leaves
            props = leaf_props
        
        plt.text(x, y, labels[node], ha='center', va='center', size=10, weight='bold', bbox=props, zorder=2)

    # Draw Cuts (Red double lines)
    # Cut 1: Edge 3_5 -> 4_11 (Leaf -67)
    x1, y1 = pos['3_5']
    x2, y2 = pos['4_11']
    mx, my = (x1+x2)/2, (y1+y2)/2
    plt.text(mx, my, "//", color='red', fontsize=20, ha='center', va='center', weight='bold', rotation=0, zorder=3)
    
    # Cut 2: Edge 1_1 -> 2_3 (Right subtree of L1-Right)
    x1, y1 = pos['1_1']
    x2, y2 = pos['2_3']
    mx, my = (x1+x2)/2, (y1+y2)/2
    plt.text(mx, my, "//", color='red', fontsize=20, ha='center', va='center', weight='bold', rotation=0, zorder=3)

    # Highlight Chosen Move
    x1, y1 = pos['0_0']
    x2, y2 = pos['1_0']
    plt.arrow(x1, y1, (x2-x1)*0.6, (y2-y1)*0.6, color='blue', width=0.15, head_width=0, length_includes_head=True, zorder=0)

    plt.axis('off')
    plt.title("Solved Minimax Tree with Alpha-Beta Pruning", fontsize=16)
    plt.tight_layout()
    plt.show()

draw_game_tree()
