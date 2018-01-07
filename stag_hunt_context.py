# coding: utf-8

# In[1]:
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import pycxsimulator
import pprint
import random
import Nash
from matplotlib.colors import ListedColormap
import networkx as nx

# set up animial classes
class Fox(Nash.Agent):

    def __init__(self, x, y):
        self.label = 'f'+str(x)+str(y)
        Nash.Agent.__init__(self, self.label)
        self.fox_neighbors = []
        self.stag_neighbors = 0
        self.rabbit_neighbors = 0
        self.color = 'red'



class Rabbit(object):

    def __init__(self, x, y):
        self.points = 1
        self.label = 'r'+str(x)+str(y)
        self.color = 'white'
        self.type = Rabbit

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


class Stag(object):

    def __init__(self, x, y):
        self.points = 2
        self.label = 's'+str(x)+str(y)
        self.color = 'tan'

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


# size of game board
space_size = 10

# animals in ecosystem and probability of seed
ecosystem = {"r": 0.5, "s": 0.5, "f": 0.5}


def initialize():
    global grid, color_grid, foxes, rabbits, stags, nodes, graph, stag_nodes
    graph = nx.Graph()
    grid = []
    foxes = []
    rabbits = []
    stags = []
    stag_nodes =[]
    color_grid = zeros([space_size, space_size])
    nodes = {}
    # seed gameboard
    for x in range(space_size):
        row = []
        for y in range(space_size):
            # select a random species from ecosystem
            species = random.choice(ecosystem.keys())
            # flip coin to see if species is seeded or cell is empty
            if ecosystem[species] > random.random():
                if species == 'r':
                    rabbit = Rabbit(x,y)
                    color_grid[x][y] = 1
                    nodes['r'+str(x)+str(y)] = (x, y)
                    row.append(rabbit)
                    rabbits.append(rabbit)
                elif species == 's':
                    stag = Stag(x,y)
                    color_grid[x][y] = 2
                    nodes['s'+str(x)+str(y)] = (x, y)
                    row.append(stag)
                    stags.append(stag)

                elif species == 'f':
                    fox = Fox(x, y)
                    color_grid[x][y] = 3
                    nodes['f'+str(x)+str(y)] = (x, y)
                    row.append(fox)
                    foxes.append(fox)
            else:
                row.append(0)
        grid.append(row)
    # print grid
    pprint.pprint(grid)


def observe():
    val_map = {'A': 'pink',
               'D': 'red',
               'H': 'tan'}
    row_labels = range(space_size)
    col_labels = range(space_size)
    cmap = ListedColormap(['white','pink', 'tan', 'red'])
    # nx.draw_networkx_nodes(graph,nodes,
    #                    nodelist=stag_nodes,
    #                    node_color='tan',
    #                    node_size=500,
    #                alpha=0.8)
    nx.draw(graph, with_labels = True, pos = nodes)
    print graph.nodes
    plt.matshow(color_grid, cmap=cmap)
    plt.xticks(range(space_size), col_labels)
    plt.yticks(range(space_size), row_labels)
    plt.show()



def update():
    global grid
    global next_grid
    games_played = []
    for x in range(space_size):
        for y in range(space_size):
            stag_neighbors = 0
            rabbit_neighbors = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    current_species = grid[((x+dx) % space_size)][((y+dy) % space_size)]
                    if(dx, dy) != (0, 0) and type(current_species) != int and type(grid[x][y]) == Fox:
                        if current_species.label.find('f') > -1:
                            grid[x][y].fox_neighbors.append(current_species)
                            graph.add_edge(grid[x][y].label, current_species.label)
                        if current_species.label.find('r') > -1:
                            grid[x][y].rabbit_neighbors += 1
                            graph.add_edge(grid[x][y].label, current_species.label)
                        if current_species.label.find('s') > -1:
                            grid[x][y].stag_neighbors += 1
                            graph.add_edge(grid[x][y].label, current_species.label)
            #print str(x) + ", " + str(y) + " is " +str(grid[x][y]) + " with these neighbors: foxes: " + str(fox_neighbors) + " rabbits: "+ str(rabbit_neighbors) + " stags: "+ str(stag_neighbors)
            if type(grid[x][y]) == Fox and len(grid[x][y].fox_neighbors) > 0:
                for foxB in grid[x][y].fox_neighbors:
                    foxA = grid[x][y]
                    if (foxA, foxB) not in games_played:
                        g = Nash.Game(foxA, foxB)
                        if foxA.stag_neighbors > 0 and foxA.rabbit_neighbors > 0:
                            g.inclusive_cooperate = 5
                            g.inclusive_defect = 3
                            g.exclusive_defect = 0
                            g.exclusive_cooperate = 3
                        elif foxA.stag_neighbors == 0 and foxA.rabbit_neighbors == 0:

                            continue

                        elif foxA.stag_neighbors > 0 and foxA.rabbit_neighbors == 0:
                            g.inclusive_cooperate = 5
                            g.inclusive_defect = 0
                            g.exclusive_defect = 0
                            g.exclusive_cooperate = 0

                        elif foxA.stag_neighbors == 0 and foxA.rabbit_neighbors > 0:
                            g.inclusive_cooperate = 0
                            g.inclusive_defect = 3
                            g.exclusive_defect = 0
                            g.exclusive_cooperate = 3
                        g.play()
                        games_played.append((foxA, foxB))
                        games_played.append((foxB, foxA))
                        foxB.games_played += 1
                        foxA.games_played += 1
                        g.get_scores()



    #         if current_state == 1:
    #             next_grid[x, y] = 1 if random() < sick_neighbors/8. else 0
    #         elif current_state == 2 :
    #             next_grid[x, y] = 1 if random() < 0.5 else 2
    #         else:
    #             next_grid[x, y] = 2 if random() > 0.5 else 3
    # grid, next_grid = next_grid, grid


initialize()
update()
observe()
#pycxsimulator.GUI(title='My Simulator', interval=0,parameterSetters=[]).start(func=[initialize, observe, update])
