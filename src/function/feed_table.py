from utils.logger import LOG
import pandas as pd
from utils.functions.aws import (
    get_s3_path_from_event,
    get_s3_object_body_from_path,
    delete_s3_object,
)
from utils.functions.db import build_db_config_string, insert_data_from_buffer
from config.settings import db_config_dict
import psycopg2


def lambda_handler(event, context) -> None:

    s3_paths = get_s3_path_from_event(event)
    count_paths = len(s3_paths)
    LOG.info(f"retrieved {count_paths} file(s) with data to insert to table")
    connection_config: str = build_db_config_string(db_config_dict)
    connection = psycopg2.connect(connection_config)
    for s3_path in s3_paths:
        body = get_s3_object_body_from_path(s3_path=s3_path)
        df = pd.read_csv(body)
        count_rows = len(df)
        insert_data_from_buffer(df, connection)
        LOG.info(f"successfully inserted {count_rows} new row(s) to table")
        delete_s3_object(s3_path=s3_path)
        LOG.info(f"deleted {s3_path}")
    connection.close()


if __name__ == "__main__":
    connection_config: str = build_db_config_string(db_config_dict)
    connection = psycopg2.connect(connection_config)
