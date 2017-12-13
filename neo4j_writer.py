import json
import os
from neo4j.v1 import GraphDatabase

NEO4J_EC2_IP = os.environ["NEO4J_EC2_IP"]
NEO4J_USER = os.environ["NEO4J_USER"]
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]


def write(event, context):
    uri = "bolt://{}".format(NEO4J_EC2_IP)
    driver = GraphDatabase.driver(uri, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        greeting = session.write_transaction(_create_and_return_greeting, "hello")
        return {
            "statusCode": 200,
            "body": json.dumps(greeting)
        }


def _create_and_return_greeting(tx, message):
    result = tx.run("CREATE (a:Greeting) "
                    "SET a.message = $message "
                    "RETURN a.message + ', from node ' + id(a)", message=message)
    return result.single()[0]
