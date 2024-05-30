import random as rd
VALUES = ["A", "B", "C", "D", "E"]
COLORS = ["yellow", "orange", "green", "blue", "red", "black"]
WHEELS = [[3, 4], [3, 4], [3, 4], [4], [4], []]
SHIPS = [[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3], [0, 1, 2, 3, 4]]
SKULL = 0.8
VALUES = [[1, 2, 3        , 1, 1],
          [1, 2, 3        , 2, 2],
          [1, 2, 3        , 2, 2],
          [1, 2, 3 - SKULL, 3, 2],
          [1, 2, 3 - SKULL, 3, 2],
          [1, 2, 3 - SKULL, 3, 4 - 2*SKULL]]

class Turn:
    def __init__(self, player):
        self.game_board = [[False] * 5 for i in range(6)]
        self.player = player

    def roll(self):
        val = rd.randint(0, 5)
        col = rd.randint(0, 5)
        if val == 5: val = 1
        # if wheel
        if val in WHEELS[col]:
            if True in [self.game_board[col][i] for i in WHEELS[col]]:
                for i in WHEELS[col]:
                    self.game_board[col][i] = False
                    return -1
            else:
                self.game_board[col][val] = True
        else:
            if self.player.remove(self): return
            if True in [self.game_board[col][i] for i in SHIPS[col]]:
                if self.player.reroll(self):
                    return self.roll()
                return 0
            self.game_board[col][val] = True
        return 1
    def play(self):
        while True:
            if not self.roll():
                return self.fail()
            if not self.player.continue_(self):
                return self.result()
    def count(self):
        return sum([col.count(True) for col in self.game_board])
    def result(self):
        count = self.count()
        ships_and_wheels = []
        for y in range(6):
            for x in range(5):
                if self.game_board[y][x]:
                    ships_and_wheels.append(VALUES[y][x])
        ships_and_wheels.sort()
        print(ships_and_wheels)
        if count <= 3:
            return ships_and_wheels.pop() - SKULL * (3-count)
        return sum(ships_and_wheels[3-count:])



    def fail(self):
        return 2 - SKULL

    def __str__(self):
        _string = ""
        for col in self.game_board:
            for val in col:
                if val:
                    _string += "X |"
                else:
                    _string += "  |"
            _string = _string[:-2] + "\n"
        return _string

class Player:
    def remove(self, turn): return False
    def reroll(self, turn): return False
    def continue_(self, turn):
        return turn.count() <= 4

player = Player()
result_list = [0] * 1000000
for i in range(100):
    alive = True
    j = 0
    turn = Turn(player)
    print(turn.play())
