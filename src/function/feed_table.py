from utils.logger import LOG
import pandas as pd
from utils.functions.aws import (
    get_s3_path_from_event,
    get_s3_object_body_from_path,
    delete_s3_object,
    send_sqs_message,
)
from utils.functions.db import (
    build_db_config_string,
    insert_data_from_buffer,
    execute_read_query,
)
from config.settings import DB_CONFIG_DICT, SQS_QUEUE_URL_FEED_GRAPH
import psycopg2


def lambda_handler(event, context) -> None:

    s3_paths = get_s3_path_from_event(event)
    count_paths = len(s3_paths)
    LOG.info(f"retrieved {count_paths} file(s) with data to insert to table")
    connection_config: str = build_db_config_string(DB_CONFIG_DICT)
    connection = psycopg2.connect(connection_config)

    for s3_path in s3_paths:
        body = get_s3_object_body_from_path(s3_path=s3_path)
        df = pd.read_csv(body)
        count_rows = len(df)
        insert_data_from_buffer(df, connection)
        LOG.info(f"successfully inserted {count_rows} new row(s) to table")
        delete_s3_object(s3_path=s3_path)
        LOG.info(f"deleted {s3_path}")

    batch_id_table: pd.DataFrame = execute_read_query(
        query="select * from transactions_batch_id;", connection=connection
    )
    last_batch_id = int(batch_id_table["last_value"].iloc[0])
    LOG.info(f"last batch id to be added to graph : {last_batch_id}")
    sqs_message = {"last_batch_id": last_batch_id}
    send_sqs_message(message=sqs_message, queue_url=SQS_QUEUE_URL_FEED_GRAPH)
    connection.close()
