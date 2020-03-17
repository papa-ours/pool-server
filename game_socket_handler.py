from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask, request, jsonify

from game_service import GameService
from user_service import UserService

class GameSocketHandler:
    @staticmethod
    def add_handlers(socket):
        @socket.on("get_balls")
        def get_balls_for_user():
            game, game_id = GameService.get_instance().get_game_for_user(request.sid)
            emit("get_balls_response", game.get_balls_for_user(UserService.get_instance().get_user(request.sid).username), room=request.sid)
            emit("game_players", game.get_members(), room=game_id)

        @socket.on("get_players")
        def get_players():
            game, game_id = GameService.get_instance().get_game_for_user(request.sid)
            emit("game_players", game.get_members(), room=request.sid)

        @socket.on("ball_entered")
        def ball_entered(data):
            game, game_id = GameService.get_instance().get_game_for_user(request.sid)
            user = game.ball_entered(int(data["number"]))
            emit("ball_entered_response", game.fills, room=game_id)
            emit("game_players", game.get_members(), room=game_id)
            emit("ball_removed", game.get_balls_for_user(user.username), room=user.sid)

