# -*- coding: utf-8 -*-
"""Lambda Handler."""

import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parameters import get_parameter
from aws_lambda_powertools.utilities.typing import LambdaContext
from message import MassageControl
from youtube_client import YoutubeClient

# https://www.youtube.com/channel/UC7fk0CB07ly8oSl0aqKkqFg
CHANNEL_ID_NAME = os.environ["CHANNEL_ID_NAME"]
STREAM_ID_LIST_NAME = os.environ["STREAM_ID_LIST_NAME"]

NOTIFY_DISCORD_BOT = os.getenv("NOTIFY_DISCORD_BOT")
NOTIFY_SLACK_BOT = os.getenv("NOTIFY_SLACK_BOT")

logger = Logger(location="[%(name)s - %(filename)s] %(funcName)s:%(lineno)d")


def lambda_handler(event: dict, context: LambdaContext):
    """Call from Lambda."""
    channel_id, valid_stream_ids = get_valid_environment()

    youtube = YoutubeClient()
    subscriber_count = youtube.get_subscribe_count(channel_id=channel_id)
    logger.info({"subscriber_count": subscriber_count})

    statics_properties = {
        "title": ["snippet", "title"],
        "view_count": ["statistics", "viewCount"],
        "like_count": ["statistics", "likeCount"],
    }

    songs = [youtube.get_video_statics(statics_properties, video_id=stream_id) for stream_id in valid_stream_ids]
    logger.info({"songs": songs})

    urls = [NOTIFY_SLACK_BOT, NOTIFY_DISCORD_BOT]
    mess = MassageControl(urls=list(filter(None, urls)))

    message = {
        "視聴数": "view_count",
        "いいね数": "like_count",
    }
    mess.create_body(message=songs)

    message = {"チャンネル登録数": subscriber_count}
    mess.send_message(message)


def get_valid_environment() -> tuple[str, list[str]]:
    """Get the youtube environment values.

    Raises:
        ValueError: These environment values are not strings

    Returns:
        tuple[str, list[str]]: channel ID and stream IDs
    """
    channel_id = get_parameter(CHANNEL_ID_NAME)
    stream_ids = get_parameter(STREAM_ID_LIST_NAME)

    if not isinstance(channel_id, str) or not isinstance(stream_ids, list):
        logger.error(
            {
                "message": "CHANNEL_ID_NAME is not string.",
                "channels": channel_id,
                "stream_ids": stream_ids,
            }
        )
        raise ValueError("CHANNEL_ID_LIST or STREAM_ID_LIST is not list string.")

    valid_stream_ids: list[str] = [id for id in stream_ids if isinstance(id, str)]
    if len(valid_stream_ids) < len(stream_ids):
        logger.error({"message": "STREAM_ID_LIST is not list string."})

    return channel_id, valid_stream_ids


def hoge():
    return "a"
