from neo4j_repo import Neo4jRepository


class UserRepository(Neo4jRepository):

    def find_player(self, user_name):
        with self.driver.session() as session:
            user = session.read_transaction(self._find_player, user_name)
            return user

    def create_player(self, user_name):
        with self.driver.session() as session:
            user = session.write_transaction(self._create_and_return_player, user_name)
            return user

    def get_or_create_player(self, user_name):
        existing_user = self.find_player(user_name)
        return existing_user if existing_user else self.create_player(user_name)

    @staticmethod
    def _create_and_return_player(tx, user_name):
        result = tx.run("CREATE (p:Player) "
                        "SET p.name = $player_name "
                        "RETURN p", player_name=user_name)
        return result.single()["p"]["name"]

    @staticmethod
    def _find_player(tx, user_name):
        result = tx.run("MATCH (p:Player) "
                        "WHERE p.name = $player_name "
                        "RETURN p", player_name=user_name)

        single_result = result.single()
        print("event: {}".format(single_result))
        return single_result["p"]["name"] if single_result else None