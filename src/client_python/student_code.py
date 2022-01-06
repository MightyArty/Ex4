import sys
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
import math
from Button import Button
import json

from src.Graph.GraphAlgo import GraphAlgo

WIDTH, HEIGHT = 1080, 720
PORT = 6666

# server host (default localhost 127.0.0.1)
HOST = "127.0.0.1"

radius = 15

# Images for the GUI
agent_img = pygame.image.load("../../../../Downloads/testP/assets/agent.png")
pokemon_img = pygame.image.load("../../../../Downloads/testP/assets/pokemon1.png")
pokemon_2_img = pygame.image.load("../../../../Downloads/testP/assets/pokemon2.png")
quit_img = pygame.image.load("../../../../Downloads/testP/assets/quit.png")

quit_button = Button(0, 0, quit_img)


# Draw the agent
def draw_agent(screen, x, y, id):
    agent_shift_height = 62 / 2
    agent_shift_width = 102 / 2
    screen.blit(agent_img, (x - agent_shift_width, y - agent_shift_height))
    id_display = FONT.render(
        f"Id: {id}", True, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0)
    )
    rect = id_display.get_rect(
        center=(x - agent_shift_width / 2, y - agent_shift_height * 2)
    )
    screen.blit(id_display, rect)


# Draw the first pokemon
def draw_pokemon(screen, x, y, value, FONT):
    pokemon_shift_height = 44 / 2
    pokemon_shift_width = 44 / 2
    screen.blit(pokemon_img, (x - pokemon_shift_width, y - pokemon_shift_height))
    value_display = FONT.render(
        f"Value: {value}", True, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0)
    )
    rect = value_display.get_rect(
        center=(x - pokemon_shift_width / 2, y - pokemon_shift_height * 2)
    )
    screen.blit(value_display, rect)


# Draw the second pokemon
def draw_pokemon_2(screen, x, y, value, FONT):
    pokemon_shift_height = 48 / 2
    pokemon_shift_width = 44 / 2
    screen.blit(pokemon_2_img, (x - pokemon_shift_width, y - pokemon_shift_height))

    value_display = FONT.render(
        f"Value: {value}", True, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0)
    )
    rect = value_display.get_rect(
        center=(x - pokemon_shift_width / 2, y - pokemon_shift_height * 2)
    )
    screen.blit(value_display, rect)


def find_slope(start, end):
    return (end[1] - start[1]) / (end[0] - start[0])


def move_arrow_up(start, end):
    slope = find_slope(start, end)
    m = -1 / slope
    l = 5
    return (
        (
            start[0] + l * math.sqrt(1 / (1 + math.pow(m, 2))),
            start[1] + m * l * math.sqrt(1 / (1 + math.pow(m, 2))),
        ),
        (
            end[0] + l * math.sqrt(1 / (1 + math.pow(m, 2))),
            end[1] + m * l * math.sqrt(1 / (1 + math.pow(m, 2))),
        ),
    )


def distance(start, end):
    return math.sqrt(math.pow(end[0] - start[0], 2) + math.pow(end[1] - start[1], 2))


def move_arrow_down(start, end):
    slope = find_slope(start, end)
    m = -1 / slope
    l = 5
    return (
        (
            start[0] - l * math.sqrt(1 / (1 + math.pow(m, 2))),
            start[1] - m * l * math.sqrt(1 / (1 + math.pow(m, 2))),
        ),
        (
            end[0] - l * math.sqrt(1 / (1 + math.pow(m, 2))),
            end[1] - m * l * math.sqrt(1 / (1 + math.pow(m, 2))),
        ),
    )


def draw_arrow(screen, colour, start, end, isForward):
    if isForward:
        start, end = move_arrow_down(start, end)
    else:
        start, end = move_arrow_up(start, end)
    d = distance(start, end)
    t1 = radius / d
    pos_x1 = (1 - t1) * start[0] + (t1) * end[0]
    pos_y1 = (1 - t1) * start[1] + t1 * end[1]
    t2 = 0.96 - radius / d
    pos_x2 = (1 - t2) * start[0] + (t2) * end[0]
    pos_y2 = (1 - t2) * start[1] + t2 * end[1]
    pygame.draw.line(screen, colour, (pos_x1, pos_y1), (pos_x2, pos_y2), 2)
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pygame.draw.polygon(
        screen,
        colour,
        (
            (
                pos_x2 + 10 * math.sin(math.radians(rotation)),
                pos_y2 + 10 * math.cos(math.radians(rotation)),
            ),
            (
                pos_x2 + 10 * math.sin(math.radians(rotation - 120)),
                pos_y2 + 10 * math.cos(math.radians(rotation - 120)),
            ),
            (
                pos_x2 + 10 * math.sin(math.radians(rotation + 120)),
                pos_y2 + 10 * math.cos(math.radians(rotation + 120)),
            ),
        ),
    )


# init pygame


pygame.init()

original_screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    depth=32,
    flags=pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE,
)
screen = original_screen.copy()

clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 20, bold=True)
client = Client()
client.start_connection(HOST, PORT)

algo = GraphAlgo()
ob = json.loads(client.get_graph())
algo.load_graph(ob)

min_x = sys.float_info.max
min_y = sys.float_info.max
max_x = sys.float_info.min
max_y = sys.float_info.min

# get data proportions
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


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (
            max_screen - min_screen
    ) + min_screen


# decorate scale with the correct values
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


amount_of_agents = int(json.loads(client.get_info())["GameServer"]["agents"])
for ag in range(amount_of_agents):
    client.add_agent("{\"id\":" + str(ag) + "}")

pokOb = json.loads(client.get_pokemons())
agOb = json.loads(client.get_agents())

algo.agent_from_json(agOb)
algo.pokemons_from_json(pokOb)

client.start()
sizeOfPokemons = len(algo.graph.pokemons)
while client.is_running() == "true":
    agOb = json.loads(client.get_agents())
    algo.agent_from_json(agOb)
    if len(algo.graph.pokemons) != sizeOfPokemons:
        pkOb = json.loads(client.get_pokemons())
        algo.pokemons_from_json(pkOb)
        print(algo.graph.pokemons)
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

        gfxdraw.filled_circle(screen, int(x), int(y), radius, pygame.Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y), radius, pygame.Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(node.id), True, pygame.Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

        # draw edges
        for e in algo.get_graph().all_out_edges_of_node(node.id).keys():
            print(e)
            src = node.id
            dest = e
            isForward = dest > src
            color = pygame.Color(239, 71, 111) if isForward else pygame.Color(6, 214, 160)

            # find the edge nodes


            # scaled positions
            src_x, src_y, src_z = algo.graph.get_all_v()[src].get_pos()
            dest_x, dest_y, dest_z = algo.graph.get_all_v()[dest].get_pos()
            sx = my_scale(src_x, x=True)
            sy = my_scale(src_y, y=True)
            dx = my_scale(dest_x, x=True)
            dy = my_scale(dest_y, y=True)

            draw_arrow(
                screen, color, (sx, sy), (dx, dy), isForward,
            )

    # draw agents
    for agent in algo.graph.agents.values():
        x_, y_, z_ = agent.get_pos()
        x = my_scale(x_, x=True)
        y = my_scale(y_, y=True)
        pygame.draw.circle(screen, pygame.Color(122, 61, 23),
                           (int(x), int(y)), 10)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in algo.graph.pokemons:
        x_, y_, z_ = p.get_pos()
        x = my_scale(x_, x=True)
        y = my_scale(y_, y=True)
        if p.type < 0:
            draw_pokemon(screen, int(x), int(y), int(p.value), FONT)
        else:
            draw_pokemon_2(screen, int(x), int(y), int(p.value), FONT)

    if quit_button.draw(screen):
        client.stop()
        pygame.quit()
        exit(0)

    ttl = client.time_to_end()
    info = json.loads(client.get_info())

    ttl_display = FONT.render(f"Time left: {str(int(ttl) // 1000)}", 1, (255, 255, 255))
    moves_display = FONT.render(
        f"Moves: {str(info['GameServer']['moves'])}", 1, (255, 255, 255)
    )
    points_display = FONT.render(
        f"Points: {str(info['GameServer']['grade'])}", 1, (255, 255, 255)
    )

    screen.blit(ttl_display, (5, 50))
    screen.blit(moves_display, (5, 80))
    screen.blit(points_display, (5, 110))
    original_screen.blit(
        pygame.transform.scale(screen, original_screen.get_rect().size), (0, 0)
    )

    # update screen changes
    pygame.display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    for pok in algo.graph.pokemons:
        findArr = algo.find_agent(pok)
        Agent = findArr[0]
        edge = findArr[2]
        if Agent.dest == -1:
            # print(findArr[1])
            for next_node in findArr[1]:
                client.choose_next_edge(
                    '{"agent_id":' + str(findArr[0].id) + ', "next_node_id":' + str(next_node) + '}')
        elif (Agent.src == edge.src and Agent.dest == edge.dest) or (Agent.src == edge.dest and Agent.dest == edge.src):
            algo.graph.pokemons.remove(pok)

            # print(algo.graph.pokemons)

    client.move()
# game over:
