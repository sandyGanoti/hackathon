import json
import os
from slackclient import SlackClient

BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_NAME = "Miss Ping"
BOT_ID = "C8E4EUGGM"


def read_from_bot(event, context):
    print(event)

    if "challenge" in event:
        return event["challenge"]

    slack_event = event['event']
    if "bot_id" in slack_event:
        return

    text = slack_event['text']
    channel_id = slack_event['channel']
    user = slack_event['user']

    sc = SlackClient(BOT_TOKEN)
    response = sc.api_call(
        "chat.postMessage",
        channel=BOT_ID,
        text=text,
    )
    return response
