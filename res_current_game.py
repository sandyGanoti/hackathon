from __future__ import print_function

import os

# topic arn
ARN_WANT_TO_PLAY = "arn:aws:sns:us-east-1:580803390928:request_want_to_play"
ARN_IS_MATCH_FINISHED = "arn:aws:sns:us-east-1:580803390928:request_is_match_finished"
ARN_CURRENT_GAME = "arn:aws:sns:us-east-1:580803390928:request_current_game"


def response_current_game(event, context):
    print(event)
    return event
