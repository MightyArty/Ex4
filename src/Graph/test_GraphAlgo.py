from unittest import TestCase
from GraphAlgo import *

graph = GraphAlgo()
file = r"/Users/david/Desktop/Ex3-new/data/A5.json"  # Enter your path here


class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        e = graph.graph
        self.assertTrue(e, graph.get_graph())

    def test_load_from_json(self):
        e = graph.load_from_json(file)
        actual = graph.get_graph()
        self.assertTrue(e, actual)

    def test_save_to_json(self):
        e = graph.load_from_json(file)
        save = graph.save_to_json("testUnit.json")  # name of the output file
        self.assertTrue(e, save)

    def test_shortest_path(self):
        graph.load_from_json(file)
        short = graph.shortest_path(0, 5)
        self.assertEqual(short[1],[0, 0, 2, 3, 5])

    def test_tsp(self):
        graph.load_from_json(file)
        test = graph.TSP([1, 3, 7])
        self.assertEqual(test[0], [0, 1, 9, 3, 2, 13, 7])

    def test_center_point(self):
        graph.load_from_json(file)
        center = graph.centerPoint()
        self.assertEqual(9.291743173960954, center[1])
        self.assertEqual(40,center[0])

    def test_plot_graph(self):
        graph.load_from_json(file)
        graph.plot_graph()
