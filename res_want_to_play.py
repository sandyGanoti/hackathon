from __future__ import print_function

import json
import os

from slackclient import SlackClient

# Grab the Bot OAuth token from the environment.
BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_NAME = "Miss Ping"
PING_PONG_CHANNEL = "C8E4EUGGM"

SLACK_URL = "https://slack.com/api/chat.postMessage"


def response_want_to_play(event, context):
    print(event)
    sns_msg = json.loads(event["Records"][0]["Sns"]["Message"])
    sc = SlackClient(BOT_TOKEN)

    success = sns_msg["success"]
    user_name = sns_msg["user_name"]

    slack_msg = "<@{}> you joined a game" if success else "<@{}> I couldn't find you a game"
    slack_msg = slack_msg.format(user_name)
    response = sc.api_call(
            "chat.postMessage",
            channel=PING_PONG_CHANNEL,
            text=slack_msg,
        )
    print(response)
    return response
