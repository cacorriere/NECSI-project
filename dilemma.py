
# coding: utf-8

# In[21]:


#Setting up and importing stuff
from numpy import *
prisoners_choices = ['Defect','Cooperate']
rounds_of_game = 1
Alice_points = 0
Bob_points = 0
#Just defining initializaition
def initialize():
    global Alice, Bob
    Alice = random.choice(prisoners_choices, 1, p=[0.5,0.5])
    Bob = random.choice(prisoners_choices, 1, p=[0.5,0.5])
    
    #This is just a work around for a weird bug that I encountered.
    Alice = " ".join(str(x) for x in Alice)
    Bob = " ".join(str(x) for x in Bob)
    

#Setting up the experiment. Yes, it's structured like a proof by casework/exhaustion, but it's my first 
#working program. Sorry about that!
def experiment():
    if Alice == Bob and Bob in ['Defect']:
        print 'Both Alice and Bob will spend two years in prison.'git
    else:
        if Alice in ['Cooperate'] and Bob in ['Defect']:
            print 'Bob will walk free. Alice is charged with three years.'
        else:
            if Alice == Bob and Bob in ['Cooperate']:
                print 'Alice and Bob will only spend a year in prison.'
            else:
                print 'Alice will walk free. Bob is charged with three years.'


#This is the actual program. 
for t in range(rounds_of_game):  
    initialize()
    print 'Alice chose to ' + Alice.lower() + '.'
    print 'Bob chose to ' + Bob.lower() + '.'
    experiment()
    print '\n'

print "Alice won " + " points."
print "Bob won" + " points."

