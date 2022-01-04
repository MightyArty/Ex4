import pygame
from pygame import *
import json
from client import Client
from src.Graph.GraphAlgo import GraphAlgo
from src.Graph.DiGraph import DiGraph
from Pokemon import Pokemon
from src.client_python.student_code import my_scale

WIDTH, HEIGHT = 1080, 720
PORT = 6666
HOST = '127,0,0,1'

pygame.init()
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)
client = Client()
client.start_connection(HOST, PORT)
graph_json = client.get_graph()
algo = GraphAlgo()  # our algo of the graph
algo.load_from_json(graph_json)  # our load from json
myGraph = algo.get_graph()
pokemons_json = client.get_pokemons()
algo.pokemons_from_json(pokemons_json)
client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this command starts the server - the game is running now
client.start()

while client.is_running() == 'true':
    # pokemons from json
    pokemons_json = client.get_pokemons()
    algo.pokemons_from_json(pokemons_json)
    # agents from json
    agents_json = client.get_agents()
    algo.agent_from_json(agents_json)
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # draw agents
    for agent in algo.graph.agents:
        X, Y, Z = agent.get_pos()
        X = my_scale(X, x=True)
        Y = my_scale(Y, y=True)

    # draw pokemons
    for pokemon in algo.graph.pokemons:
        X, Y, Z = pokemon.get_pos()
        X = my_scale(X, x=True)
        Y = my_scale(Y, y=True)


    for a in algo.graph.agents:
        if a.dest == -1:
            next = (a.src - 1) % algo.get_graph().v_size()
            client.choose_next_edge('{"agent_id":' + str(a.id) + ', "next_node_id":' + str(next) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
            print(myGraph.pokoemons)
    client.move()
