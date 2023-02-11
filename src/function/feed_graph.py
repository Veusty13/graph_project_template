from utils.logger import LOG
from utils.functions.aws import get_message_from_sqs
from utils.functions.db import execute_read_query, build_db_config_string
from config.settings import DB_CONFIG_DICT, GREMLIN_CONFIG_DICT

from resources.queries.get_last_batch import query as get_last_batch_query
import psycopg2
from utils.functions.gremlins import GremlinClient


def lambda_handler(event, context) -> None:
    message = get_message_from_sqs(event=event)
    LOG.info(message)
    pg_connection_config: str = build_db_config_string(DB_CONFIG_DICT)
    conn = psycopg2.connect(pg_connection_config)
    for message_element in message:
        last_batch_id = message_element["last_batch_id"]
        query = get_last_batch_query.format(last_batch_id)
        last_batch_response = execute_read_query(
            query=query,
            connection=conn,
        )
        gremlin_client = GremlinClient(db_config=GREMLIN_CONFIG_DICT)
        gremlin_client.get_traversal()
        # gremlin_client.add_vertex(vertex_type="Person", vertex_id=1, name="Steve")
        # gremlin_client.add_vertex(vertex_type="Person", vertex_id=2, name="Enzo")
        # gremlin_client.add_vertex(vertex_type="Person", vertex_id=3, name="Jimmy")
        # gremlin_client.add_vertex(vertex_type="Person", vertex_id=4, name="Marla")
        # gremlin_client.add_edge(from_id=1, to_id=2, edge_type="friendship", param="0.8")
        # gremlin_client.add_edge(from_id=1, to_id=2, edge_type="colleagues", param="0.8")
        # gremlin_client.add_edge(from_id=2, to_id=1, edge_type="friendship", param="0.8")
        # gremlin_client.add_edge(from_id=2, to_id=3, edge_type="friendship", param="0.8")
        # gremlin_client.add_edge(from_id=2, to_id=4, edge_type="love", param="0.8")
        gremlin_client.close_connection()
