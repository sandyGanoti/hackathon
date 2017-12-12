import json


def handle_miss_ping(event, context):
    body = {
        "message": "Hello slack! We are ready for pingo pong!",
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
