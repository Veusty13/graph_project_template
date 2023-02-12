from utils.logger import LOG
from utils.functions.aws import get_message_from_sqs
from utils.functions.db import execute_read_query, build_db_config_string
from config.settings import DB_CONFIG_DICT, GREMLIN_CONFIG_DICT

from utils.queries.get_last_batch import query as get_last_batch_query
import psycopg2
from utils.functions.gremlins import GremlinClient
from utils.types import Transaction
from typing import List


def lambda_handler(event, context) -> None:
    message = get_message_from_sqs(event=event)
    LOG.info(message)
    pg_connection_config: str = build_db_config_string(DB_CONFIG_DICT)
    conn = psycopg2.connect(pg_connection_config)
    for message_element in message:
        last_batch_id = message_element["last_batch_id"]
        query = get_last_batch_query.format(last_batch_id)
        transactions: List[Transaction] = execute_read_query(
            query=query,
            connection=conn,
        )
        gremlin_client = GremlinClient(db_config=GREMLIN_CONFIG_DICT)
        gremlin_client.get_traversal()
        for transaction in transactions:
            gremlin_client.add_transaction(transaction)
        gremlin_client.close_connection()
