BUCKET_NAME = "project-bucket"
PROCESSING_FOLDER = "processing"
NEW_DATA_FOLDER = "new_data"
ENDPOINT_URL = "http://localhost.localstack.cloud:4566"


db_name = "graph_project"
db_user = "postgres"
db_password = db_user
DB_CONFIG_DICT = {
    "host": "graph-project-postgres",
    "port": 5432,
    "dbname": db_name,
    "user": db_user,
    "password": db_password,
}
GREMLIN_CONFIG_DICT = {
    "protocol": "ws",
    "host": "graph-project-gremlin",
    "port": 8182,
    "service": "gremlin",
    "traversal_source": "g",
}
sqs_queue_url_template = "http://localhost:4566/000000000000/{}"
SQS_QUEUE_URL_FEED_TABLE = sqs_queue_url_template.format("feed-table-queue")
SQS_QUEUE_URL_FEED_GRAPH = sqs_queue_url_template.format("feed-graph-queue")
