

class Move:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final
        # initial and final are square on the board
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    