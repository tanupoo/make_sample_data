import random

def scatter_sample(dim_range,
                   nb_points,
                   nb_clusters,
                   ret_type="scatter",
                   cluster_sizes=None,
                   jitters=None,
                   random_seed=None,
                   debug=False):
    """
    dim_range: a list of the range of each dimension.
        e.g. [(s0_min,s0_max), (s1_min,s1_max), ...]
        i.e. the number of dimensions is len(dim_range)
    ret_type: return type.
        "scatter":
            the form of return value is like:
                [ [i00, j00], [i10, j10], ..., [i90, j91], ... ]
            the number of items is equal to nb_points.
            the form of each item is equal to dim_range.
        "linear":
            the form of return value is like:
                [ [i00, i10, ..., i90], [j01, j11, ..., j91], ... ]
            the number of items is equal to the number of dimensions.
    cluster_sizes: a list of the size of each dimension for a cluster.
        it is only used to determine the jitters.
    jitters: a list of the jitter of each dimension.
        e.g. [0.1, 0.02, ...]
        if jitters is specified, cluster_sizes will be ignored.
    """
    if random_seed is not None:
        random.seed(random_seed)
    #
    if ret_type not in ["scatter","linear"]:
        raise ValueError('ret_type must be "scatter" or "linear".')
    #
    if cluster_sizes is None:
        cluster_sizes = []
        for s_min, s_max in dim_range:
            cluster_sizes.append(random.uniform(0.5,1.5)*(s_max-s_min)/nb_clusters)
        if debug:
            print("cluster_sizes=", cluster_sizes)
    #
    if jitters is None:
        jitters = []
        for i in range(len(dim_range)):
            jitters.append(cluster_sizes[i]*0.2)
        if debug:
            print("jitters=", jitters)
    #
    cluster_pos = []
    for cn in range(nb_clusters):
        p = []
        for i, (s_min, s_max) in enumerate(dim_range):
            p.append(random.uniform(s_min+jitters[i],s_max-jitters[i]))
        cluster_pos.append(p)
    #
    sample = []
    if ret_type == "scatter":
        for n in range(nb_points):
            c = random.choice(cluster_pos)
            p = []
            for i, d in enumerate(c):
                p.append(random.gauss(d,jitters[i]))
            sample.append(p)
    elif ret_type == "linear":
        for i in range(len(dim_range)):
            sample.append([])
        for n in range(nb_points):
            pos = random.choice(cluster_pos)
            for i, d in enumerate(pos):
                sample[i].append(random.gauss(d,jitters[i]))
    else:
        raise "XXX should not be reached."
    #
    return sample

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    #
    # the form of n is [ [i0, j0], [i1, j1], ..., [i9, j9] ]
    n = scatter_sample([(0,10),(0,10)], 10, 4, ret_type="scatter",
                       random_seed=0)
    #
    # the form of n is [ [i0, i1, ..., i9], [j0, j1, ..., j9] ]
    n = scatter_sample([(0,10),(0,10)], 100, 4, ret_type="linear",
                       random_seed=1)
    fig = plt.figure()
    plt.plot(n[0], n[1], "o")
    plt.show()
    #
    n = scatter_sample([(0,10),(0,10)], 1000, 10, ret_type="linear",
                       jitters=(0.4,0.4),
                       random_seed=2, debug=True)
    fig = plt.figure()
    plt.plot(n[0], n[1], "o")
    plt.show()
