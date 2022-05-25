import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import string
from aco import aco

def generate_nodes(n_nodes):
    letters = string.ascii_uppercase
    nodes = []
    for i in range(len(letters)):
        if len(nodes) == n_nodes:
            break
        for j in range(int(n_nodes/len(letters)) + 1):
                name = letters[i] + str(j)
                nodes.append(name)
                if len(nodes) == n_nodes:
                    break
    return nodes

def generate_graph(n_nodes,max_degree):
    nodes = generate_nodes(n_nodes)
    degrees = np.random.randint(1,max_degree,size=n_nodes)
    edges_list = []
    neighbors = {}
    for i in range(n_nodes):
        new_nodes = nodes.copy()
        new_nodes.remove(nodes[i])  
        for node in new_nodes:
            if node in neighbors.keys() and nodes[i] in neighbors[node]:
                new_nodes.remove(node)
        node_neighbors = np.random.choice(new_nodes,size=degrees[i],replace=False).tolist()
        neighbors[nodes[i]] = node_neighbors
        distances = np.random.randint(1,10,size=degrees[i])
        for n,d in zip(node_neighbors,distances):
            edges_list.append((nodes[i],n,d))

    # edges_list = [('A0', 'H0', 3), ('B0', 'F0', 3), ('C0', 'D0', 6), ('D0', 'I0', 2), ('E0', 'H0', 4), ('F0', 'G0', 6), ('G0', 'H0', 3), ('H0', 'B0', 6), ('I0', 'B0', 3), ('J0', 'A0', 8)]
    G = nx.Graph()
    G.add_weighted_edges_from(edges_list)
    return G

if __name__ == "__main__":
    n_nodes = 1000
    max_degree = 8
    G = generate_graph(n_nodes, max_degree)
    nodes = list(G.nodes)
    start, end = nodes[0],nodes[1]
    print('Source:{0}, Destination:{1}'.format(start,end))

    try:
        swarm = aco.antcolony(G, alpha=1,beta=1, start=start,end=end)
        swarm.run(number_of_ants=100,times=10)
        founded_path = []
        for a in swarm.colony:
            if end in a.route.keys():
                # print(a.route,a.L)
                founded_path.append((a.L,a.route))
        print('Shortest Path: {0}\nPath Length:{1}'.format(min(founded_path)[1],min(founded_path)[0]))
    except Exception as e:
        print("---------------------------------------------------------------")
    nx.draw(G, pos=nx.spring_layout(G),with_labels=True)
    plt.show()