import client
from src.Graph import DiGraph, Edge
from src.Graph.GraphAlgo import GraphAlgo

pokemons = {}
agents = {}
algo = GraphAlgo()


def startPos() -> list:
    ans = list
    for p in pokemons:
        for Dict in algo.graph.edgesMap().values():
            for edge in Dict.values():
                srcPos = algo.graph.nodesMap[edge.src].pos
                destPos = algo.graph.nodesMap[edge.dest].pos
                if p.isOn(srcPos[0], srcPos[1], destPos[0], destPos[1]):
                    ans.append(edge)
    return ans


def allocateAgents():
    pokEdges = startPos()
    # compares the length of agents to pokemons
    if len(agents) >= len(pokemons):
        # setting the agents to be on the edge's pokemon src
        for index in range(len(pokEdges)):
            pokSrc = pokEdges[index].src
            pokDest = pokEdges[index].dest
            agents[index].set_src(algo.graph.nodesMap[pokSrc].src)
            agents[index].set_dest(algo.graph.nodesMap[pokDest].dest)
            agents[index].set_pos(pokEdges[index].pos)
        center = algo.centerPoint()
        index = len(pokEdges)
        # deals with the leftover agents
        while index < len(agents):
            agents[index].setPos = algo.graph.nodesMap[center[0]].pos
            agents[index].setSrc = center[0]
            index += 1
    else:



while client.is_running() == 'true':
