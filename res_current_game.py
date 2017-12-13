from __future__ import print_function
import json
import os

from game_repo import GameRepository

NEO4J_EC2_IP = os.environ["NEO4J_EC2_IP"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

# topic arn
ARN_WANT_TO_PLAY = "arn:aws:sns:us-east-1:580803390928:request_want_to_play"
ARN_IS_MATCH_FINISHED = "arn:aws:sns:us-east-1:580803390928:request_is_match_finished"
ARN_CURRENT_GAME = "arn:aws:sns:us-east-1:580803390928:request_current_game"


def response_current_game(event, context):
    print(event)
    repository = GameRepository(
        db_instance_ip=NEO4J_EC2_IP,
        db_user=NEO4J_USER,
        db_password=NEO4J_PASSWORD
    )
    return repository.get_current_game()
