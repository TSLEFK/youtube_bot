from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(location="[%(name)s - %(filename)s] %(funcName)s:%(lineno)d")


def lambda_handler(event, context: LambdaContext):
    hoge()


def hoge():
    return "a"
