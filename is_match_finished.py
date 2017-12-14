from __future__ import print_function
import json
import os

import boto3

from game_repo import GameRepository

NEO4J_EC2_IP = os.environ["NEO4J_EC2_IP"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

ARN_RES_IS_MATCH_FINISHED = "arn:aws:sns:us-east-1:580803390928:response_is_match_finished"


def request_is_match_finished(event, context):
    print(event)
    repository = GameRepository(
        db_instance_ip=NEO4J_EC2_IP,
        db_user=NEO4J_USER,
        db_password=NEO4J_PASSWORD
    )
    finished = repository.is_current_game_finished()
    print("finished: {}".format(finished))
    sns_client = boto3.client('sns')
    sns_message = {"finished": finished}
    sns_response = sns_client.publish(
            TopicArn=ARN_RES_IS_MATCH_FINISHED,
            Message=json.dumps(sns_message)
        )

    return {
        "statusCode": 200,
        "body": sns_response
    }
