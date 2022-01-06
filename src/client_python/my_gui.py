import sys

import pygame
from pygame import *
import json

from pygame import gfxdraw

from client import Client
from src.Graph.GraphAlgo import GraphAlgo
from src.Graph.DiGraph import DiGraph
from Pokemon import Pokemon

# from src.client_python.student_code import scale

WIDTH, HEIGHT = 1080, 720
PORT = 6666
HOST = '127.0.0.1'

pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)

clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)

client = Client()
client.start_connection(HOST, PORT)

algo = GraphAlgo()
ob = json.loads(client.get_graph())
algo.load_graph(ob)

min_x = sys.float_info.max
min_y = sys.float_info.max
max_x = sys.float_info.min
max_y = sys.float_info.min

for node in algo.graph.get_all_v().values():
    x_, y_, z_ = node.get_pos()
    if max_x < x_:
        max_x = x_
    if max_y < y_:
        max_y = y_
    if min_x > x_:
        min_x = x_
    if min_y > y_:
        min_y = y_


def Scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def my_scale(data, x=False, y=False):
    if x:
        return Scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return Scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

pkOb = json.loads(client.get_pokemons())
algo.pokemons_from_json(pkOb)

# good_pos = 0
# for pok in algo.graph.pokemons:
#     edge = algo.find_pokemon_edge(pok)
#     good_pos = edge.src

# client.add_agent("{\"id\":" + str(good_pos) + "}")


# client.add_agent("{\"id\":" + str(start_pos) + "}")
amount_of_agents = int(json.loads(client.get_info())["GameServer"]["agents"])
for ag in range(amount_of_agents):
    client.add_agent("{\"id\":" + str(ag) + "}")

pokOb = json.loads(client.get_pokemons())
agOb = json.loads(client.get_agents())

algo.agent_from_json(agOb)
algo.pokemons_from_json(pokOb)
# print(algo.graph.get_agents())
# print(algo.graph.get_pokemons())

client.start()
sizeOfPokemons = len(algo.graph.pokemons)
while client.is_running() == 'true':
    agOb = json.loads(client.get_agents())
    algo.agent_from_json(agOb)
    if len(algo.graph.pokemons) != sizeOfPokemons:
        pkOb = json.loads(client.get_pokemons())
        algo.pokemons_from_json(pkOb)



    # print(algo.graph.get_agents())
    # print(algo.graph.get_pokemons())

    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(pygame.Color(0, 0, 0))

    # draw nodes
    for node in algo.get_graph().get_all_v().values():
        x, y, z = node.get_pos()
        x = my_scale(x, x=True)
        y = my_scale(y, y=True)

        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(node.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

        # draw edges
        for e in algo.get_graph().all_out_edges_of_node(node.id).keys():
            source = node.id
            destination = e

            # scaled position
            src_x, src_y, src_z = algo.graph.get_all_v()[source].get_pos()
            dest_x, dest_y, dest_z = algo.graph.get_all_v()[destination].get_pos()
            sx = my_scale(src_x, x=True)
            sy = my_scale(src_y, y=True)
            dx = my_scale(dest_x, x=True)
            dy = my_scale(dest_y, y=True)

            # draw the line
            pygame.draw.line(screen, Color(61, 72, 126),
                             (sx, sy), (dx, dy))

    # draw agents
    for agent in algo.graph.agents.values():
        x_, y_, z_ = agent.get_pos()
        x = my_scale(x_, x=True)
        y = my_scale(y_, y=True)
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(x), int(y)), 10)
    # draw pokemons
    for pok in algo.graph.pokemons:
        x_, y_, z_ = pok.get_pos()
        x = my_scale(x_, x=True)
        y = my_scale(y_, y=True)
        pygame.draw.circle(screen, Color(0, 255, 255),
                           (int(x), int(y)), 10)

    display.update()

    clock.tick(10)

    # choose next edge for the agent
    # print(algo.graph.get_agents())
    for pok in algo.graph.pokemons:
        findArr = algo.find_agent(pok)
        Agent = findArr[0]
        tempDest = Agent.dest
        edge = findArr[2]
        if Agent.dest == -1:
            # print(findArr[1])
            for next_node in findArr[1]:

                client.choose_next_edge(
                    '{"agent_id":' + str(findArr[0].id) + ', "next_node_id":' + str(next_node) + '}')

        elif Agent.src == edge.src and Agent.dest == edge.dest:
            algo.graph.pokemons.remove(pok)
            # print(algo.graph.agents)
    client.move()



            # print(algo.graph.pokemons)



    ttl = client.time_to_end()
    print(ttl, client.get_info())
    # print(algo.graph.pokemons)
