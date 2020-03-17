from singleton import Singleton

class User:
    def __init__(self, username):
        self.username = username
        self.balls = []
    
    def __eq__(self, username):
        return self.username == username

class UserService(Singleton):
    def __init__(self):
        self.active_users = {}

    def get_users(self):
        return list(self.active_users.values())

    def get_user(self, sid):
        return self.active_users[sid]

    def get_usernames(self):
        return list(map(lambda user: user.username, self.get_users()))
    
    def connect_user(self, sid, username):
        if sid in self.active_users or username in self.get_usernames():
            return False
        self.active_users[sid] = User(username)
        return True

    def disconnect_user(self, sid):

        print(self.active_users[sid].username + " is leaving")
        del self.active_users[sid]
