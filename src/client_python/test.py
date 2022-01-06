"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import random
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

# init pygame
from src.Graph.GraphAlgo import GraphAlgo

WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)

client = Client()
client.start_connection(HOST, PORT)

graph_json = client.get_graph()
algo = GraphAlgo()
object = json.loads(client.get_graph())
algo.load_graph(object)
print(algo.graph)
pokemons = json.loads(client.get_pokemons())
print(pokemons)
algo.pokemons_from_json(pokemons)


# load the json string into SimpleNamespace Object

# graph = json.loads(
#     graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in algo.graph.nodesMap:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
# min_x = min(list(algo.graph.nodesMap.values()), key=lambda n: n.pos.x).pos.x
# min_y = min(list(algo.graph.nodesMap.values()), key=lambda n: n.pos[1]).pos[1]
# max_x = max(list(algo.graph.nodesMap.values()), key=lambda n: n.pos[0]).pos[0]
# max_y = max(list(algo.graph.nodesMap.values()), key=lambda n: n.pos[1]).pos[1]


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

client.add_agent("{\"id\":0}")
client.add_agent("{\"id\":1}")
client.add_agent("{\"id\":2}")
client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

# print(client.get_agents())
while client.is_running() == 'true':
    algo.agent_from_json(client.get_agents())
    print(algo.graph.get_agents())
    pokemons = json.loads(client.get_pokemons())
    algo.pokemons_from_json(pokemons)

    pokemons = algo.graph.get_pokemons()
    for p in pokemons:
        x = p.pos[0]
        y = p.pos[1]
        # x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # agents = json.loads(client.get_agents(),
    #                     object_hook=lambda d: SimpleNamespace(**d)).Agents
    # agents = [agent.Agent for agent in agents]
    agents = algo.graph.get_agents()
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in algo.graph.nodesMap.values():
        x = my_scale(n.pos[0], x=True)
        y = my_scale(n.pos[1], y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for i in algo.graph.edgesMap.values():
        for e in i.values():
            # find the edge nodes
            src = next(n for n in algo.graph.nodesMap.values() if n.id == e.src)
            dest = next(n for n in algo.graph.nodesMap.values() if n.id == e.dest)

            # scaled positions
            src_x = my_scale(src.pos[0], x=True)
            src_y = my_scale(src.pos[1], y=True)
            dest_x = my_scale(dest.pos[0], x=True)
            dest_y = my_scale(dest.pos[1], y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126),
                             (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos[0]), int(agent.pos[1])), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    print(algo.graph)
    print(algo.graph.agents)
    for agent in algo.graph.agents.values():
        if agent.dest == -1:
            List = algo.sendAgent(agent)
            for v in List:
                client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(v) + '}')
        client.move()
# game over: