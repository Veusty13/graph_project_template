from utils.logger import LOG
from utils.functions.aws import get_s3_path_from_event, get_s3_object_body_from_path
import pandas as pd
import io
from typing import Any
import psycopg2


def insert_with_string_io(df: pd.DataFrame, connection: Any):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    with connection.cursor() as cursor:
        cursor.copy_expert(
            f"COPY transactions FROM STDIN (FORMAT 'csv', HEADER false)",
            buffer,
        )
        connection.commit()


def lambda_handler(event, context) -> None:
    s3_paths = get_s3_path_from_event(event)
    connection_config = "host='localhost' port='5432' dbname='graph_project' user='postgres' password='postgres'"
    connection = psycopg2.connect(connection_config)
    cursor = connection.cursor()
    for s3_path in s3_paths:
        body = get_s3_object_body_from_path(s3_path=s3_path)
        df = pd.read_csv(body)
        insert_with_string_io(df, connection)
    cursor.close()


# import psycopg2
# conn = psycopg2.connect("host='localhost' port='5432' dbname='Ekodev' user='bn_openerp' password='fa05844d'")
# cur = conn.cursor()
# cur.execute("""truncate table "meta".temp_unicommerce_status;""")
# cur.execute("""Copy temp_unicommerce_status from 'C:\Users\n\Desktop\data.csv';""")
# conn.commit()
# conn.close()

if __name__ == "__main__":
    event = {
        "Records": [
            {
                "eventVersion": "2.2",
                "eventSource": "aws:s3",
                "awsRegion": "us-west-2",
                "eventTime": "The time, in ISO-8601 format, for example, 1970-01-01T00:00:00.000Z, when Amazon S3 finished processing the request",
                "eventName": "event-type",
                "userIdentity": {
                    "principalId": "Amazon-customer-ID-of-the-user-who-caused-the-event"
                },
                "requestParameters": {
                    "sourceIPAddress": "ip-address-where-request-came-from"
                },
                "responseElements": {
                    "x-amz-request-id": "Amazon S3 generated request ID",
                    "x-amz-id-2": "Amazon S3 host that processed the request",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "ID found in the bucket notification configuration",
                    "bucket": {
                        "name": "project-bucket",
                        "ownerIdentity": {
                            "principalId": "Amazon-customer-ID-of-the-bucket-owner"
                        },
                        "arn": "bucket-ARN",
                    },
                    "object": {
                        "key": "new_data/fraud_data_partition_1.csv",
                        "size": "object-size in bytes",
                        "eTag": "object eTag",
                        "versionId": "object version if bucket is versioning-enabled, otherwise null",
                        "sequencer": "a string representation of a hexadecimal value used to determine event sequence, only used with PUTs and DELETEs",
                    },
                },
                "glacierEventData": {
                    "restoreEventData": {
                        "lifecycleRestorationExpiryTime": "The time, in ISO-8601 format, for example, 1970-01-01T00:00:00.000Z, of Restore Expiry",
                        "lifecycleRestoreStorageClass": "Source storage class for restore",
                    }
                },
            }
        ]
    }
    lambda_handler(event, "")
