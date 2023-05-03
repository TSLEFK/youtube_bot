"""YouTube API Class."""
import os
from typing import Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parameters import get_parameter
from googleapiclient.discovery import build

API_KEY_NAME = os.environ["API_KEY_NAME"]

logger = Logger(child=True)


class YoutubeClient:
    """YT Client class.

    Returns:
        _type_: YT Client class.
    """
    def __init__(self) -> None:
        """Initialize youtube instance."""
        self.client = build(
            "youtube",
            "v3",
            developerKey=get_parameter(name=API_KEY_NAME, decrypt=True),
        )

    def _execute_channel_statics(self, channel_id: str) -> dict[str, Any]:
        # https://developers.google.com/youtube/v3/docs/channels?hl=ja#%E3%83%AA%E3%82%BD%E3%83%BC%E3%82%B9%E8%A1%A8%E7%8F%BE
        return self.client.channels().list(part="statistics", id=channel_id).execute()

    def get_subscribe_count(self, channel_id) -> int:
        """Get subscribe count of a channel.

        Args:
            channel_id (_type_): youtube channel id.

        Returns:
            int: channel subscribe count
        """
        statics_response = self._execute_channel_statics(channel_id=channel_id)

        subscriber_counts = [
            item.get("statistics", {}).get("subscriberCount")
            for item in statics_response.get("items", {})
            if item["kind"] == "youtube#channel"
        ]

        logger.info({"subscriber_counts": subscriber_counts})

        return int(subscriber_counts[0]) if subscriber_counts[0] else 0

    def _execute_video_snippet_statics_list(self, video_id: str):
        # https://developers.google.com/youtube/v3/docs/videos?hl=ja#%E3%83%AA%E3%82%BD%E3%83%BC%E3%82%B9%E8%A1%A8%E7%8F%BE
        return self.client.videos().list(part="snippet,statistics", id=video_id).execute()

    def get_video_statics(self, statics_properties: dict, video_id: str) -> dict[str, str]:
        """Get video statistics.

        Args:
            video_id (str): youtube video id.

        Returns:
            dict[str, str]: video statistics that is title, view count, like count.
        """
        statics_response = self._execute_video_snippet_statics_list(video_id=video_id)

        video = [
            self._extract_statistics(item=item, properties=statics_properties)
            for item in statics_response.get("items", [])
            if item["kind"] == "youtube#video"
        ][0]

        logger.info(
            {
                "title": video.get("title"),
                "watch": video.get("view_count"),
                "like": video.get("like_count"),
            }
        )

        return video

    def _extract_statistics(self, item: dict, properties: dict) -> dict[str, Any]:
        extracted_items = {}
        for name, props in properties.items():
            extracted_items.update({name: item.get(props[0], {}).get(props[1], "-")})

        return extracted_items
