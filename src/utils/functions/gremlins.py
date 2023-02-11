from gremlin_python.process.graph_traversal import GraphTraversalSource
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T
from gremlin_python.process.anonymous_traversal import traversal
from typing import Optional
from utils.logger import LOG


class GremlinClient:
    def __init__(self, db_config: dict) -> None:
        self.db_config = db_config
        self.build_gremlin_config_dict()

    def build_gremlin_config_dict(self) -> None:
        protocol = self.db_config["protocol"]
        host = self.db_config["host"]
        port = self.db_config["port"]
        service = self.db_config["service"]
        traversal_source = self.db_config["traversal_source"]
        url = f"{protocol}://{host}:{port}/{service}"
        self.config_dict = {"url": url, "traversal_source": traversal_source}

    def get_traversal(self) -> None:
        self.connection = DriverRemoteConnection(**self.config_dict)
        self.g: GraphTraversalSource = traversal().withRemote(self.connection)

    def clear_graph(self) -> None:
        self.g.V().drop().iterate()
        self.g.E().drop().iterate()

    def close_connection(self) -> None:
        self.connection.close()

    def add_edge(
        self,
        from_id: int,
        to_id: int,
        edge_type: str,
        param: Optional[str] = None,
    ):
        try:
            existing_edge = (
                self.g.V()
                .has(T.id, from_id)
                .outE(edge_type)
                .as_("e")
                .inV()
                .has(T.id, to_id)
                .select("e")
                .next()
            )
            LOG.info(
                f"existing edge with label {edge_type} between {from_id} and {to_id} : {existing_edge}"
            )
        except Exception:
            LOG.info(
                f"no existing edge with label {edge_type} between {from_id} and {to_id}"
            )
            self.g.V().has(T.id, from_id).addE(edge_type).property("param", param).to(
                __.V().has(T.id, to_id)
            ).next()

    def add_vertex(
        self,
        vertex_type: str,
        vertex_id: int,
        name: Optional[str] = None,
    ):
        try:
            existing_vertex = self.g.V().has(T.id, vertex_id).valueMap().next()
            LOG.info(f"existing vertex with id {vertex_id} : {existing_vertex}")
        except Exception:
            LOG.info(f"no existing vertex with id {vertex_id}")
            self.g.addV(vertex_type).property(T.id, vertex_id).property(
                "name", name
            ).next()
