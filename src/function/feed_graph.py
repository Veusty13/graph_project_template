from utils.logger import LOG
from utils.functions.aws import get_message_from_sqs


def lambda_handler(event, context) -> None:
    message = get_message_from_sqs(event=event)
    for message_element in message:
        last_batch_id = message_element["last_batch_id"]
        LOG.info(last_batch_id)
