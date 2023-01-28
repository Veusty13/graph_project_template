import boto3
from typing import List, Any
from config.settings import ENDPOINT_URL
import json

s3 = boto3.client(service_name="s3", endpoint_url=ENDPOINT_URL)


def parse_s3_path(s3_path: str) -> List[str]:
    bucket = s3_path.split("//")[1].split("/")[0]
    folder_path = "/".join(s3_path.split("//")[1].split("/")[1:])
    return [bucket, folder_path]


def get_all_s3_keys(s3_path_to_folder: str) -> List[str]:
    bucket, folder_in_bucket_to_scan = parse_s3_path(s3_path_to_folder)
    kwargs = {"Bucket": bucket, "Prefix": folder_in_bucket_to_scan}
    keys = []
    while True:
        resp = s3.list_objects_v2(**kwargs)
        key_count = resp["KeyCount"]
        if key_count:
            for obj in resp["Contents"]:
                keys.append(obj["Key"])
            try:
                kwargs["ContinuationToken"] = resp["NextContinuationToken"]
            except KeyError:
                break
        else:
            break
    return keys


def get_s3_path_from_event(event: dict) -> List[str]:
    s3_paths_list = []
    records = event["Records"]
    for record in records:
        body = json.loads(record["body"])
        for body_record in body["Records"]:
            s3_info = body_record["s3"]
            bucket = s3_info["bucket"]["name"]
            key = s3_info["object"]["key"]
            s3_path = get_s3_path(bucket_name=bucket, path_in_bucket=key)
            s3_paths_list.append(s3_path)
    return s3_paths_list


def get_s3_object_body_from_path(s3_path) -> Any:
    bucket, key = parse_s3_path(s3_path=s3_path)
    data = s3.get_object(Bucket=bucket, Key=key)
    body = data["Body"]
    return body


def move_object(s3_path_from: str, s3_path_to: str) -> None:
    bucket_name, key_from = parse_s3_path(s3_path_from)
    _, key_to = parse_s3_path(s3_path_to)
    copy_source = {"Bucket": bucket_name, "Key": key_from}
    s3.copy_object(Bucket=bucket_name, CopySource=copy_source, Key=key_to)
    s3.delete_object(Bucket=bucket_name, Key=key_from)


def delete_s3_object(s3_path: str) -> None:
    bucket_name, key = parse_s3_path(s3_path)
    s3.delete_object(Bucket=bucket_name, Key=key)


def get_s3_path(bucket_name: str, path_in_bucket: str) -> str:
    return f"s3://{bucket_name}/{path_in_bucket}"
