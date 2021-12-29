from unittest import TestCase
from DiGraph import *

graph = DiGraph()
a = (1, 2, 0)
b = (2, 4, 0)
c = (6, 3, 0)
graph.add_node(0, a)
graph.add_node(1, b)
graph.add_node(2, c)
graph.add_edge(0, 1, 5)  # one edge 2 -- 4


class TestDiGraph(TestCase):
    def test_v_size(self):
        a = graph.v_size()
        self.assertEqual(2,a)
        tempTuple = (9, 9, 0)
        graph.add_node(10, tempTuple)
        a2 = graph.v_size()
        self.assertEqual(3,a2)

    def test_e_size(self):
        a = graph.e_size()
        self.assertEqual(2,a)
        graph.add_edge(2,1,0)
        a2 = graph.e_size()
        self.assertEqual(a2,3)

    def test_get_all_v(self):
        a = graph.get_all_v()
        self.assertEqual(graph.nodesMap, a)

    def test_all_in_edges_of_node(self):
        a = graph.all_in_edges_of_node(1)
        self.assertEqual({0: 5},a)

    def test_all_out_edges_of_node(self):
        a = graph.all_out_edges_of_node(0)
        self.assertEqual({1: 5},a)

    def test_get_mc(self):
        a = graph.get_mc()
        self.assertEqual(a, 7)



    def test_add_edge(self):
        before = graph.e_size()
        graph.add_edge(1, 2, 1)
        e = graph.e_size()
        self.assertNotEqual(before, e)
        flag = graph.add_edge(99, 98, 97).__bool__()  # node ids doesn't exist
        self.assertEqual(flag, False)

    def test_add_node(self):
        before = graph.v_size()  # 3
        temp = (10, 10, 0)
        graph.add_node(4, temp)
        e = graph.v_size()  # 4
        self.assertNotEqual(before, e)
        flagTuple = ()
        flag = graph.add_node(1, flagTuple).__bool__()  # id already exist
        self.assertEqual(flag, False)

    def test_remove_node(self):
        before = graph.v_size()  # 3
        graph.remove_node(2)
        e = graph.v_size()  # 2
        self.assertNotEqual(e, before)
        flag = graph.remove_node(1).__bool__()
        self.assertEqual(flag, True)

    def test_remove_edge(self):
        graph.add_edge(2, 1, 10)
        before = graph.e_size()
        graph.remove_edge(2, 1)
        graph.remove_edge(2, 1)
        e = graph.e_size()  # 0
        self.assertNotEqual(e, before)
        flag = graph.remove_edge(99, 92).__bool__()
        self.assertEqual(flag, False)
