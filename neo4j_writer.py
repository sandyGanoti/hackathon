import json
from neo4j.v1 import GraphDatabase


def write(event, context):
    uri = "bolt://10.8.48.244:7687"
    user = "neo4j"
    password = "MissP!ng"
    driver = GraphDatabase.driver(uri, auth=(user, password))
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
