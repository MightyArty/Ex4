 ![GitHub contributors](https://img.shields.io/github/contributors/MightyArty/Ex4?style=plastic) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/MightyArty/Ex4?style=plastic)
# Autores: Tom Shabalin, David Yosopov and Lior Patael


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
</br>`load_json` - save the graph to a json file with the given file name
</br>`save_to_json()` - load the graph from a json file by the give file name
</br>`shortest_path()` - compute the shortest path between to nodes using Dijkstra's algorithm, and return (weight, path)
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

# GUI - short video :
**Click below to see a short video of our game**

[![CLICK HERE](https://user-images.githubusercontent.com/77808208/148528228-bcf6f8c9-d14f-4f49-8a19-5e77dab86879.png)](https://youtu.be/c6eJEzhy5GY "CLICK HERE")

# Game results:
To see the rueslts please click here --> [Results](https://github.com/MightyArty/Ex4/wiki/Game-results)

# UML Diagram:

![](https://i.ibb.co/3h5pBSG/matala1-1.png)


# How to run the game:
**Clone this repository firsly, open the project and run the following command in the terminal :**
![Screen Shot 2022-01-07 at 12 14 09](https://user-images.githubusercontent.com/77808208/148528949-512f87ed-2c11-46cc-8e68-5df0b0aac91c.png)

The number 10 after the jar line is the case that you would like to run [0-15]



