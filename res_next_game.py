from __future__ import print_function

import json
import os

from slackclient import SlackClient

BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_NAME = "Miss Ping"
PING_PONG_CHANNEL = "C8E4EUGGM"


def response_next_game(event, context):
    print(event)
    sns_msg = json.loads(event["Records"][0]["Sns"]["Message"])
    sc = SlackClient(BOT_TOKEN)

    success = sns_msg["success"]

    slack_msg = "The game finished!" if success else "You can't finish a game that is not yours :wave: "
    response = sc.api_call(
        "chat.postMessage",
        channel=PING_PONG_CHANNEL,
        text=slack_msg,
    )
    print(response)
    return response
