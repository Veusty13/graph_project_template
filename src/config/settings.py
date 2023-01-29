BUCKET_NAME = "project-bucket"
PROCESSING_FOLDER = "processing"
NEW_DATA_FOLDER = "new_data"
ENDPOINT_URL = "http://localhost.localstack.cloud:4566"


db_name = "graph_project"
db_user = "postgres"
db_password = db_user
db_config_dict = {
    "host": "graph-project-postgres",
    "port": 5432,
    "dbname": db_name,
    "user": db_user,
    "password": db_password,
}
