import networkx as nx
import matplotlib.pyplot as plt

def _plot(filename, title, x, y1, y2, \
        xlabel, ylabel, label1, label2):
    plt.clf()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(x, y1, label=label1)
    if len(y2) != 0:
        plt.plot(x, y2, label=label2)
        plt.legend()
    plt.savefig(filename)

def plot_graphs(generations, nvehicle_avgs, distance_avgs, \
        nvehicle_bests, distance_bests, path=""):
    if len(path) != 0:
        path = path + "/"
    # Avarage of Num of Vehicles by Generations
    title = "Avarage of Number of Vehicles by Generations"
    _plot(path+"vehicles_avg.png", title, generations, nvehicle_avgs, [], \
            "Genration", "Avarage of Number of Vehicle", \
            "Vehicles", "")
    # Avarage of Distance by Generations
    title = "Avarage of Distance by Generations"
    _plot(path+"distance_avg.png", title, generations, distance_avgs, [], \
            "Genration", "Avarage of Distance", \
            "Distance", "")
    # Best Num of Vehicles by Generations
    title = "Best Number of Vehicles by Generations"
    _plot(path+"vehicles_best.png", title, generations, nvehicle_bests, [], \
            "Genration", "Best Number of Vehicle", \
            "Vehicles", "")
    # Best Distance by Generations
    title = "Avarage of Distance by Generations"
    _plot(path+"distance_best.png", title, generations, distance_bests, [], \
            "Genration", "Avarage of Distance", \
            "Distance", "")
    # Num of Vehicles (Avarage & Best) by Generations
    title = "Number of Vehicles by Generations"
    _plot(path+"vehicles_avg_best.png", title, generations, nvehicle_avgs, \
            nvehicle_bests, "Genration", "Number of Vehicle", \
            "Avarage of Vehicles", "Best Vehicles")
    # Distance (Avarage & Best) by Generations
    title = "Distance by Generations"
    _plot(path+"distance_avg_best.png", title, generations, distance_avgs, \
            distance_bests, "Genration", "Avarage of Distance", \
            "Avarage of Distance", "Best Distance")

def draw_routings(nodes, solutions, path=""):
    G = nx.Graph()
    depot = nodes.get_depot()
    colors = ['black', 'green', 'cyan', 'magenta', 'red', 'blue']
  
    # Add nodes
    G.add_node(depot.get_id(), pos=depot.get_pos(), color='blue')
    for customer in nodes.get_customers():
        G.add_node(customer.get_id(), pos=customer.get_pos(), color='red')
  
    for (index, solution) in enumerate(solutions):
        edge_list = []
        G.remove_edges_from(list(G.edges()))
        plt.clf()
  
        for route in solution.chromosome:
            edges = []
            edges.append((depot.get_id(), route[0]))
            for i in range(len(route)-1):
                edges.append((route[i], route[i+1]))
            edges.append((route[-1], depot.get_id()))
            edge_list.append(edges)
  
        for edges in edge_list:
            G.add_edges_from(edges)
  
        # Draw Nodes
        positions = {id_: (x, y) for (id_, (x, y)) in nx.get_node_attributes(G, 'pos').items()}
        nx.draw(G, positions, with_labels=True)
        nx.draw_networkx_nodes(G,positions,
                               nodelist=[depot.get_id()],
                               node_color='blue',)
        nx.draw_networkx_nodes(G,positions,
                               nodelist=nodes.get_customers_id_list(),
                               node_color='r',)
        # Draw Edges
        for (i, edges) in enumerate(edge_list):
            nx.draw_networkx_edges(G,positions,
                                   edgelist=edges,
                                   edge_color=colors[i%(len(colors))])
        # Save Figure
        if len(path) != 0:
            path = path + "/"
        plt.savefig(path + "routing" + str(index).zfill(3) + ".png")
