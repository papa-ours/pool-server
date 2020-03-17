import random
import copy

class Game:
    BALL_PER_MEMBER = 5
    COLORS = ["#0356fc", "#15bd42", "#de1818"]
    def __init__(self, members):
        self.members = members
        self.balls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.fills = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        self.distribute_balls()
    
    def get_members(self):
        member_list = []
        for i in range(len(self.members)):
            member_list.append({"username": self.members[i].username, "color": Game.COLORS[i], "numberOfBalls": len(self.members[i].balls)})
        return member_list

    def get_usernames(self):
        return list(map(lambda user: user.username, self.members))

    def has_member(self, username):
        return username in self.get_usernames()

    def get_user(self, username):
        return self.members[self.members.index(username)]

    def get_balls_for_user(self, username):
        return self.get_user(username).active_balls

    def distribute_balls(self):
        for member in self.members:
            sample = random.sample(self.balls, k=Game.BALL_PER_MEMBER)
            sample.sort()
            for n in sample:
                self.balls.pop(self.balls.index(n))
            member.balls = copy.deepcopy(sample)
            member.active_balls = copy.deepcopy(sample)

    def member_index_with_ball(self, number):
        index = 0
        for member in self.members:
            if number in member.balls:
                return index
            index = index + 1

    def ball_entered(self, number):
        member_index = self.member_index_with_ball(number)
        self.fills[number - 1] = Game.COLORS[member_index]
        self.members[member_index].active_balls.pop(self.members[member_index].active_balls.index(number))
        return self.members[member_index]
    
    def cancel_ball_entered(self, number):
        member_index = self.member_index_with_ball(number)
        self.fills[number - 1] = ""
        self.members[member_index].active_balls.append(number)
        return self.members[member_index]

    def remaining_balls_count(self):
        count = 0
        for member in self.members:
            count = count + len(member.active_balls)
        return count
            
    def get_winner(self):
        for member in self.members:
            if len(member.active_balls) > 0:
                return member