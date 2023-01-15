from utils.logger import LOG


def lambda_handler(event, context) -> None:
    print("excuting lambda function in charge of table feeding")
    print(event)
