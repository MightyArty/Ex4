 ![GitHub contributors](https://img.shields.io/github/contributors/MightyArty/Ex4?style=plastic) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/MightyArty/Ex4?style=plastic)
# Autores: Artem Shabalin, David Yosopov and Lior Patael


![index](https://user-images.githubusercontent.com/77808208/148431522-dd3d2c56-c675-4c79-a39e-6dbda8880f2f.jpg)



**This is a Pokemon game, which is played on a directed weighted graph**

# Game concept :
In this game we (the agent) need to catch as much pokemons as we can in short amount of time. As much as better :)

The pokemons are spread all over the graph edges, and the agents looking for them untill the game is running.

# We used this algorithms in order to complete the task
- [Graph Center](https://en.wikipedia.org/wiki/Graph_center)
- [Travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
- [Shortest Path Problem](https://en.wikipedia.org/wiki/Shortest_path_problem)
- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Floyd Warshall algorithm](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm)

# Part I - DiGraph class (implements GraphInterface):
 **In this class we have the next functions :**
</br>`v_size()` - return the number of nodes in the graph (|V|)
</br>`e_size()` - return the number of edges in the graph (|E|)
</br>`get_all_v()` - return a dictionary of graph nodes {(node_id : NodeData)}
</br>`all_in_edges_of_node()` - return a dictionary of all the nodes connected to node {(parent_id, weight)}
</br>`all_in_edges_of_node()` - return a dictionary of all the nodes connected from the node {(child_id, weight)}
</br>`get_mc()` - return graph mode count
</br>`add_edge()` - connect between two nodes with weight
</br>`add_node()` - adding node to the graph
</br>`remove_node()` - remove node from the graph and all the connections with other nodes
</br>`remove_edge()` - removing connection between 2 nodes
</br>`get_pokemons()`- return the list of pokemons
</br>`get_agents()` - return the dict() of agents
</br>`add_agent()` - given some agent the function appending this agent (by id) to the dict()
</br>`remove_pokemon()` - given some pokemon the function removing this pokemon from the list

# Part II - GraphAlgo class (implements GraphAlgoInterface):
  **In this class we have the next functions :**
</br>`get_graph()` - return the init graph
</br>`load_from_json()` - save the graph to a json file with the given file name
</br>`save_to_json()` - load the graph from a json file by the give file name
</br>`shortest_path()` - compute the shortest path between to nodes using Dijkstra's algorithm, and return (weight, path)
</br>`TSP()` - Finds the shortest path that visits all the nodes in the list
</br>`centerPoint()` - Finds the node that has the shortest distance to it's farthest node.
</br>`plot_graph()` - plot the graph to a window using matplotlib
</br>`pokemon_to_json` - given string of pokemons, get's all the data of each pokemon and adding it to the list of our pokemons in the graph
</br>`agent_to_json` - given string of agents, get's all the data of each agent and adding it to the dict() of our agents in the graph
</br>`time_to_catch` - calculating the time needed for agent to catch the pokemon
</br>`find_pokemon_edge` - finding the exact edge that the pokemon is located on
</br>`find_agent` - finding the best agent to each given pokemon

# Part III - Pokemon Game:
**In this class we have a several sub-classes :**
</br>`Agent` - contains all the agent info (src,dest,id,speed,pos and value)
</br>`Pokemon` - contains all the pokemon info (value,type and pos)
</br>`Button` - represent the button function for the GUI
</br>`Client` - all the game info (port,ip...) and dealing with the actual connetion to the server of the game
</br>`Game` - the actual implementation of all the classes together to perfectly working algorithm of the Pokemon Game 

# GUI - using pygame:
![case 2](https://serving.photos.photobox.com/157897008105496e997fa0809c055be006eb6501179b00896346f6f8636ef1632604a81a.jpg)
