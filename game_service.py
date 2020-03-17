from singleton import Singleton
from game import Game
from user_service import UserService

class GameService(Singleton):
    def __init__(self):
        self.games = {}

    def create_game(self, game_id, members):
        self.games[game_id] = Game(members)

    def get_game_for_user(self, sid):
        user = UserService.get_instance().get_user(sid)
        for game_id in self.games:
            game = self.games[game_id]
            if game.has_member(user.username):
                return game
