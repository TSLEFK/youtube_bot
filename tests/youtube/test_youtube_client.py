import os
from unittest import mock

import pytest

os.environ["API_KEY_NAME"] = "hoge"
from src.youtube.youtube_client import YoutubeClient


@pytest.fixture
def youtube_client():
    params = mock.MagicMock()
    params.return_value = "hoge"
    with mock.patch("src.youtube.youtube_client.get_parameter", return_value=params):
        return YoutubeClient()


def test_get_video_statics(youtube_client: YoutubeClient):
    statics_properties = {
        "title": ["snippet", "title"],
        "view_count": ["statistics", "viewCount"],
        "like_count": ["statistics", "likeCount"],
    }

    response = {
        "items": [
            {
                "kind": "youtube#video",
                "snippet": {
                    "channelId": "hoge",
                    "title": "fuga",
                    "channelTitle": "hoge",
                    "categoryId": "hoge",
                },
                "statistics": {
                    "viewCount": 12345,
                    "likeCount": 98765,
                    "dislikeCount": 10000,
                    "favoriteCount": 10000,
                    "commentCount": 10000,
                },
            }
        ]
    }
    with mock.patch(
        "src.youtube.youtube_client.YoutubeClient._execute_video_snippet_statics_list", return_value=response
    ):
        actual = youtube_client.get_video_statics(statics_properties, video_id="hoge")

    expected = {
        "title": "fuga",
        "view_count": 12345,
        "like_count": 98765,
    }
    assert actual == expected


def test_extract_statistics(youtube_client: YoutubeClient):

    statics_properties = {
        "title": ["snippet", "title"],
        "view_count": ["statistics", "viewCount"],
        "like_count": ["statistics", "likeCount"],
    }

    item = {
        "kind": "youtube#video",
        "snippet": {
            "channelId": "hoge",
            "title": "fuga",
            "channelTitle": "hoge",
            "categoryId": "hoge",
        },
        "statistics": {
            "viewCount": 12345,
            "likeCount": 98765,
            "dislikeCount": 10000,
            "favoriteCount": 10000,
            "commentCount": 10000,
        },
    }
    statistics = youtube_client._extract_statistics(item=item, properties=statics_properties)

    expected = {
        "title": "fuga",
        "view_count": 12345,
        "like_count": 98765,
    }

    assert expected == statistics
