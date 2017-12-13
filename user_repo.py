from neo4j_repo import Neo4jRepository


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

        print("event: {}".format(result.single()))
        return result.single()["u"]["name"] if result and result.single() and result.single()["u"] else None