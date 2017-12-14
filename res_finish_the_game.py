from __future__ import print_function

import json
import os

from slackclient import SlackClient

BOT_TOKEN = os.environ["BOT_TOKEN"]
PING_PONG_CHANNEL = "C8E4EUGGM"


def response_finish_the_game(event, context):
    print(event)

    sns_msg = json.loads(event["Records"][0]["Sns"]["Message"])
    sc = SlackClient(BOT_TOKEN)
    response = sc.api_call(
        "chat.postMessage",
        channel=PING_PONG_CHANNEL,
        text=", ".join(sns_msg["players"]),
    )
    print(response)
    return response
