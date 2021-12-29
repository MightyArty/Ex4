class Node:

    def __init__(self, myID: int, pos: tuple = None):
        self.id = myID
        self.pos = pos
        self.tag = 0

    def get_id(self):
        return self.id

    def get_tag(self):
        return self.tag

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"Node id: {self.id}, pos: {self.pos}"