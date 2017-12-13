from __future__ import print_function
import json
import os
import logging
import boto3

# Grab the Bot OAuth token from the environment.

from slackclient import SlackClient
BOT_TOKEN = os.environ["BOT_TOKEN"]
BOT_NAME = "Miss Ping"
PING_PONG_CHANNEL = "C8E4EUGGM"

SLACK_URL = "https://slack.com/api/chat.postMessage"

# topic arn

ARN_RES_WANT_TO_PLAY = "arn:aws:sns:us-east-1:580803390928:response_want_to_play"
ARN_RES_IS_MATCH_FINISHED = "arn:aws:sns:us-east-1:580803390928:response_is_match_finished"
ARN_RES_CURRENT_GAME = "arn:aws:sns:us-east-1:580803390928:response_current_game"

COMMANDS = {
    ":TABLE_TENNIS_PADDLE_AND_BALL:": "arn:aws:sns:us-east-1:580803390928:request_want_to_play",
    "IS CURRENT GAME FINISHED?": "arn:aws:sns:us-east-1:580803390928:request_is_match_finished",
    "WHO ARE PLAYING NOW?": "arn:aws:sns:us-east-1:580803390928:request_current_game"
}


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
    response_text = 'Hi @{} :wave:'.format(user) #TODO: remove?
    # todo : https://api.slack.com/methods/users.list

    sns_client = boto3.client('sns')

    sc = SlackClient(BOT_TOKEN)
    if text.upper() in COMMANDS:
        userInfo = sc.api_call(
            "users.info",
            user=user
        )

        userInfo["ok"]
        if userInfo["ok"] == "true":
            responseFromSns = sns_client.publish(
                # TargetArn=arn,
                # Message=json.dumps({'default': json.dumps(message)}),
                # MessageStructure='json'
                TopicArn=COMMANDS[text.upper()],
                Message=json.dumps(userInfo["user"]["name"])
            )
            print("response from SNS: {}".format(responseFromSns))
            return responseFromSns
    else:
        response = sc.api_call(
            "chat.postMessage",
            channel=PING_PONG_CHANNEL,
            text="Parse error :grimacing:",
        )
        return response


