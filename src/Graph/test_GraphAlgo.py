import json
from unittest import TestCase
from GraphAlgo import *
import os
from src.PokemonGame.client import Client
from src.Graph.Edge import Edge
from src.PokemonGame.Agent import *

algo = GraphAlgo()
file = os.path.join(os.path.curdir, "A0")
client = Client()

 
class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        e = algo.graph
        self.assertTrue(e, algo.get_graph())

    def test_load_from_json(self):
        e = algo.load_from_json(file)
        actual = algo.get_graph()
        self.assertTrue(e, actual)

    def test_save_to_json(self):
        e = algo.load_from_json(file)
        save = algo.save_to_json("testUnit.json")  # name of the output file
        self.assertTrue(e, save)

    def test_shortest_path(self):
        algo.load_from_json(file)
        short = algo.shortest_path(0, 5)
        self.assertEqual(short[1], [0, 1, 2, 3, 4, 5])

    def test_find_pokemon_edge(self):
        algo.load_from_json(file)
        value = 5
        type = -1
        pos: tuple = (35.20319591121872, 32.1031462, 0.0)
        pok = Pokemon(value, type, pos)
        algo.graph.add_pokemon(pok)
        e = algo.find_pokemon_edge(pok)
        a = Edge(8, 7, 1.6449953452844968)
        self.assertEqual(a.__str__(), e.__str__())

    def test_time_to_catch(self):
        pos = (35.197656770719604, 32.10191878639921, 0.0)
        agent = Agent(1, 2.0, 1, 2, 1, pos)
        speed = agent.speed
        ansTest = algo.time_to_catch(speed, 0, 5)
        self.assertTrue(True, ansTest)

    def test_find_agent(self):
        pos = (35.197656770719604, 32.10191878639921, 0.0)
        pok = Pokemon(1, -1, pos)
        e = algo.find_agent(pok)
        self.assertTrue(e, True)

    def test_agent_to_json(self):
        ag1 = Agent(5, 5, 1, 8, 2, (35.197656770719604, 32.10191878639921, 0.0))
        ag2 = Agent(2, 1, 7, 3, 1, ((35.20319591121872, 32.1031462, 0.0)))
        agDict = {ag1, ag2}
        self.assertTrue(agDict, True)

    def test_pokemon_to_json(self):
        pok1 = (35.197656770719604, 32.10191878639921, 0.0)
        pok2 = (35.20319591121872, 32.1031462, 0.0)
        pokDict = {pok1, pok2}
        self.assertTrue(pokDict, True)
