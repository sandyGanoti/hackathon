from neo4j_repo import Neo4jRepository


class GameRepository(Neo4jRepository):

    def join_available_game(self, player_name):
        with self.driver.session() as session:
            game_id = session.read_transaction(self._get_current_game)
            # no games, create one
            if not game_id:
                game_id = session.write_transaction(self._create_and_return_game)
            else:
                # there is a current game
                is_available = session.read_transaction(self._get_is_game_available, game_id)
                if not is_available:
                    next_game_id = game_id
                    # find the next game
                    while game_id is not None:
                        next_game_id = game_id
                        print("next game id: {}".format(next_game_id))
                        game_id = session.read_transaction(self._get_next_game_after, game_id)
                        if game_id:
                            is_available = session.read_transaction(self._get_is_game_available, game_id)
                            # if next game is available join it
                            if is_available:
                                success = session.write_transaction(self._join_game, game_id, player_name)
                                return success
                    # no available game found, create one
                    game_id = session.write_transaction(self._create_next_game_after, next_game_id)

            success = session.write_transaction(self._join_game, game_id, player_name)
        return success

    def get_players_from_current_game(self):
        with self.driver.session() as session:
            game = session.read_transaction(self._get_players_from_current_game)
        return game

    def get_players_from_game(self, game_id):
        with self.driver.session() as session:
            players = session.read_transaction(self._get_players_from_game, game_id)
        return players

    def finish_current_game(self, player_name):
        with self.driver.session() as session:
            success = session.write_transaction(self._finish_game, player_name)
        return success

    def is_current_game_finished(self):
        with self.driver.session() as session:
            success = session.read_transaction(self._is_current_game_finished)
        return success

    def get_next_after_current(self):
        with self.driver.session() as session:
            current_game_id = session.read_transaction(self._get_current_game)
            next_game_id = session.read_transaction(self._get_next_game_after, current_game_id)
        return next_game_id

    @staticmethod
    def _create_and_return_game(tx):
        result = tx.run("CREATE (g:Game {current: true, finished: false}) RETURN id(g)")
        return result.single()[0]

    @staticmethod
    def _join_game(tx, game_id, player_name):
        result = tx.run("Match (g:Game), (p:Player) "
                        "WHERE id(g) = $game_id "
                        "AND p.name = $player_name "
                        "CREATE (p)-[r:PARTICIPATES]->(g) "
                        "RETURN r", game_id=game_id, player_name=player_name)
        single_result = result.single()
        print("join game result: {}".format(single_result))
        return True

    @staticmethod
    def _get_available_game(tx):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(o:Player) "
                        "WITH count(o) as num_of_players, g as g "
                        "WHERE num_of_players < 2 "
                        "RETURN id(g)")
        single_result = result.single()
        return single_result[0] if single_result else None

    @staticmethod
    def _get_number_of_participants(tx, game_id):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(o:Player) "
                        "WHERE id(g) = $game_id "
                        "WITH count(o) as num_of_players "
                        "RETURN num_of_players", game_id=game_id)
        return result.single()[0]

    @staticmethod
    def _get_next_game_after(tx, game_id):
        result = tx.run("MATCH (g1:Game)<-[:NEXT_AFTER]-(g2:Game) "
                        "WHERE id(g1) = $game_id "
                        "RETURN id(g2)", game_id=game_id)
        single_result = result.single()
        return single_result[0] if single_result else None

    @staticmethod
    def _create_next_game_after(tx, game_id):
        result = tx.run("MATCH (g1:Game) "
                        "WHERE id(g1) = $game_id "
                        "CREATE (g2:Game {current: false, finished: false})-[:NEXT_AFTER]->(g1) "
                        "RETURN id(g2)", game_id=game_id)
        return result.single()[0]

    @staticmethod
    def _get_players_from_current_game(tx):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(p:Player) "
                        "WHERE g.current = true "
                        "RETURN p")
        results = result.records()
        return [result["p"]["name"] for result in results]

    @staticmethod
    def _get_players_from_game(tx, game_id):
        result = tx.run("MATCH (g:Game)<-[r:PARTICIPATES]-(p:Player) "
                        "WHERE id(g) = $game_id "
                        "RETURN p", game_id=game_id)
        results = result.records()
        return [result["p"]["name"] for result in results]

    @staticmethod
    def _get_current_game(tx):
        result = tx.run("MATCH (g:Game) "
                        "WHERE g.current = true "
                        "RETURN id(g)")
        single_result = result.single()
        return single_result[0] if single_result else None

    @staticmethod
    def _get_is_game_available(tx, game_id):
        print("game id={}".format(game_id))
        result = tx.run("MATCH (g:Game)<-[:Participates]-(p:Player) "
                        "WHERE id(g) = $game_id "
                        "WITH count(p) as num_of_players "
                        "return num_of_players < 2", game_id=game_id)
        _result = result.single()[0]
        print(_result)
        return _result

    @staticmethod
    def _finish_game(tx, player_name):
        result = tx.run("MATCH (g:Game)<-[:Participates]-(p:Player) "
                        "WHERE g.current = true "
                        "AND p.name = $player_name "
                        "SET g.current = false, g.finished = true "
                        "RETURN id(g)", player_name=player_name)
        return True if result.single()[0] else False

    @staticmethod
    def _is_current_game_finished(tx):
        result = tx.run("MATCH (g:Game) "
                        "WHERE g.current = true RETURN g.finished")
        return result.single()[0]
