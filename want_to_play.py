from __future__ import print_function
import json
import os
from slackclient import SlackClient

BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_NAME = "Miss Ping"
PING_PONG_CHANNEL = "C8E4EUGGM"


def request_want_to_play(event, context):
    print("event: {}".format(event))
    sns_message = json.loads(event["Records"][0]["Sns"]["Message"])

    if "challenge" in sns_message:
        return sns_message["challenge"]

    slack_event = sns_message['event']
    if "bot_id" in slack_event:
        return

    text = slack_event['text']
    channel_id = slack_event['channel']
    user = slack_event['user']

    sc = SlackClient(BOT_TOKEN)
    response = sc.api_call(
        "chat.postMessage",
        channel=PING_PONG_CHANNEL,
        text=text,
    )
    return response
