from gremlin_python.process.graph_traversal import GraphTraversalSource
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T
from gremlin_python.process.anonymous_traversal import traversal
from utils.logger import LOG
from utils.types import (
    Transaction,
    EdgeType,
    VertexType,
    TransactionVertexInformation,
    TransactionEdgeInformation,
)


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
        edge_type: EdgeType,
        edge_information: TransactionEdgeInformation,
        vertex_id_from: int,
        vertex_id_to: int,
    ):
        edge_id = edge_information["id"]
        try:
            existing_edge = (
                self.g.V()
                .has(T.id, vertex_id_from)
                .outE(edge_type.value)
                .has(T.id, edge_id)
                .as_("e")
                .inV()
                .has(T.id, vertex_id_to)
                .select("e")
                .next()
            )
            # LOG.info(
            #     f"existing edge with label {edge_type.value} and id {edge_id} between {vertex_id_from} and {vertex_id_to} : {existing_edge}"
            # )
        except Exception:

            # LOG.info(
            #     f"no existing edge with label {edge_type.value} and id {edge_id} between {vertex_id_from} and {vertex_id_to}"
            # )
            self.g.V().has(T.id, vertex_id_from).addE(edge_type.value).property(
                T.id, edge_id
            ).property("step", edge_information["step"]).property(
                "type", edge_information["type"]
            ).property(
                "amount", edge_information["amount"]
            ).property(
                "oldbalanceorg", edge_information["oldbalanceorg"]
            ).property(
                "newbalanceorig", edge_information["newbalanceorig"]
            ).property(
                "oldbalancedest", edge_information["oldbalancedest"]
            ).property(
                "newbalancedest", edge_information["newbalancedest"]
            ).property(
                "isfraud", edge_information["isfraud"]
            ).property(
                "isflaggedfraud", edge_information["isflaggedfraud"]
            ).to(
                __.V().has(T.id, vertex_id_to)
            ).next()

    def add_vertex(self, vertex_type: VertexType, vertex_id: int) -> None:
        try:
            existing_vertex = self.g.V().has(T.id, vertex_id).valueMap().next()
            # LOG.info(f"existing vertex with id {vertex_id} : {existing_vertex}")
        except Exception:
            # LOG.info(f"no existing vertex with id {vertex_id}")
            self.g.addV(vertex_type.value).property(T.id, vertex_id).property(
                "name", vertex_id
            ).next()

    def add_transaction(self, transaction: Transaction) -> None:
        # from transaction split vertices and edge information
        vertex_information: TransactionVertexInformation = {
            k: v
            for k, v in transaction.items()
            if k in TransactionVertexInformation.__annotations__.keys()
        }
        edge_information: TransactionEdgeInformation = {
            k: v
            for k, v in transaction.items()
            if k in TransactionEdgeInformation.__annotations__.keys()
        }
        # add vertices
        vertex_from: str = vertex_information["nameorig"]
        vertex_to: str = vertex_information["namedest"]
        vertex_type: VertexType = VertexType.ACCOUNT
        self.add_vertex(vertex_type=vertex_type, vertex_id=vertex_from)
        self.add_vertex(vertex_type=vertex_type, vertex_id=vertex_to)
        # add edges
        edge_type: EdgeType = EdgeType.TRANSFER
        self.add_edge(
            edge_type=edge_type,
            edge_information=edge_information,
            vertex_id_from=vertex_from,
            vertex_id_to=vertex_to,
        )
