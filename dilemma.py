#Setting up and importing stuff
from numpy import *
prisoners_choices = ['defect','cooperate']
rounds_of_game = 10000

#Starting values for Alice and Bob. It doesn't make much sense to have the
#values be non-zero, unless you want a player to start with a disadvantage.
Alice_points = 0
Bob_points = 0

#Trust settings are basically the percentage that the player will choose 
#cooperate.
Alice_trust = 0.5
Bob_trust = 0.5

#Note that in the following variables, the higher the number, the more severe 
#the punishment.
both_cooperate_punishment = 1
both_defect_punishment = 3
victor_defect_punishment = 0
sucker_cooperate_punishment = 5


#Just defining initializaition
def initialize():
    global Alice, Bob, Alice_trust, Bob_trust
    Alice = random.choice(prisoners_choices, 1, p=[Alice_trust,1 - Alice_trust])
    Bob = random.choice(prisoners_choices, 1, p=[Alice_trust,1 - Alice_trust])
    
    #This is just a work around for a weird bug that I encountered.
    Alice = " ".join(str(x) for x in Alice)
    Bob = " ".join(str(x) for x in Bob)
    

#Setting up the experiment. Yes, it's structured like a proof by 
#casework/exhaustion, but it's my first working program. Sorry about that!
def experiment():
    global Alice, Bob, Alice_points, Bob_points
    if Alice == Bob and Bob in ['defect']:
        print 'Both Alice and Bob will spend ' +  str(both_defect_punishment) + ' years in prison.'
        Alice_points = Alice_points + both_defect_punishment
        Bob_points = Bob_points + both_defect_punishment
    else:
        if Alice in ['cooperate'] and Bob in ['defect']:
            print 'Bob will spend ' + str(victor_defect_punishment) + ' years in prison. Alice will spend ' + str(sucker_cooperate_punishment) + ' years in prison.'
            Alice_points = Alice_points + sucker_cooperate_punishment
            Bob_points = Bob_points + victor_defect_punishment
        else:
            if Alice == Bob and Bob in ['cooperate']:
                print 'Alice and Bob will only spend ' + str(both_cooperate_punishment) + ' years in prison.'
                Alice_points = Alice_points + both_cooperate_punishment
                Bob_points = Bob_points + both_cooperate_punishment
            else:
                print 'Alice will spend ' + str(victor_defect_punishment) + ' years in prison. Bob will spend ' + str(sucker_cooperate_punishment) + ' years in prison.'
                Bob_points = Bob_points + sucker_cooperate_punishment
                Alice_points = Alice_points + victor_defect_punishment


#This is the actual program. 
for t in range(rounds_of_game):  
    initialize()
    print 'Alice chose to ' + Alice.lower() + '.'
    print 'Bob chose to ' + Bob.lower() + '.'
    experiment()
    print '\n'

print "Alice won " + str(Alice_points) + " points."
print "Bob won " + str(Bob_points) + " points."

