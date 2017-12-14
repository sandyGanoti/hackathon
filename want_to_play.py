from __future__ import print_function
import json
import os

import boto3

from game_repo import GameRepository
from user_repo import PlayerRepository

NEO4J_EC2_IP = os.environ["NEO4J_EC2_IP"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

ARN_RES_WANT_TO_PLAY = "arn:aws:sns:us-east-1:580803390928:response_want_to_play"


def request_want_to_play(event, context):
    print("event: {}".format(event))
    user_name = event["Records"][0]["Sns"]["Message"]
    print(user_name)
    game_repository = GameRepository(
        db_instance_ip=NEO4J_EC2_IP,
        db_user=NEO4J_USER,
        db_password=NEO4J_PASSWORD
    )
    player_repository = PlayerRepository(
        db_instance_ip=NEO4J_EC2_IP,
        db_user=NEO4J_USER,
        db_password=NEO4J_PASSWORD
    )
    player_repository.get_or_create_player(user_name)

    success = game_repository.join_available_game(user_name)

    sns_client = boto3.client('sns')
    sns_message = {"success": success, "user_name": user_name}
    sns_response = sns_client.publish(
            TopicArn=ARN_RES_WANT_TO_PLAY,
            Message=json.dumps(sns_message)
        )

    return {
        "statusCode": 200,
        "body": sns_response
    }
