from src.Graph.DiGraph import DiGraph


class Pokemon:
    def __init__(self, value: float, pokemonType: int, pos: tuple):
        self.value = value
        self.type = pokemonType
        self.pos = pos

    def __repr__(self):
        return f"Pokemon (value : {self.value}, type : {self.type}, pos : {self.pos})"

