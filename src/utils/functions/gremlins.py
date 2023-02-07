from gremlin_python.process.graph_traversal import GraphTraversalSource
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal


class GremlinClient:
    def __init__(self, db_config: dict) -> None:
        self.db_config = db_config

    def build_gremlin_config_dict(self) -> None:
        protocol = self.db_config["protocol"]
        host = self.db_config["host"]
        port = self.db_config["port"]
        service = self.db_config["service"]
        traversal_source = self.db_config["traversal_source"]
        url = f"{protocol}://{host}:{port}/{service}"
        self.config_dict = {"url": url, "traversal_source": traversal_source}

    def get_traversal(self) -> None:
        connection = DriverRemoteConnection(**self.config_dict)
        self.g = traversal().withRemote(connection)
        # reset traversal source
        self.g.V().drop().iterate()
        self.g.E().drop().iterate()

    def add_egde(self) -> None:
        pass

    def add_node(self) -> None:
        pass
