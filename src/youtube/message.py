"""Massage Control Class."""
import json

import requests
from aws_lambda_powertools import Logger

logger = Logger(child=True)


class MassageControl(object):
    """Massage Control Class."""

    def __init__(self, urls: list[str]):
        """Initialise."""
        self.urls = urls
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def create_body(self, message):
        """Create Body."""
        return json.dumps({"message": message})

    def send_message(self, text: str):
        """Send message to urls.

        Args:
            text (str): _description_
        """
        for url in self.urls:
            response = self.session.post(
                url=url,
                data=json.dumps({"username": "~お嬢チャンネル情報~", "text": text}),
            )
            logger.info({"response": response.json})
