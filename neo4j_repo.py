from neo4j.v1 import GraphDatabase


class Neo4jRepository:
    def __init__(self, db_instance_ip, db_user, db_password):
        uri = "bolt://{}".format(db_instance_ip)
        driver = GraphDatabase.driver(uri, auth=(db_user, db_password))
        self.driver = driver
