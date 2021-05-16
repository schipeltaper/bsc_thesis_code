# In this document I re-create a simplified version of the VFD algorithm from the
# paper bij Martijn Onderwater.

from main import *
from generate_sample import *
from run_vfd import *

import random
import math

# number of sample point sets
Q = 10

# Limit state space TODO
L = 14

# how accurate do we want value iteration to be?
epsilon = 0.000001

# this times two is the amount of sample points we take from each MDP
half_sample_size = 10

def VFD_algorithm(L, Q, epsilon, half_sample_size):
    # create empty doc
    # To create a new sample set. uncomment the following, and change the filename in run_vfd.py accordingly
    # open('sample_points.txt', 'w').close()

    # repeats Q times: generate random parameters and apply value iteration and save results of few points.
    # For each of the iterations, we save points in the form of: (s, V(s)), where s is the state, and V(s)
    # the outcome of the value iteration function.
    generate_sample(L, Q, epsilon, half_sample_size)

    print(run_vfd(Q, L, half_sample_size))


VFD_algorithm(L, Q, epsilon, half_sample_size)
