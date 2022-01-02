from Edge import Edge
from GraphInterface import GraphInterface
from Node import Node


class DiGraph(GraphInterface):

    def __init__(self):
        self.vertexSize = 0
        self.edgeSize = 0
        self.mc = 0
        self.edgesMap = dict()
        self.reversEdges = dict()
        self.nodesMap = dict()

    def v_size(self) -> int:
        return len(self.nodesMap)

    def e_size(self) -> int:
        return self.edgeSize

    def get_all_v(self) -> dict:
        return self.nodesMap

    def all_in_edges_of_node(self, id1: int) -> dict:
        nodes = dict()
        temp1 = self.reversEdges[id1]
        for e in temp1.values():
            nodes[e.src] = e.weight
        return nodes

    def all_out_edges_of_node(self, id1: int) -> dict:
        nodes = dict()

        if id1 not in self.edgesMap:
            # in the case there are no edges going out of id1
            return dict()

        nodeEdges = self.edgesMap[id1]
        for e in nodeEdges.values():
            nodes[e.dest] = e.weight
        return nodes

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        # if the nodes is even exists
        if self.nodesMap.__contains__(id1) and self.nodesMap.__contains__(id2):
            e = Edge(id1, id2, weight)
            destMap = self.edgesMap.get(id1)
            # if it's the first edge that connect from this vertex
            if destMap is None:
                destMap = dict()
                destMap[id2] = e
                self.edgesMap[id1] = destMap
                reversTemp = dict()
                reversTemp[id1] = e
                self.reversEdges[id2] = reversTemp
                self.edgeSize += 1
                self.mc += 1
                return True
            # check if the edge is not already exsist
            elif not destMap.__contains__(id2):
                tempHas = self.edgesMap[id1]
                tempHas[id2] = e
                self.edgesMap[id1] = tempHas
                # updating the the reversEdge according to his keys
                if not self.reversEdges.__contains__(id2):
                    reverseTemp = dict()
                    reverseTemp[id1] = e
                    self.reversEdges[id2] = reverseTemp
                else:
                    reverseTemp = self.reversEdges[id2]
                    reverseTemp[id1] = e
                    self.reversEdges[id2] = reverseTemp
                self.edgeSize += 1
                self.mc += 1
                return True
        else:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        node = Node(node_id, pos)
        # check if the vertex is elready exsist
        if not self.nodesMap.__contains__(node_id):
            self.nodesMap[node_id] = node
            self.mc += 1
            self.vertexSize += 1
            return True
        else:
            return False

    def remove_node(self, node_id: int) -> bool:
        # check if the vertex even exsist
        if self.nodesMap.__contains__(node_id):
            # self.nodesMap.pop(node_id)
            self.mc += 1
            self.vertexSize -= 1
            # check if there any edges that connect to this vertex
            if self.edgesMap.__contains__(node_id):
                self.edgeSize = self.edgeSize - len(self.edgesMap.get(node_id))
                self.mc += len(self.edgesMap.get(node_id))
                Dict = self.edgesMap.pop(node_id)
                for e in Dict.values():
                    self.reversEdges.pop(e.dest)
            if self.reversEdges.__contains__(node_id):
                self.edgeSize = self.edgeSize - len((self.reversEdges.get(node_id)))
                self.mc += len((self.reversEdges.get(node_id)))
                Dict = self.reversEdges.pop(node_id)
                for e in Dict.values():
                    self.edgesMap.pop(e.src)
            self.nodesMap.pop(node_id)
            return True
        else:
            return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        # check if the vertexes are exists
        if self.nodesMap.__contains__(node_id1) and self.nodesMap.__contains__(node_id2):
            tempMap = self.edgesMap.get(node_id1)
            # check if the edge is even exists
            if tempMap is not None:
                if len(tempMap) != 0:
                    tempMap.pop(node_id2)
                    self.edgesMap[node_id1] = tempMap
                    reversedTempMap = self.reversEdges.get(node_id2)
                    reversedTempMap.pop(node_id1)
                    self.reversEdges[node_id2] = reversedTempMap
                    self.edgeSize -= 1
                    self.mc += 1
                else:
                    self.edgesMap.pop(node_id1)
            return True
        else:
            return False

    def __str__(self):
        return str({self.nodesMap.values()})

    def __repr__(self):
        return f"The graph: {self.nodesMap.values()}"
