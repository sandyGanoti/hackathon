import json


def write_from_bot(event, context):
    body = {
        "message": "I am going to write to slack channel",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Ready forn pingo pong",
        "event": event
    }
    """
