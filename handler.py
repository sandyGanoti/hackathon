import json
import os
import logging

# Grab the Bot OAuth token from the environment.

from slackclient import SlackClient
BOT_TOKEN = os.environ["BOT_TOKEN"]


SLACK_URL = "https://slack.com/api/chat.postMessage"


def handle_miss_ping(event, context):
    print(event)

    if "challenge" in event["body"]:
        return event["body"]["challenge"]

    slack_event = event['event']
    text = slack_event['text']
    channel_id = slack_event["channel"]

    if "bot_id" in slack_event:
        return

    sc = SlackClient(BOT_TOKEN)

    response = sc.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=text,
    )
    return response

