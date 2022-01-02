class Agent:
    def __init__(self, agentId: int, value: float, src: int, dest: int, speed: float, pos: tuple):
        self.id = agentId
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def set_dest(self, newDest: int):
        self.dest = newDest

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"Agent (id : {self.id}, value : {self.value}, src : {self.src}, dest : {self.dest}, speed : {self.speed}, " \ 
               f"pos : {self.pos})"