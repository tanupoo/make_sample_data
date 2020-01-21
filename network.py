import random

def network_sample(node_profile=None,
                   random_seed=None):
    """
    node_profile:
        a set of { node_name : nb_edge }
        default is:
            { "A":10, "B":4, "C":3, "D":1, ..., "Z":1 }
    return:
        In the default profile, "A" has 10 edges from the differnt nodes.
    """
    if random_seed is not None:
        random.seed(random_seed)
    #
    if node_profile is None:
        node_profile = {}
        node_list = [chr(_) for _ in range(ord("A"), ord("Z")+1)]
        weight_list = [ 10, 5, 3 ] + [1 for _ in range(len(node_list)-3)]
        for a,b in zip(node_list, weight_list):
            node_profile.update({a:b})
    #
    sample = []
    node_list = node_profile.keys()
    for n, w in sorted(node_profile.items(), key=lambda kv:kv[1]):
        peers = list(node_list).copy()
        peers.remove(n)
        for i in range(w):
            sample.append((random.choice(peers), n))
    #
    return sample

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import networkx as nx
    def show_result(edges):
        G = nx.DiGraph()
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)
        plt.show()
    #
    result = network_sample({"A":5, "B":3, "C":-1})
    for i in result:
        print(i)
    show_result(result)
    show_result(network_sample(random_seed=0))
