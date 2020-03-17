from flask import Flask
from flask_cors import CORS
from socket_handler import SocketHandler

class App:
    def __init__(self, run = True):
        self.app = Flask(__name__)
        cors = CORS(self.app)
        # To activate hot reloading
        self.app.debug = True
        SocketHandler.set_app(self.app)
    
    def run(self, debug = True):
        self.app.debug = debug
        SocketHandler.get_instance().run(self.app)
