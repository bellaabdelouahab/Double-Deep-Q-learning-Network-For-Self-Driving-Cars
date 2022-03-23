import time
from matplotlib import pyplot as plt
import numpy as np
import math
def computeTicks (x):
    step=len(x)//25
    if step==0:
        step=1
    xMax, xMin = math.ceil(max(x)), math.floor(min(x))
    dMax, dMin = xMax + abs((xMax % step) - step) + (step if (xMax % step != 0) else 0), xMin - abs((xMin % step))
    return range(dMin, dMax, step)

import time
def draw_graphe(x,ShowGraphe=False):
    if len(x) == 0: return
    plt.figure(figsize=(12,4),facecolor="grey")
    accuren=sum([ x[i+1]-x[i] for i in range(0,len(x)-1)])/(len(x)-1)
    xis=[i for i in range(len(x))]
    plt.plot(xis,x)
    plt.gca().set_facecolor("grey")
    plt.xticks(computeTicks(xis))
    plt.ylabel("Score")
    plt.xlabel("Episodes")
    plt.title("Learnin gRate :{}".format(accuren))
    plt.savefig("./last_learning_rate_graph"+str(time.localtime)+".jpg")
    if ShowGraphe:
        plt.show()