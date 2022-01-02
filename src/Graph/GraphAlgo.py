import copy
import json
import random
from typing import List

from matplotlib import pyplot as plt
from matplotlib.patches import ConnectionPatch

from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from GraphInterface import GraphInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph: DiGraph = DiGraph()):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        return self.graph

    def copy(self):
        graph = DiGraph()
        for node in self.graph.nodesMap.values():
            graph.add_node(node.id, node.pos)
            for edge in self.graph.all_out_edges_of_node(node.id):
                weight = self.graph.edgesMap[node.id][edge]
                graph.add_edge(node.id, edge, weight)
        return graph

    """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
    """

    def load_from_json(self, file_name: str) -> bool:
        graph = DiGraph()
        Edges: list
        Nodes: list
        try:
            with open(file_name, 'r') as f:
                r = json.load(f)
                Edges = r["Edges"]
                Nodes = r["Nodes"]

                for node in Nodes:
                    try:
                        out = node["pos"].split(',')
                        pos = (float(out[0]), float(out[1]), float(out[2]))
                    except Exception:
                        pointX = random.randint(5, 50)
                        pointY = random.randint(5, 50)
                        pos = (pointX, pointY, 0.0)

                    graph.add_node(node["id"], pos)

                for edge in Edges:
                    graph.add_edge(edge["src"], edge["dest"], edge["w"])
                self.graph = graph
                print("Successfully loaded from json format")
                return True
        except():
            print("Error in loading from json format")
            return False

    """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
    """

    def save_to_json(self, file_name: str) -> bool:
        output = {"Edges": [], "Nodes": []}
        for node in self.graph.nodesMap.values():
            dict1 = {"id": node.id}
            if node.pos is not None:
                dict1["pos"] = node.pos
            output["Nodes"].append(dict1)

            for edge in self.graph.all_out_edges_of_node(node.id):
                dict2 = {"src": node.id, "w": self.graph.all_out_edges_of_node(node.id)[edge], "dest": edge}
                output["Edges"].append(dict2)
        try:
            with open(file_name, "w") as f:
                f.write(json.dumps(output))
                print("Successfully saved to json format")
                return True
        except():
            print("Error in saving to json format")
            return False

    """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Notes:
            If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
            More info:
            https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    """

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        vertexDirection = dict()
        ansArr = list()
        try:
            if self.graph.nodesMap[id1] is None or self.graph.nodesMap[id2] is None or self.graph is None:
                vertexDirection[float('inf')] = []
                return vertexDirection
            if id1 == id2:
                vertexDirection[0] = [id1]
                return vertexDirection
            tempGraph = self.graph
            curr = tempGraph.nodesMap[id1]
            curr.weight = 0
            vertexDirection[id1] = curr
            for n in tempGraph.nodesMap.values():
                tempNode = n
                if tempNode.id != id1:
                    # set the weight, info and the tag
                    tempGraph.nodesMap[tempNode.id].weight = float('inf')
                    tempGraph.nodesMap[tempNode.id].info = "Not Visited"
                    tempGraph.nodesMap[tempNode.id].tag = -1
            curr.info = "Not Visited"
            pq = [curr]
            # starting the dijkstra algo
            while len(pq) != 0:
                if curr.id != id2:
                    tempDict = self.graph.edgesMap[curr.id]
                for e in tempDict.values():
                    if curr.id != e.dest:
                        sumWeight = e.weight + tempGraph.nodesMap[e.src].weight
                        # check if this route is cost less
                        if tempGraph.nodesMap[e.dest].weight > sumWeight:
                            tempGraph.nodesMap[e.dest].weight = sumWeight
                            tempGraph.nodesMap[e.dest].tag = curr.id
                            vertexDirection[e.dest] = curr
                    tempNode = tempGraph.nodesMap[e.dest]
                    if tempNode.info != "Visited":
                        pq.append(tempGraph.nodesMap[e.dest])
                if pq[0] is not None:
                    tempGraph.nodesMap[pq[0].id].info = "Visited"
                    pq.pop(0)
                if len(pq) != 0:
                    curr = pq[0]
            minWeight = tempGraph.nodesMap[id2].weight  # the cheaper route value
            ansArr.append(tempGraph.nodesMap[id2].id)
            index = id2
            # updating the cheaper route list
            while index != id1:
                ansArr.append(vertexDirection[index].tag)
                index = vertexDirection[index].id
            ansArr.reverse()
            return minWeight, ansArr
        except Exception:
            return -1, ansArr

    """
        Finds the shortest path that visits all the nodes in the list
        param: node_lst: A list of nodes id's
        return: A list of the nodes id's in the path, and the overall distance
    """

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        if (node_lst is None) or len(node_lst) < 1:
            print("The list should not be empty !")
            return [], -1

        # if there are only one node in the given list
        # just return this node
        if len(node_lst) == 1:
            return [node_lst, 0]

        output = []
        destination = 0
        tempList = copy.deepcopy(node_lst)  # copy of the given list

        # go from start to the last node of the list and compare
        # each 2 nodes [0,1],[1,2]...[n-1,n]
        for runner in range(0, len(tempList) - 1):
            first = tempList[runner]
            second = tempList[runner + 1]
            currentDist = self.shortest_path(first, second)[1]
            destination = destination + self.shortest_path(first, second)[0]

            for i in currentDist:
                if not output.__contains__(i):
                    output.append(i)
        return output, destination

    def centerPoint(self) -> (int, float):
        size = len(self.graph.nodesMap)
        matrix = []
        # creating a matrix [][]
        for i in range(size):
            a = []
            for j in range(size):
                if i == j:
                    a.append(0)
                else:
                    a.append(float('inf'))
            matrix.append(a)
        # setting the vertexes
        for i in range(size):
            keys = self.graph.all_out_edges_of_node(i).keys()
            for j in range(size):
                if keys.__contains__(j):
                    Edge = self.graph.edgesMap[i]
                    matrix[i][j] = Edge[j].weight
        # updating the matrix according to the FW algo
        for k in range(size):
            for i in range(size):
                for j in range(size):
                    if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                        matrix[i][j] = matrix[i][k] + matrix[k][j]

        id = -1
        minMax = float('inf')
        # finding the minimum from the maximum between all the rows
        for i in range(size):
            max = -1
            for j in range(size):
                if matrix[i][j] > max:
                    max = matrix[i][j]
                if max == float('inf'):
                    return float('inf')
            if minMax > max:
                id = i  # updates the center ID
                minMax = max  # updates center's weight
        return id, minMax

    """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
    """

    def plot_graph(self) -> None:
        # define dimensions of figure and axis

        fig, (ax1) = plt.subplots(figsize=(15, 15))  # set image dimensions

        nodes = self.graph.get_all_v()  # (node_key: int, (x,y,z) :tuple)
        nodes_keys = nodes.keys()
        for i in nodes.values():
            if i.pos is None:
                i.pos = (random.random() * 15, random.random() * 15, 0.0)

        else:

            x_values = [nodes[id].pos[0] for id in nodes_keys]
            y_values = [nodes[id].pos[1] for id in nodes_keys]

        # Construct a set of all class edge
        arrows = set()
        for v in nodes:
            start = (nodes[v].pos[0], nodes[v].pos[1])
            outgoing_edges = self.graph.all_out_edges_of_node(v)

            for e in outgoing_edges.keys():
                weight = outgoing_edges[e]
                dest_id = e

                end_x_value = nodes[dest_id].pos[0]
                end_y_value = nodes[dest_id].pos[1]
                end = (end_x_value, end_y_value)
                coordsA = "data"
                coordsB = "data"
                arrows.add(
                    ConnectionPatch(start, end, coordsA, coordsB, arrowstyle="-|>", shrinkA=5, shrinkB=5, linewidth=2,
                                    color="r", mutation_scale=30))

        # plot the nodes
        plt.scatter(x_values, y_values, color="b", marker="o", s=100 * 2)
        # plot the ids
        for i in nodes:
            plt.text(x_values[i], y_values[i], f'{nodes[i]}', ha='right', fontsize=25)  # add node id
        # plot edges
        for edge in arrows:
            ax1.add_artist(edge)
        plt.tight_layout()
        plt.show()



