import re

re_tcpdump = re.compile("^(?P<dtime>\S+) (?P<ipv>\S+) (?P<src>\S+) > (?P<dst>\S+): (?P<proto>\S+).*")

def make_cydata(input_data,
                layout="circle",
                input_source=None,
                ignore_port_number=True,
                debug=False):
    """
    input_data:
        a list of tupple like below
            e.g.
            [
            ("C", "B"),
            ("C", "B"),
            ("A", "B"),
            ("C", "A"),
            ("C", "A"),
            ("C", "A"),
            ("B", "A"),
            ("B", "A")
            ]
        or, a list of dict like below:
            e.g.
            [
            { "src":"A", "dst":"B", "proto":"tcp", "sport":4321, "dstport":80 },
            { "src":"A", "dst":"B", "proto":"tcp", "sport":4322, "dstport":80 },
            { "src":"C", "dst":"B", "proto":"udp", "sport":5522, "dstport":53 }
            ]
    layout:
        "grid", "circle", "breadthfirst", "cose"
    input_source:
        None, "tcpdump"
    ignore_port_number:
        default is True

    return: e.g.
        the input is;
            [
            {
                "group": "nodes",
                "data": {
                    "id": "A",
                    "name": "A",
                    "score_dst": 10,
                    "score_src": 1,
                }
            }
            {
                "group": "edges",
                "data": {
                    "id": "A_to_B",
                    "source": "A",
                    "target": "B",
                    "score": .1,
                }
                "classes": "tcp"    # tcp, udp, icmp, ip, other, ipv4, ipv6
            }
            ]
        """
    cy_nodes = []
    cy_edges = []
    total_score = 0
    node_score = {}
    edge_score = {}
    # common function to make a node.
    def make_node(src, dst, proto=None):
        x = node_score.setdefault(src, {"count_src":0, "count_dst":0})
        x["count_src"] += 1
        x = node_score.setdefault(dst, {"count_src":0, "count_dst":0})
        x["count_dst"] += 1
        x = edge_score.setdefault(f"{src}_to_{dst}",
                                {"score":0, "src":src, "dst":dst})
        x["proto"] = proto
        x["score"] += 1
    #
    if input_source is None:
        if not isinstance(input_data, list):
            raise ValueError("ERROR: no input_data found.")
        if isinstance(input_data[0], dict):
            for d in input_data:
                make_node(d["src"], d["dst"], d.get("proto"))
                total_score += 1
        else:
            # list or tuple
            for d in input_data:
                if len(d) == 3:
                    make_node(d[0], d[1], d[2])
                elif len(d) == 2:
                    make_node(d[0], d[1], None)
                else:
                    # ignore
                    if debug:
                        print("IGNORE:", d, file=sys.stderr)
                    continue
                total_score += 1
    elif input_source == "tcpdump":
        for line in input_data:
            r = re_tcpdump.match(line)
            if not r:
                # ignore
                if debug:
                    print("IGNORE:", line, file=sys.stderr)
                continue
            src = r.group("src")
            dst = r.group("dst")
            if ignore_port_number:
                try:
                    src = src[:src.rindex(".")]
                    dst = dst[:dst.rindex(".")]
                except:
                    # just ignore to remove a port number.
                    pass
            make_node(src, dst, r.group("proto"))
            total_score += 1
    else:
        raise ValueError("ERROR: invalid input_source, {}".format(input_source))

    # make edges.
    for k,v in edge_score.items():
        cy_edges.append({
                "group": "edges",
                "data": {
                        "id": k,
                        "source": "{}".format(v["src"]),
                        "target": "{}".format(v["dst"]),
                        "score": round(v["score"]/total_score,5),
                        },
                "classes": "ipv4",
                "proto": v["proto"]
                })

    # make nodes.
    for k,v in node_score.items():
        cy_nodes.append({
                "group": "nodes",
                "data": {
                        "id": k,
                        "name": k,
                        "score_src": round(v["count_src"]/total_score,5),
                        "score": round(v["count_dst"]/total_score,5),
                        }
                })

    #for k,v in sorted(node_score.items(), key=lambda kv: kv[1]["dst"], reverse=True):
    #    print(k,v)
    layout = {
        "name": f"{layout}",
        "idealEdgeLength": 100,
        "nodeOverlap": 20,
        "refresh": 1000,
        "fit": True,
        "padding": 30,
        "randomize": False,
        "componentSpacing": 100,
        "nodeRepulsion": 400000,
        "edgeElasticity": 100,
        "nestingFactor": 5,
        "gravity": 80,
        "numIter": 1000,
        "initialTemp": 200,
        "coolingFactor": 0.95,
        "minTemp": 1.0
      },

    return { "data":cy_nodes + cy_edges, "layout":layout }

if __name__ == "__main__":
    import json
    import sys
    """
    e.g.
        python make_cyelement.py [tuple|dict|test]
    or
        sudo tcpdump -w hoge.dmp -nqti en0
        tcpdump -r hoge.dmp -n | python make_cyelement.py
    """
    if len(sys.argv) == 1:
        """
        e.g.
        """
        cy_data = make_cydata(sys.stdin, input_source="tcpdump")
        print(json.dumps(cy_data))
        exit(0)
    # simple test
    if sys.argv[1] == "tuple":
        cy_data = make_cydata(
            [
            ("C", "B"),
            ("C", "B"),
            ("A", "B"),
            ("C", "A"),
            ("C", "A"),
            ("C", "A"),
            ("B", "A"),
            ("B", "A")
            ]
            )
    elif sys.argv[1] == "dict":
        cy_data = make_cydata(
            [
            { "src":"A", "dst":"B", "proto":"tcp", "sport":4321, "dstport":80 },
            { "src":"A", "dst":"B", "proto":"tcp", "sport":4322, "dstport":80 },
            { "src":"C", "dst":"B", "proto":"udp", "sport":5522, "dstport":53 }
            ]
            )
    elif sys.argv[1] == "test":
        sys.path.insert(0, "../")
        from make_sample_data.network import network_sample
        input_data = network_sample(random_seed=0)
        cy_data = make_cydata(input_data)
    else:
        print("this [tuple|dict|test]")
        exit(1)
    print(json.dumps(cy_data))

"""
# reference
{
  "data": {
    "id": "605755",
    "idInt": 605755,
    "name": "PCNA",
    "score": 0.006769776522008331,
    "query": true,
    "gene": true
  },
  "position": {
    "x": 481.0169597039117,
    "y": 384.8210888234145
  },
  "group": "nodes",
  "removed": false,
  "selected": false,
  "selectable": true,
  "locked": false,
  "grabbed": false,
  "grabbable": true,
  "classes": "fn10273 fn6944 fn9471 fn10569 fn8023 fn6956 fn6935 fn8147 fn6939 fn6936 fn6629 fn7928 fn6947 fn8612 fn6957 fn8786 fn6246 fn9367 fn6945 fn6946 fn10024 fn10022 fn6811 fn9361 fn6279 fn6278 fn8569 fn7641 fn8568 fn6943"
}
"""
