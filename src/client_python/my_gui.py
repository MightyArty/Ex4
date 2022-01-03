import pygame
from pygame import *
import json
from client import Client
from src.Graph.GraphAlgo import GraphAlgo
from Pokemon import Pokemon

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
g = GraphAlgo()  # our algo of the graph
g.load_from_json(graph_json)  # our load from json
myGraph = g.get_graph()
pokemons_json = client.get_pokemons()
g.pokemons_from_json(pokemons_json)
client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this command starts the server - the game is running now
client.start()

while client.is_running() == 'true':
    # pokemons from json
    pokemons_json = client.get_pokemons()
    g.pokemons_from_json(pokemons_json)
    # agents from json
    agents_json = client.get_agents()
    g.agent_from_json(agents_json)


