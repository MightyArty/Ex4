from asyncio import PriorityQueue

import client
from src.Graph.GraphAlgo import GraphAlgo

pokemons = {}
agents = {}
algo = GraphAlgo()


def startPos() -> list:
    ans = list
    sizeOfDup = {}
    pq = PriorityQueue()
    for p in pokemons:
        for Dict in algo.graph.edgesMap().values():
            for edge in Dict.values():
                srcPos = algo.graph.nodesMap[edge.src].pos
                destPos = algo.graph.nodesMap[edge.dest].pos
                if p.isOn(srcPos[0], srcPos[1], destPos[0], destPos[1]):
                    ans.append(edge)
                    if sizeOfDup[edge] is None:
                        sizeOfDup[edge] = 1
                        pq.put(1, edge)
                    else:
                        pq.get()
                        size = sizeOfDup[edge] + 1
                        sizeOfDup[edge] = size
                        num = sizeOfDup[edge]
                        pq.put(num * (-1), edge)

    return ans, pq


def allocateAgents():
    allocate = startPos()
    pokEdges = allocate[0]
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
        pq = allocate[1]


while client.is_running() == 'true':
    pass