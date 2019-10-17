import constants


class City:
    def __init__(self, name, pos, owner):
        self.pos = pos
        self.name = name
        self.owner = owner

        self.hammer_rate = 0
        self.hammers = 0

        self.buildings = 0

        self.soldier_rate = 2
        self.soldiers = 0

    def calculate_hammer_rate(self, terrain):
        rate = 0
        for col in range(3):
            for row in range(3):
                if len(terrain) - 1 >= (self.pos[1] - 1) + row:
                    if len(terrain[(self.pos[1] - 1) + row]) - 1 >= (self.pos[0] - 1) + col:
                        rate += constants.HAMMRT_dict[terrain[(self.pos[1] - 1) + row][(self.pos[0] - 1) + col]]

        self.hammer_rate = rate

    def run_turn(self):
        self.hammers += self.hammer_rate
        self.soldiers += self.soldier_rate
