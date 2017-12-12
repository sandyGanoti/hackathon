import json
import os
import logging
import urllib

# Grab the Bot OAuth token from the environment.
BOT_TOKEN = "xoxb-286531350151-MFLesbsehzDsxmnybsYqJQCo"

SLACK_URL = "https://slack.com/api/chat.postMessage"


def handle_miss_ping(event, context):
    print(event)
    slack_event = event['event']
    text = slack_event['text']
    channel_id = slack_event["channel"]

    data = urllib.parse.urlencode(
        (
            ("token", BOT_TOKEN),
            ("channel", channel_id),
            ("text", text)
        )
    )
    data = data.encode("ascii")
    request = urllib.request.Request(
        SLACK_URL,
        data=data,
        method="POST"
    )

    urllib.request.urlopen(request).read()

    return "200 OK"

    # body = {
    #     "message": "Hello slack! We are ready for pingo pong!",
    #     "input": event
    # }
    #
    # response = {
    #     "statusCode": 200,
    #     "body": json.dumps(body)
    # }
    #
    # return response

