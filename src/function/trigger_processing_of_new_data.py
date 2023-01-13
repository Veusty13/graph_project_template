from utils.logger import LOG
from config.settings import BUCKET_NAME, NEW_DATA_FOLDER, PROCESSING_FOLDER
from utils.functions.aws import get_all_s3_keys, get_s3_path, move_object


def lambda_handler(event, context) -> None:
    """lambda that aims at sending fresh data to the processing folder so that an event is sent to the lambda in charge of the data processing"""
    s3_folder_path_from = get_s3_path(
        bucket_name=BUCKET_NAME, path_in_bucket=NEW_DATA_FOLDER
    )
    s3_folder_path_to = get_s3_path(
        bucket_name=BUCKET_NAME, path_in_bucket=PROCESSING_FOLDER
    )
    keys = get_all_s3_keys(s3_path_to_folder=s3_folder_path_from)
    count_retrieved_keys = len(keys)
    count_failed_keys = 0
    for key_from in keys:
        try:
            key_to = key_from.replace(NEW_DATA_FOLDER, PROCESSING_FOLDER)
            s3_key_path_from = get_s3_path(
                bucket_name=BUCKET_NAME, path_in_bucket=key_from
            )
            s3_key_path_to = get_s3_path(bucket_name=BUCKET_NAME, path_in_bucket=key_to)
            move_object(s3_key_from=s3_key_path_from, s3_key_to=s3_key_path_to)
        except Exception as e:
            count_failed_keys += 1
            LOG.error(
                f"Could not move object in {s3_key_path_from} to {s3_key_path_to}, error : {e}"
            )

    LOG.info(
        f"done moving objects to {s3_folder_path_to}, total moved objects: {count_retrieved_keys - count_failed_keys}, failed : {count_failed_keys} key(s)"
    )
