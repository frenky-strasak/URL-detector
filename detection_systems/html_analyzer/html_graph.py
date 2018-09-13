"""
Get structure of html. At the end we have set of edges in graph.
"""


import networkx as nx
from lxml import html
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
import urllib.request


# print(html)
# raw = html_output


def download_html() -> str:
    urlib_instant = urllib.request.urlopen('http://' + 'www.seznam.cz', timeout=5)
    html_output = urlib_instant.read().decode('utf-8')
    return html_output

    # with open('test_html.html') as f:
    #     html_output = f.read()
    # return html_output


def build_graph(html_output: str):
    raw = html_output

    def traverse(parent, graph, labels):
        labels[parent] = parent.tag
        for node in parent.getchildren():
            graph.add_edge(parent, node)
            traverse(node, graph, labels)

    G = nx.DiGraph()
    labels = {}  # needed to map from node to tag
    # html_tag = html.document_fromstring(raw)
    html_tag = html.fromstring(raw)


    # print(html_tag.tag)
    # print(html_tag.name)
    traverse(html_tag, G, labels)

    for edge in G.edges:
        a, b = edge
        print('{} {}'.format(a.tag, b.tag))

    print('------------------------- nodes: {}'.format(len(G.nodes)))
    for node in G.nodes:
        # print(labels[node])
        print(node.tag)


def main():
    html_output = download_html()
    build_graph(html_output)


if __name__ == '__main__':
    main()
