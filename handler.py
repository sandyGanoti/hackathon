import json
import os
import logging
import boto3

# Grab the Bot OAuth token from the environment.

from slackclient import SlackClient
BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_NAME = "Miss Ping"
BOT_ID = "C8E4EUGGM"

SLACK_URL = "https://slack.com/api/chat.postMessage"


def handle_miss_ping(event, context):
    print(event)

    if "challenge" in event:
        return event["challenge"]

    slack_event = event['event']
    if "bot_id" in slack_event:
        return

    text = slack_event['text']
    channel_id = slack_event['channel']
    user = slack_event['user']
    response_text = 'Hi @{} :wave:'.format(user)
    # todo : https://api.slack.com/methods/users.list

    sns_client = boto3.client('sns')
    topic = sns_client.create_topic(Name="read_from_bot")
    topic_arn = topic['TopicArn']

    responseFromSns = sns_client.publish(
        # TargetArn=arn,
        # Message=json.dumps({'default': json.dumps(message)}),
        # MessageStructure='json'
        TopicArn=topic_arn,
        Message=event
    )
    return


    # sc = SlackClient(BOT_TOKEN)
    # response = sc.api_call(
    #     "chat.postMessage",
    #     channel=BOT_ID,
    #     text=response_text,
    # )
    # return response

