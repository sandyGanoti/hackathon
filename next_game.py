from __future__ import print_function
import json
import os

import boto3

from game_repo import GameRepository

NEO4J_EC2_IP = os.environ["NEO4J_EC2_IP"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

ARN_RES_NEXT_GAME = "arn:aws:sns:us-east-1:580803390928:response_next_game"


def request_next_game(event, context):
    print("event: {}".format(event))
    user_name = event["Records"][0]["Sns"]["Message"]
    print(user_name)
    repository = GameRepository(
        db_instance_ip=NEO4J_EC2_IP,
        db_user=NEO4J_USER,
        db_password=NEO4J_PASSWORD
    )
    success = repository.finish_current_game(user_name)
    print("success: {}".format(success))
    sns_client = boto3.client('sns')
    sns_message = {"success": success}
    sns_response = sns_client.publish(
            TopicArn=ARN_RES_NEXT_GAME,
            Message=json.dumps(sns_message)
        )

    return {
            "statusCode": 200,
            "body": sns_response
        }
