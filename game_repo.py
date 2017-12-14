from neo4j_repo import Neo4jRepository


class GameRepository(Neo4jRepository):

    def create_game(self):
        with self.driver.session() as session:
            game = session.write_transaction(self._create_and_return_game)
        return game

    def join_available_game(self, player_name):
        with self.driver.session() as session:
            game = session.read_transaction(self._get_available_game)
            game_id = game["id"]
            if not game_id:
                return False
            success = session.write_transaction(self._join_game, game_id, player_name)
        return success

    def get_players_from_current_game(self):
        with self.driver.session() as session:
            game = session.read_transaction(self._get_players_from_current_game)
        return game

    def finish_current_game(self, player_name):
        with self.driver.session() as session:
            success = session.write_transaction(self._finish_game, player_name)
        return success

    @staticmethod
    def _create_and_return_game(tx):
        result = tx.run("CREATE (g:Game {current: false}) RETURN g")
        return result.single()["g"]["id"]

    @staticmethod
    def _join_game(tx, game_id, player_name):
        result = tx.run("Match (g:Game)<-[:PARTICIPATES]-(o:Player), (p:Player) "
                        "WHERE id(g) = {$game_id} "
                        "AND p.name = {$player_name} "
                        "WITH count(o) num_of_players "
                        "WHERE num_of_players < 2 "
                        "CREATE (p)-[r:PARTICIPATES]->(g) "
                        "RETURN r", game_id=game_id, player_name=player_name)
        if not result.single():
            print(result)
            return False
        if not result.single()["r"]:
            print(result.single())
            return False
        return True

    @staticmethod
    def _get_available_game(tx):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(o:Player) "
                        "WITH count(o) as num_of_players "
                        "WHERE num_of_players < 2 "
                        "RETURN g")
        return result.single()["g"] if result.single() else None

    @staticmethod
    def _get_players_from_current_game(tx):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(p:Player) "
                        "WHERE g.current = true "
                        "RETURN p")
        results = result.records()
        return [result["p"]["name"] for result in results]

    @staticmethod
    def _finish_game(tx, player_name):
        result = tx.run("MATCH (g:Game)<-[:Participates]-(p:Player) "
                        "WHERE g.current = true "
                        "AND p.name = {$player_name} "
                        "SET g.current = false "
                        "RETURN g", player_name=player_name)
        return True if result.single()["g"] else False

    @staticmethod
    def _is_current_game_finished(tx):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(p:Player) "
                        "WHERE g.current = true RETURN g.finished")
        results = result.records()
        return [result["p"]["name"] for result in results]
