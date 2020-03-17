import bson

from singleton import Singleton
from game import Game
from user_service import User

class Lobby:
    MAX_MEMBERS = 1
    def __init__(self, _id):
        self._id = _id
        self.members = []

    def is_full(self):
        return self.number_of_members() == Lobby.MAX_MEMBERS

    def get_usernames(self):
        return list(map(lambda user: user.username, self.members))

    def add_member(self, user):
        if user.username in self.get_usernames():
            self.members.pop(self.get_usernames().index(user.username))
        self.members.append(user)

    def number_of_members(self):
        return len(self.members)

    def remove_user(self, user):
        if user.username in self.get_usernames():
            self.members.pop(self.get_usernames().index(user.username))
            return True
        return False

class LobbyService(Singleton):
    def __init__(self):
        self.lobbies = {}

    def remove_lobby(self, lobby_id):
        if lobby_id in self.lobbies:
            del self.lobbies[lobby_id]

    def create_lobby(self):
        lobby_id = str(bson.ObjectId())
        self.lobbies[lobby_id] = Lobby(lobby_id)

    def remove_user(self, user):
        for lobby_id in self.lobbies.keys():
            lobby = self.lobbies[lobby_id]
            removed = lobby.remove_user(user)
            if removed:
                return lobby_id, lobby.number_of_members()
        return "", 0

    def add_user_to_lobby(self, user):
        if len(self.lobbies) == 0:
            self.create_lobby()
        for lobby_id in self.lobbies.keys():
            lobby = self.lobbies[lobby_id]
            if not lobby.is_full():
                lobby.add_member(user)
                return lobby_id, lobby.number_of_members()
