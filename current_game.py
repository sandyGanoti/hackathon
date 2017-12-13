from __future__ import print_function
import json
import os

from game_repo import GameRepository

BOT_NAME = "Miss Ping"
PING_PONG_CHANNEL = "C8E4EUGGM"

NEO4J_EC2_IP = os.environ["NEO4J_EC2_IP"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]


def request_current_game(event, context):
    print(event)
    repository = GameRepository(
        db_instance_ip=NEO4J_EC2_IP,
        db_user=NEO4J_USER,
        db_password=NEO4J_PASSWORD
    )
    return repository.get_current_game()
