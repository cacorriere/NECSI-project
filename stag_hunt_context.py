# coding: utf-8

# In[1]:
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import pycxsimulator
import random
import Nash
from matplotlib.colors import ListedColormap
import networkx as nx
from matplotlib import animation

# set up animial classes
class Fox(Nash.Agent):

    def __init__(self, x, y):
        self.label = 'f'+str(x)+str(y)
        Nash.Agent.__init__(self, self.label)
        self.fox_neighbors = []
        self.stag_neighbors = []
        self.rabbit_neighbors = []
        self.color = 'red'
        self.x = x
        self.y = y
        self.games_played =  0
        self.last_score = 0





class Rabbit(object):

    def __init__(self, x, y):
        self.points = 1
        self.label = 'r'+str(x)+str(y)
        self.color = 'pink'
        self.type = Rabbit
        self.x = x
        self.y = y
        self.games_played =  0

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


class Stag(object):

    def __init__(self, x, y):
        self.points = 2
        self.label = 's'+str(x)+str(y)
        self.color = 'tan'
        self.x = x
        self.y = y
        self.games_played =  0

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


# size of game board
space_size = 50

# animals in ecosystem and probability of seed
ecosystem = {"r": 0.002, "s": 0.001, "f": 0.004}

color_map ={'r': 'pink','f': 'red', 's': 'tan'}



def seed_grid():
    print "calling seed_grid"
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
                    nodes[rabbit.label] = (x, y)
                    row.append(rabbit)

                elif species == 's':
                    stag = Stag(x,y)
                    nodes[stag.label] = (x, y)
                    row.append(stag)


                elif species == 'f':
                    fox = Fox(x, y)
                    nodes[fox.label] = (x, y)
                    row.append(fox)

            else:
                row.append(0)
        grid.append(row)


def repopulate_species(x,y):
    #print "calling repopulate_species"
    global grid, next_grid
    # select a random species from ecosystem
    species = random.choice(ecosystem.keys())
    # flip coin to see if species is seeded or cell is empty
    if ecosystem[species] > random.random():
        if species == 'r':
            rabbit = Rabbit(x,y)
            next_grid[x][y] = rabbit
            nodes[rabbit.label] = (x, y)


        elif species == 's':
            stag = Stag(x,y)
            next_grid[x][y] = stag
            nodes[stag.label] = (x, y)


        elif species == 'f':
            fox = Fox(x, y)
            next_grid[x][y] = fox
            nodes[fox.label] = (x, y)

    else:
        next_grid[x][y] = 0




def initialize():
    print "calling initialize"
    global grid, next_grid, nodes, graph, stag_nodes, color_grid, games_played
    graph = nx.Graph()
    grid = []
    games_played = []
    color_grid = zeros([space_size, space_size])

    nodes = {}
    seed_grid()
    get_color_grid()



def animate(i):
    print "calling animate"
    update()
    matrice.set_array(color_grid)

def observe():
    print "calling observe"

    cmap = ListedColormap(['green','pink', 'tan', 'red'])
    values = [color_map.get(''.join([i for i in node if not i.isdigit()]),'white') for node in graph.nodes()]
    pos = nx.spring_layout(graph)
    # nx.draw(graph, node_color=values, with_labels = False, pos = pos, node_size = 10, alpha = 0.3, linewidths= 0)
    fig, ax = plt.subplots()
    global matrice
    matrice = ax.matshow(color_grid, cmap=cmap)


    ani = animation.FuncAnimation(fig, animate,
                                frames=200, interval=500)
    plt.show()

def get_neighbors():
    print "calling get_neighbors"
    global grid
    for x in range(space_size):
        for y in range(space_size):
            current_fox = grid[x][y]
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    current_neighbor = grid[((x+dx) % space_size)][((y+dy) % space_size)]
                    if(dx, dy) != (0, 0) and type(current_neighbor) != int and type(current_fox) == Fox:
                        if current_neighbor.label.find('f') > -1:
                            current_fox.fox_neighbors.append(current_neighbor)
                            graph.add_edge(current_fox.label, current_neighbor.label)
                        if current_neighbor.label.find('r') > -1:
                            current_fox.rabbit_neighbors.append(current_neighbor)
                            graph.add_edge(current_fox.label, current_neighbor.label)
                        if current_neighbor.label.find('s') > -1:
                            current_fox.stag_neighbors.append(current_neighbor)
                            graph.add_edge(current_fox.label, current_neighbor.label)


def play_game():
    print "calling play_game"
    games_played = []
    global grid, next_grid, games_played
    for x in range(space_size):
        for y in range(space_size):
            current_fox = grid[x][y]
            if type(current_fox) != Fox:
                continue
                for foxB in current_fox.fox_neighbors:
                    if (current_fox.stag_neighbors == 0 and current_fox.rabbit_neighbors) > 0:
                        g.inclusive_cooperate = 0
                        g.inclusive_defect = 3
                        g.exclusive_defect = 3
                        g.exclusive_cooperate = 0
                    if  len(current_fox.fox_neighbors) > 0:
                        if current_fox.stag_neighbors == 0 and current_fox.rabbit_neighbors == 0:

                            continue
                        if (current_fox, foxB) not in games_played and current_fox is not foxB:
                            g = Nash.Game(current_fox, foxB)
                            if current_fox.stag_neighbors > 0 and current_fox.rabbit_neighbors > 1:
                                g.inclusive_cooperate = 5
                                g.inclusive_defect = 3
                                g.exclusive_defect = 0
                                g.exclusive_cooperate = 3


                            elif current_fox.stag_neighbors > 0 and current_fox.rabbit_neighbors == 0:
                                g.inclusive_cooperate = 5
                                g.inclusive_defect = 0
                                g.exclusive_defect = 0
                                g.exclusive_cooperate = 0

                            elif current_fox.stag_neighbors == 0 and current_fox.rabbit_neighbors > 1:
                                g.inclusive_cooperate = 0
                                g.inclusive_defect = 3
                                g.exclusive_defect = 0
                                g.exclusive_cooperate = 3



                        current_fox.last_score= current_fox.score
                        foxB.last_score = foxB.score

                        g.play()

                        games_played.append((current_fox, foxB))
                        games_played.append((foxB, current_fox))


def repopulate():
    print "calling repopulate"

    global grid, next_grid, games_played
    next_grid = grid
    preyB = None
    PreyA = None
    for x in range(space_size):
        for y in range(space_size):
            current_species = grid[x][y]
            if current_species == 0:
                repopulate_species(x, y)
                continue
            if type(current_species) is Fox and len(current_species.fox_neighbors) > 0:
                for foxB in current_species.fox_neighbors:
                        if current_species.score == current_species.last_score + 5 and len(current_species.stag_neighbors) > 0:
                            preyA = random.choice(current_species.stag_neighbors)
                            #print "prey A " + str(preyA)
                            next_grid[preyA.x][preyA.y] = 0

                        elif current_species.score == current_species.last_score + 3 and len(current_species.rabbit_neighbors) > 0:
                            preyA = random.choice(current_species.rabbit_neighbors)
                            #print "prey A " + str(preyA)
                            next_grid[preyA.x][preyA.y] = 0



                        if foxB.score == foxB.last_score + 5 and len(foxB.stag_neighbors) > 0:
                            preyB = random.choice(foxB.stag_neighbors)
                            #print "prey B " + str(preyB)
                            repopulate_species(preyB.x, preyB.y)

                        elif foxB.score == foxB.last_score + 3 and len(foxB.rabbit_neighbors) > 0:
                            preyB = random.choice(foxB.rabbit_neighbors)
                            #print "prey B " + str(preyB)
                            repopulate_species(preyB.x, preyB.y)


                if current_species.score > 0:
                    print current_species.label +" " + str(current_species.score)
                if foxB.score > 0:
                    print foxB.label +" " + str(foxB.score)
                foxB.games_played += 1
                current_species.games_played += 1

                if current_species.games_played >= 7:
                    if (current_species.score/current_species.games_played + foxB.score/foxB.games_played) > 3 :
                        if ecosystem['f'] < 0.998:
                            ecosystem['f'] += 0.001
                    else:
                        if ecosystem['f'] > 0.2:
                            ecosystem['f'] -= 0.001
                        color_grid[current_species.x][current_species.y] = 0
                        nodes[current_species.label] = None
                        color_grid[foxB.x][current_species.y] = 0
                        nodes[foxB.label] = None
                        repopulate_species(current_species.x, current_species.y)
                        repopulate_species(foxB.x, foxB.y)
                        current_species = None
                        foxB = None



    grid = next_grid

def update():
    print "calling update"

    get_neighbors()
    play_game()
    repopulate()
    print ecosystem
    get_color_grid()

def get_color_grid():
    print "calling get_color_grid"
    global grid, color_grid
    for x in range(space_size):
        for y in range(space_size):
            if grid[x][y] == 0:
                color_grid[x][y] = 0
            elif grid[x][y].color == 'tan':
                color_grid[x][y] = 2
            elif grid[x][y].color == 'pink':
                color_grid[x][y] = 1
            elif grid[x][y].color == 'red':
                color_grid[x][y] = 3












initialize()
observe()
