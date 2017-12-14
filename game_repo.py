from neo4j_repo import Neo4jRepository


class GameRepository(Neo4jRepository):

    def create_game(self):
        with self.driver.session() as session:
            game = session.write_transaction(self._create_and_return_game)
        return game

    def join_available_game(self, player_name):
        with self.driver.session() as session:
            game = session.read_transaction(self._get_current_game)
            # no games, create one
            if not game:
                game = session.write_transaction(self._create_and_return_game)
            else:
                # there is a current game
                is_available = session.read_transaction(self._get_is_game_available, game["id"])
                if not is_available:
                    next_game = game
                    # find the next game
                    while game is not None:
                        next_game = game
                        game = session.read_transaction(self._get_next_game_after, game["id"])
                        is_available = session.read_transaction(self._get_is_game_available, game["id"])
                        # if next game is available join it
                        if is_available:
                            success = session.write_transaction(self._join_game, game["id"], player_name)
                            return success
                    # no available game found, create one
                    game = session.write_transaction(self._create_next_game_after, next_game["id"])

            success = session.write_transaction(self._join_game, game["id"], player_name)
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
        result = tx.run("CREATE (g:Game {current: false, finished: false}) RETURN g")
        return result.single()["g"]["id"]

    @staticmethod
    def _join_game(tx, game_id, player_name):
        result = tx.run("Match (g:Game)<-[:PARTICIPATES]-(o:Player), (p:Player) "
                        "WHERE id(g) = {$game_id} "
                        "AND p.name = {$player_name} "
                        "WITH count(o) num_of_players, g as g, p as p "
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
                        "WITH count(o) as num_of_players, g as g "
                        "WHERE num_of_players < 2 "
                        "RETURN g")
        return result.single()["g"] if result.single() else None

    @staticmethod
    def _get_number_of_participants(tx, game_id):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(o:Player) "
                        "WHERE id(g) = {$game_id} "
                        "WITH count(o) as num_of_players "
                        "RETURN num_of_players", game_id=game_id)
        return result.single()[0]

    @staticmethod
    def _get_next_game_after(tx, game_id):
        result = tx.run("MATCH (g1:Game)<-[:NEXT_AFTER]-(g2:Game) "
                        "WHERE id(g1) = {$game_id} "
                        "RETURN g2", game_id=game_id)
        return result.single()["g2"] if result.single() else None

    @staticmethod
    def _create_next_game_after(tx, game_id):
        result = tx.run("MATCH (g1:Game) "
                        "WHERE id(g1) = {$game_id} "
                        "CREATE (g2:Game {current: false, finished: false})-[:NEXT_AFTER]->(g1) "
                        "RETURN g2", game_id=game_id)
        return result.single()["g2"]

    @staticmethod
    def _get_players_from_current_game(tx):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(p:Player) "
                        "WHERE g.current = true "
                        "RETURN p")
        results = result.records()
        return [result["p"]["name"] for result in results]

    @staticmethod
    def _get_current_game(tx):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(p:Player) "
                        "WHERE g.current = true "
                        "RETURN g")
        return result.single()["g"] if result.single() else None

    @staticmethod
    def _get_is_game_available(tx, game_id):
        result = tx.run("MATCH (g:Game)<-[:Participates]-(p:Player) "
                        "WHERE id(g) = {$game_id} "
                        "WITH count(o) as num_of_players "
                        "return num_of_players < 2", game_id=game_id)
        return result.single()[0]

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
        return result.single()[0]
