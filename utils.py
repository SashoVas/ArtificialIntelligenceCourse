import networkx as nx
import matplotlib.pyplot as plt
import utils


class Graph:

    def __init__(self, nodes, edges, heuristic=None, start_node=None, end_node=None, is_tree=False):
        self.nodes = nodes
        self.edges = edges
        self.is_tree = is_tree
        self.start_node = start_node
        self.end_node = end_node
        self.heuristic = heuristic

    def show(self, show_weights=True, node_color='skyblue', display_graph_name=True, heuristic_offset=0.1):
        edge_list = []
        for node, successors in self.edges.items():
            for successor, cost in successors:
                if show_weights:
                    edge_list.append((node, successor, {"weight": cost}))
                else:
                    edge_list.append((node, successor))
        # 1. Create a Graph object
        if self.is_tree:
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        # 2. Add nodes
        G.add_nodes_from(self.nodes)

        # 3. Add edges (connections)
        G.add_edges_from(edge_list)

        # 4. Define a layout (positioning of nodes)
        # Common layouts: spring_layout (force-directed), circular_layout, shell_layout

        if self.is_tree:
            pos = hierarchy_pos(G, root=self.start_node)
        else:
            pos = nx.spring_layout(G)

        # 5. Draw the graph
        nx.draw(G, pos, with_labels=True, node_color=node_color,
                node_size=1500, edge_color='k', linewidths=1, font_size=15)

        if self.start_node:
            # Draw the start node in red
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=[self.start_node],
                node_color='red',
                node_size=1500,
            )
        if self.end_node:
            # Draw the end node in green
            nx.draw_networkx_nodes(
                G,
                pos,
                nodelist=[self.end_node],
                node_color='green',
                node_size=1500,
            )
        if self.heuristic:
            # ---- Create shifted positions for heuristic labels ----
            heuristic_pos = {node: (x, y + heuristic_offset)
                             for node, (x, y) in pos.items()}

            # ---- Draw heuristic values above nodes ----
            nx.draw_networkx_labels(
                G,
                heuristic_pos,
                labels={node: f"({self.heuristic[node]})" for node in G.nodes},
                font_size=10,
                font_color='black'
            )
        # ---- Draw edge labels (costs) ----
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # 6. Display the plot
        if display_graph_name:
            plt.title("Graph")
        plt.show()


def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = {root: (xcenter, vert_loc)}
    children = list(G.successors(root))

    if children:
        dx = width / len(children)
        nextx = xcenter - width / 2 - dx / 2

        for child in children:
            nextx += dx
            pos.update(
                hierarchy_pos(
                    G,
                    child,
                    width=dx,
                    vert_gap=vert_gap,
                    vert_loc=vert_loc - vert_gap,
                    xcenter=nextx
                )
            )
    return pos
