import json
import os
from neo4j.v1 import GraphDatabase

NEO4J_EC2_IP = os.environ["NEO4J_EC2_IP"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]


def write(event, context):
    if "user" in event:
        uri = "bolt://{}".format(NEO4J_EC2_IP)
        driver = GraphDatabase.driver(uri, auth=(NEO4J_USER, NEO4J_PASSWORD))
        repository = Neo4jUserRepository(driver)
        user = repository.get_or_create_user(event["user"])
        return {
            "statusCode": 200,
            "body": user
        }
    return event


class Neo4jUserRepository:

    def __init__(self, driver):
        self.driver = driver

    def find_user(self, user_name):
        with self.driver.session() as session:
            user = session.read_transaction(self._find_user, user_name)
            return user

    def create_user(self, user_name):
        with self.driver.session() as session:
            user = session.write_transaction(self._create_and_return_user, user_name)
            return user

    def get_or_create_user(self, user_name):
        existing_user = self.find_user(user_name)
        return existing_user if existing_user else self.create_user(user_name)

    @staticmethod
    def _create_and_return_user(tx, user_name):
        result = tx.run("CREATE (u:User) "
                        "SET u.name = $user_name "
                        "RETURN u", user_name=user_name)
        return result.single()["u"]["name"]

    @staticmethod
    def _find_user(tx, user_name):
        result = tx.run("MATCH (u:User) "
                        "WHERE u.name = $user_name "
                        "RETURN u", user_name=user_name)
        return result.single()["u"]["name"] if result.single() else None

