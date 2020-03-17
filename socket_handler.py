from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask, request, jsonify

from lobby_service import LobbyService, Lobby
from user_service import UserService
from game_service import GameService
from game_socket_handler import GameSocketHandler

class SocketHandler:
    _socket: SocketIO

    __instance = None

    def __init__(self, app: Flask = None):
        self._socket = SocketIO()
        self._socket.init_app(app, cors_allowed_origins="*")
        self.add_handlers()
        GameSocketHandler.add_handlers(self._socket)

    @staticmethod
    def get_instance():
        return SocketHandler.__instance

    @staticmethod
    def set_app(app):
        if SocketHandler.__instance == None:
            SocketHandler.__instance = SocketHandler(app)

    def run(self, app : Flask):
        self._socket.run(app, host = "0.0.0.0")

    def add_handlers(self):
        @self._socket.on("connect")
        def connect():
            pass

        @self._socket.on("connect_user")
        def connect_user(connection_data):
            user_connected = UserService.get_instance().connect_user(request.sid, connection_data["username"])
            emit("connect_user_response", user_connected, room=request.sid)

        @self._socket.on("find_game")
        def find_game():
            lobby_id, n_members = LobbyService.get_instance().add_user_to_lobby(UserService.get_instance().get_user(request.sid))
            join_room(str(lobby_id))
            emit("find_game_response", {"lobbyId": lobby_id, "numberOfMembers": n_members}, room=lobby_id)
            if LobbyService.get_instance().lobbies[lobby_id].is_full():
                GameService.get_instance().create_game(lobby_id, LobbyService.get_instance().lobbies[lobby_id].members)
                LobbyService.get_instance().remove_lobby(lobby_id)
                emit("game_started", room=lobby_id)

        @self._socket.on("disconnect_user")
        def disconnect_user():
            lobby_id, n_members = LobbyService.get_instance().remove_user(UserService.get_instance().get_user(request.sid))
            if lobby_id != "":
                leave_room(lobby_id)
                emit("find_game_response", {"lobbyId": lobby_id, "numberOfMembers": n_members}, room=lobby_id)
            UserService.get_instance().disconnect_user(request.sid)

        @self._socket.on("disconnect")
        def disconnect():
            lobby_id, n_members = LobbyService.get_instance().remove_user(UserService.get_instance().get_user(request.sid))
            if lobby_id != "":
                leave_room(lobby_id)
                emit("find_game_response", {"lobbyId": lobby_id, "numberOfMembers": n_members}, room=lobby_id)
            UserService.get_instance().disconnect_user(request.sid)

        # @self._socket.on_error()        # Handles the default namespace
        # def error_handler(error):
        #     print("Error " + str(error))
        #     self._socket.emit("error", str(error))
