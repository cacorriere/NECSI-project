# coding: utf-8

# In[1]:
import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import pycxsimulator
import pprint
import random


# set up animial classes
class Fox:

    def __init__(self, label):
        self.score = 0
        self.trust_level = 0.5
        self.label = str(label)

        def __str__(self):
            return self.label

        def __repr__(self):
            return self.label

    def eat(self, points):
        self.score = self.score+2


class Rabbit:

    def __init__(self, label):
        self.points = 1
        self.label = str(label)

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


class Stag:

    def __init__(self, label):
        self.points = 2
        self.label = str(label)

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


# size of game board
space_size = 10

# animals in ecosystem and probability of seed
ecosystem = {"r": 0.5, "s": 0.5, "f": 0.5}


def initialize():
    global grid, next_grid, foxes, rabbits, stags
    grid = []

    # seed gameboard
    for x in range(space_size):
        row = []
        for y in range(space_size):
            # select a random species from ecosystem
            species = random.choice(ecosystem.keys())
            # flip coin to see if species is seeded or cell is empty
            if ecosystem[species] > random.random():
                if species == 'r':
                    row.append(Rabbit('r'+str(x)+str(y)))
                elif species == 's':
                    row.append(Stag('s'+str(x)+str(y)))
                elif species == 'f':
                    row.append(Fox('f'+str(x)+str(y)))
            else:
                row.append(0)
        grid.append(row)
    # print grid
    pprint.pprint(grid)


def observe():
    imshow(grid, cmap=cm.binary)
    show()


def update():
    global grid
    global next_grid

    for x in range(space_size):
        for y in range(space_size):
            fox_neighbors = 0
            stag_neighbors = 0
            rabbit_neighbors = 0
            for dx in [-1, 0, 1]:
               for dy in [-1, 0, 1]:
                    current_species = grid[((x+dx) % space_size)][((y+dy) % space_size)]
                    if(dx, dy) != (0, 0) and type(current_species) != int:
                        if grid[((x+dx) % space_size)][((y+dy) % space_size)].label.find('f') > -1:
                            fox_neighbors += 1
                        if grid[((x+dx) % space_size)][((y+dy) % space_size)].label.find('r') > -1:
                            rabbit_neighbors += 1
                        if grid[((x+dx) % space_size)][((y+dy) % space_size)].label.find('s') > -1:
                            stag_neighbors += 1
            print str(x) + ", " + str(y) + " is " +str(grid[x][y]) + " with these neighbors: foxes: " + str(fox_neighbors) + " rabbits: "+ str(rabbit_neighbors) + " stags: "+ str(stag_neighbors)



    #         if current_state == 1:
    #             next_grid[x, y] = 1 if random() < sick_neighbors/8. else 0
    #         elif current_state == 2 :
    #             next_grid[x, y] = 1 if random() < 0.5 else 2
    #         else:
    #             next_grid[x, y] = 2 if random() > 0.5 else 3
    # grid, next_grid = next_grid, grid


initialize()
update()
#just calling initial game board for now
#pycxsimulator.GUI(title='My Simulator', interval=0,parameterSetters=[]).start(func=[initialize, observe, update])
