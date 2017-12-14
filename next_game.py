from __future__ import print_function
import json
import os

import boto3

from game_repo import GameRepository

BOT_NAME = "Miss Ping"
PING_PONG_CHANNEL = "C8E4EUGGM"

NEO4J_EC2_IP = os.environ["NEO4J_EC2_IP"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

ARN_RES_NEXT_GAME = "arn:aws:sns:us-east-1:580803390928:response_next_game"


def request_next_game(event, context):
    print(event)
    repository = GameRepository(
        db_instance_ip=NEO4J_EC2_IP,
        db_user=NEO4J_USER,
        db_password=NEO4J_PASSWORD
    )
    players = repository.get_players_from_current_game()
    print(players)
    sns_client = boto3.client('sns')
    sns_response = sns_client.publish(
            TopicArn=ARN_RES_NEXT_GAME,
            Message=json.dumps({"players": players})
        )

    return {
            "statusCode": 200,
            "body": sns_response
        }
