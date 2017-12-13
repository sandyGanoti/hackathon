from neo4j.v1 import GraphDatabase


class Neo4jRepository:
    def __init__(self, db_instance_ip, db_user, db_password):
        uri = "bolt://{}".format(db_instance_ip)
        driver = GraphDatabase.driver(uri, auth=(db_user, db_password))
        self.driver = driver


class UserRepository(Neo4jRepository):

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


class GameRepository(Neo4jRepository):

    def create_game(self):
        return
