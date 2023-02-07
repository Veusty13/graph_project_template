from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import GraphTraversalSource, __
from gremlin_python.process.traversal import (
    Barrier,
    Bindings,
    Cardinality,
    Column,
    Direction,
    Operator,
    Order,
    P,
    Pop,
    Scope,
    T,
    WithOptions,
)
from typing import Optional
from gremlin_python.process.anonymous_traversal import traversal


def generate_graph():
    # set the graph traversal from the local machine:
    connection = DriverRemoteConnection(
        "ws://localhost:8182/gremlin", "g"
    )  # Connect it to your local server
    g = traversal().withRemote(connection)

    def add_edge(
        g: GraphTraversalSource,
        from_id: int,
        to_id: int,
        edge_label: str,
        param: Optional[str] = None,
    ):
        g.V(from_id).addE(edge_label).to(__.V(to_id)).property("param", param).next()

    def add_vertex(
        g: GraphTraversalSource,
        vertex_label: str,
        vertex_id: int,
        name: Optional[str] = None,
    ):
        g.addV(vertex_label).property(T.id, vertex_id).property("name", name).next()

    def init_toy_graph(g: GraphTraversalSource):
        g.V().drop().iterate()  # so you can run this cell more than ones
        g.E().drop().iterate()  # so you can run this cell more than ones
        add_vertex(g, "user", 1, name="Olivia")
        add_vertex(g, "user", 2, name="Emma")
        add_vertex(g, "file", 3, name="your_new_idea.pdf")
        add_vertex(g, "file", 4, name="salary.pdf")
        add_vertex(g, "file", 5, name="demo.py")
        add_vertex(g, "file", 6, name="blog.html")
        add_vertex(g, "drive", 7, name="my_drive")
        add_vertex(g, "user", 8, name="Steve")
        add_edge(g, 1, 2, "edit")
        add_edge(g, 1, 3, "edit")
        add_edge(g, 1, 4, "view")
        add_edge(g, 2, 5, "print")
        add_edge(g, 2, 6, "edit")
        add_edge(g, 3, 7, "located_in")
        add_edge(g, 8, 5, "print")

    init_toy_graph(g)
    # count how many
    print(g.V().valueMap(True).toList())  # get a list of all of the vertices
    print(g.E().valueMap(True).toList())  # get a list of all of the edges


if __name__ == "__main__":
    generate_graph()
