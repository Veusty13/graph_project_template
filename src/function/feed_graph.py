from utils.logger import LOG
from utils.functions.aws import get_message_from_sqs
from utils.functions.db import execute_read_query, build_db_config_string
from config.settings import DB_CONFIG_DICT
import psycopg2


def lambda_handler(event, context) -> None:
    message = get_message_from_sqs(event=event)
    LOG.info(message)
    connection_config: str = build_db_config_string(DB_CONFIG_DICT)
    connection = psycopg2.connect(connection_config)
    for message_element in message:
        last_batch_id = message_element["last_batch_id"]
        last_rows = execute_read_query(
            query=f"select * from transactions where batch_id = {last_batch_id};",
            connection=connection,
        )
