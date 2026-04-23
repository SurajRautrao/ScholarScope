import networkx as nx
from pyvis.network import Network
import uuid
import os


def build_citation_graph(papers, fetch_references_fn, max_refs=10):
    G = nx.DiGraph()

    for paper in papers:
        main_title = paper["title"]

        #  Mark main nodes
        G.add_node(
            main_title,
            size=30,
            color="red",
            title=main_title
        )

        try:
            references = fetch_references_fn(main_title)[:max_refs]
            print(f"[DEBUG] {main_title} -> {len(references)} references")
        except Exception as e:
            print(f"[ERROR] Failed to fetch references for {main_title}: {e}")
            references = []
        print("REFERENCES:", references)

        for ref in references:
            ref_title = ref.get("title", "Unknown Paper")

            if not ref_title:
                continue

            G.add_node(
                ref_title,
                size=10,
                color="lightblue",
                title=ref_title
            )

            G.add_edge(main_title, ref_title)

    return G


def plot_graph(graph):
    unique_id = str(uuid.uuid4())[:8]
    #path = f"citation_graph_{unique_id}.html"
    output_dir = os.path.join(os.getcwd(), "graphs")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"citation_graph_{unique_id}.html")

    net = Network(
        height="650px",
        width="100%",
        bgcolor="#f0f2f8",   # dark modern bg
        font_color="white",
        directed=True,
        cdn_resources="in_line"
    )

    #  Enable physics (CRITICAL)
    net.barnes_hut()

    # Add nodes with styling
    for node, data in graph.nodes(data=True):
        net.add_node(
            node,
            label=node[:40],
            title=data.get("title", node),
            color=data.get("color", "#97c2fc"),
            size=data.get("size", 10)
        )

    # Add edges
    for source, target in graph.edges():
        net.add_edge(source, target)

    #  Better layout options
    net.set_options("""
    var options = {
      "nodes": {
        "font": {"size": 14}
      },
      "edges": {
        "color": {"inherit": true},
        "smooth": false
      },
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -3000,
          "springLength": 200
        }
      }
    }
    """)

    #path = "citation_graph.html"

    net.save_graph(path)
    print("GRAPH SAVED AT:", path)

    return path


