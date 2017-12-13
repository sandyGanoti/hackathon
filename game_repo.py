from neo4j_repo import Neo4jRepository


class GameRepository(Neo4jRepository):

    def create_game(self):
        return