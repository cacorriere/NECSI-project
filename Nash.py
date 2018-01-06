# coding: utf-8
from numpy import *


class Agent(object):

    def __init__(self, label, trust_level=0.5, strategy=""):
        self.score = 0
        self.trust_level = trust_level
        self.label = str(label)
        self.strategy = strategy
        self.games_played = 0

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label




class Game:

    def __init__(self, agent1=Agent("Alice"), agent2=Agent("Bob"), label="Alice vs Bob"):
        self.agentA = agent1
        self.agentB = agent2
        self.inclusive_cooperate = 1
        self.inclusive_defect = 3
        self.exclusive_defect = 0
        self.exclusive_cooperate = 5
        self.label = str(label)
        self.choices = ['defect', 'cooperate']
        self.agentA.strategy = random.choice(self.choices, 1, p=[self.agentA.trust_level, 1 - self.agentA.trust_level])[0]
        self.agentB.strategy = random.choice(self.choices, 1, p=[self.agentB.trust_level, 1 - self.agentB.trust_level])[0]


    def __str__(self):
            return self.label

    def __repr__(self):
            return self.label

    # to update the game is to play a round
    def play(self):

        if self.agentA.strategy == self.agentB.strategy == 'defect':
            print self.agentA.label + " and " + self.agentB.label + " defected and scored " + str(self.inclusive_defect)
            self.agentA.score += self.inclusive_defect
            self.agentB.score += self.inclusive_defect

        if self.agentA.strategy == self.agentB.strategy == 'cooperate':
            print self.agentA.label + " and " + self.agentB.label + " cooperated and scored " + str(self.inclusive_cooperate)
            self.agentA.score += self.inclusive_cooperate
            self.agentB.score += self.inclusive_cooperate

        if self.agentA.strategy != self.agentB.strategy and self.agentA.strategy == 'cooperate':
            print self.agentA.label + " scored " + str(self.exclusive_cooperate) + " with " + self.agentA.strategy + " and " + self.agentB.label + " scored " + str(self.exclusive_defect) + " with " + self.agentB.strategy
            self.agentA.score += self.exclusive_cooperate
            self.agentB.score += self.exclusive_defect

        if self.agentA.strategy != self.agentB.strategy and self.agentA.strategy == 'defect':
            print self.agentA.label + " scored " + str(self.exclusive_defect) + " with " + self.agentA.strategy + " and " + self.agentB.label + " scored " + str(self.exclusive_cooperate) + " with " + self.agentB.strategy
            self.agentA.score += self.exclusive_defect
            self.agentB.score += self.exclusive_cooperate

    def get_scores(self):
        print self.agentA.label + " has " + str(self.agentA.score) + " points."
        print self.agentB.label + " has " + str(self.agentB.score) + " points."
