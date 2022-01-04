

class Pokemon:
    def __init__(self, value: float, pokemonType: int, pos: tuple):
        self.value = value
        self.type = pokemonType
        self.pos = pos

    def get_pos(self):
        return self.pos

    def isOn(self, src_X, src_Y, dest_X, dest_Y) -> bool:
        m = float((src_Y - dest_Y) / (src_X - dest_X))
        if (self.pos[1] - src_Y) == m * (self.pos[0] - src_X):
            return True
        return False

    def __repr__(self):
        return f"Pokemon (value : {self.value}, type : {self.type}, pos : {self.pos})"

