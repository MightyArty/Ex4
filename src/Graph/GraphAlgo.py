import copy
import json
import queue
import random
from typing import List

from matplotlib import pyplot as plt
from matplotlib.patches import ConnectionPatch


from src.Graph.GraphAlgoInterface import GraphAlgoInterface
from src.Graph.DiGraph import DiGraph
from src.Graph.GraphInterface import GraphInterface
from src.PokemonGame.Pokemon import Pokemon
from src.PokemonGame.Agent import Agent


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

    def load_graph(self, object: dict):
        graph = DiGraph()
        Edges: list
        Nodes: list
        for node in object['Nodes']:
            out = node["pos"].split(',')
            pos = (float(out[0]), float(out[1]), float(out[2]))
            graph.add_node(node["id"], pos)
        for edge in object['Edges']:
            graph.add_edge(edge["src"], edge["dest"], edge["w"])
        self.graph = graph

    """
    Gets a string of pokemons from client
    And saves it as json
    """
    def pokemon_to_json(self, pokemons: dict) -> list:
        # graph = DiGraph()
        self.graph.pokemons.clear()
        for p in pokemons['Pokemons']:
            value = (p['Pokemon']["value"])

            type = (p['Pokemon']["type"])
            out = p['Pokemon']["pos"].split(',')
            pos = (float(out[0]), float(out[1]), float(out[2]))
            pokemon = Pokemon(value, type, pos)
            self.graph.pokemons.append(pokemon)
        self.__init__(self.graph)

    """
    Gets a string of agents from client
    And saves it to dict()
    """
    def agent_to_json(self, agents: dict) -> dict():
        # graph = DiGraph()
        for a in agents['Agents']:
            id = (a['Agent']["id"])
            value = (a['Agent']["value"])
            src = (a['Agent']["src"])
            dest = (a['Agent']["dest"])
            speed = (a['Agent']["speed"])
            try:
                out = (a['Agent']["pos"].split(','))
                pos = (float(out[0]), float(out[1]), float(out[2]))
            except Exception:
                pointX = random.randint(5, 50)
                pointY = random.randint(5, 50)
                pos = (pointX, pointY, 0.0)
            agent = Agent(id, value, src, dest, speed, pos)
            self.graph.add_agent(agent)
        self.__init__(self.graph)

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
                ansArr.append(vertexDirection[index].id)
                index = vertexDirection[index].id
            # ansArr.pop()
            ansArr.reverse()
            return minWeight, ansArr
        except Exception:
            return -1, ansArr

    """
    Calculating the time that takes for the agent to catch the pokemon
    @:param agent, src of the pokemon
    @:return the best time and list of shortest path
    """

    def time_to_catch(self, speed, src, srcPok: int) -> float and list:
        path = self.shortest_path(src, srcPok)
        distance = path[0]
        arr = path[1]
        # speed = agent.speed
        return float(distance / speed), arr

    """
    Allocating the pokemon (only if the pokemon is on some edge)
    @:param pokemon
    @:return edge
    """

    def find_pokemon_edge(self, pokemon: Pokemon):
        for edge in self.graph.edgesMap.values():
            for runner in edge.values():
                srcPos = self.graph.nodesMap[runner.src].pos
                destPos = self.graph.nodesMap[runner.dest].pos
                if pokemon.isOn(srcPos[0], srcPos[1], destPos[0], destPos[1]):
                    if pokemon.type == -1:

                        temp = self.graph.edgesMap[runner.dest]
                        runner = temp[runner.src]
                    else:
                        temp = self.graph.edgesMap[runner.src]
                        runner = temp[runner.dest]
                    return runner

    """
    Finding the best agent for each pokemon
    @:param pokemon
    @:return time and list of nodes to visit
    """

    def find_agent(self, pokemon: Pokemon):
        out = list
        arr = self.graph.agents
        minimum = float('inf')
        temp = None
        edge = self.find_pokemon_edge(pokemon)
        # print(edge)
        for agent in arr.values():
            if agent.src == edge.dest:
                time = self.time_to_catch(agent.speed, edge.src, edge.dest)
            else:
                time = self.time_to_catch(agent.speed, agent.src, edge.dest)
            real_time = time[0]
            if real_time < minimum:
                minimum = real_time
                temp = agent
                out = time[1]
                out.append(edge.dest)
        return temp, out, edge
