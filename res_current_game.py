from __future__ import print_function

import os

from slackclient import SlackClient


BOT_TOKEN = os.environ["BOT_TOKEN"]
PING_PONG_CHANNEL = "C8E4EUGGM"


def response_current_game(event, context):
    print(event)
    sc = SlackClient(BOT_TOKEN)
    response = sc.api_call(
            "chat.postMessage",
            channel=PING_PONG_CHANNEL,
            # text=", ".join(event["players"]),
            text="test",
        )
    print(response)
    return response
