from user_repo import UserRepository
import os

NEO4J_EC2_IP = os.environ["NEO4J_EC2_IP"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]


def write(event, context):
    print("event: {}".format(event))
    if "user" in event:
        repository = UserRepository(
            db_instance_ip=NEO4J_EC2_IP,
            db_user=NEO4J_USER,
            db_password=NEO4J_PASSWORD
        )

        user = repository.get_or_create_user(event["user"])
        return {
            "statusCode": 200,
            "body": user
        }
    return event
