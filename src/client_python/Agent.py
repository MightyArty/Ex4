class Agent:
    def __init__(self, agentId: int, src: int, dest: int, speed: float, pos: tuple):
        self.id = agentId
        self.value = 0
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"Agent id : {self.id}, value : {self.value}, src : {self.src}, dest : {self.dest}, speed : {self.speed}, " \
               f"pos : {self.pos}"