from __future__ import print_function

import json
import os

from slackclient import SlackClient

BOT_TOKEN = os.environ["BOT_TOKEN"]
PING_PONG_CHANNEL = "C8E4EUGGM"


def response_is_match_finished(event, context):
    print(event)
    sns_msg = json.loads(event["Records"][0]["Sns"]["Message"])
    sc = SlackClient(BOT_TOKEN)

    finished = sns_msg["finished"]
    slack_msg = "Current game finished" if finished else "Current game has not finished yet"
    response = sc.api_call(
            "chat.postMessage",
            channel=PING_PONG_CHANNEL,
            text=slack_msg,
        )
    print(response)
    return response
