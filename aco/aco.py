import numpy as np
import networkx as nx


class ant:  
    def __init__(self, name, G, alpha=1, beta=1, start='S', end='D'):
        self.name = name
        self.G = G
        self.alpha = alpha
        self.beta = beta
        self.current_city = start
        self.target_city = end
        self.route = {self.current_city:0}
        self.L = 0
    
    def move(self):
        if self.current_city == self.target_city : return
        possible_edges = [e for e in self.G.edges([self.current_city]) if e[1] not in self.route]
        possible_cities = [e[1] for e in possible_edges]
        if len(possible_edges)==0: return
        distances = np.array([self.G.edges[e]['weight'] for e in possible_edges])
        pheromones = np.array([self.G.edges[e]['pheromone'] for e in possible_edges])

        preferences = pheromones**self.alpha/distances**self.beta
        probabilites = preferences/preferences.sum()
        new_city = np.random.choice(a= possible_cities, size=1, p=probabilites)[0]
        self.L += self.G.edges[(self.current_city, new_city)]['weight']
        self.current_city = new_city
        self.route[self.current_city] = len(self.route)
    
    def go(self):
        for i in range(self.G.number_of_nodes()):
            self.move()
    
    def get_path(self):
        inv_route = {v:k for k,v in self.route.items()}
        return [inv_route[i] for i in range(len(inv_route))]

class antcolony:
    def __init__(self, G, alpha=1, beta=1, start='S', end='D'):
        self.G = G
        self.alpha = alpha
        self.beta = beta
        self.start = start
        self.end = end
        eps = 0.0001
        nx.set_edge_attributes(self.G, eps, 'pheromone')
    
    def evaporation(self, decay=0.05):
        phe = nx.get_edge_attributes(self.G,'pheromone')
        new_phe = {k:v * (1-decay) for k,v in phe.items()}
        nx.set_edge_attributes(self.G, new_phe, 'pheromone')

    def deposit(self, route, L, delta=1):
        for i,j in zip(route[:-1],route[1:]):
            self.G.edges[(i,j)]['pheromone'] += delta/L

    def run(self, number_of_ants=10, times=2):
        for i in range(times):
            self.colony = [ant(k,self.G, self.alpha, self.beta, self.start, self.end) for k in range(number_of_ants)]
            for k in range(number_of_ants): self.colony[k].go()
            for k in range(number_of_ants): 
                self.deposit(route=self.colony[k].get_path(),L=self.colony[k].L)
            self.evaporation()

