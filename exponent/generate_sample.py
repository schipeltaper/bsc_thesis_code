from main import *

import random
import math

# create a random parameter combination and save the results from value iteration into a text file
# L is the maximum queue size, Q is the amount of parameter combinations that we will look at
# Epsilon determines when we stop the value iteration function and half_sample_size indicates how many
# states we take to put in our sample set.
def generate_sample(L, Q, epsilon, half_sample_size):
    for i in range(Q):
        # Generate random values for each of the parameters
        temp1 = random.uniform(0, 1)
        temp2 = random.uniform(0, 1)
        temp3 = random.uniform(0, 1)
        temp = [temp1, temp2, temp3]
        mu1 = max(temp)
        temp.remove(mu1)
        if random.uniform(0, 1) < 0.5:
            mu2 = max(temp)
            lambdaa = min(temp)
        else:
            lambdaa = max(temp)
            mu2 = min(temp)

        # normalize
        (lambdaa, mu1, mu2) = (lambdaa / (lambdaa + mu1 + mu2), mu1 / (lambdaa + mu1 + mu2), mu2 / (lambdaa + mu1 + mu2))

        # Create the MDP
        statespace_size = 2 * (L + 1)

        # We number the states, starting with the the ones where server2 is not used
        # In that way we get the actions as follows
        actionspace_matrix = [get_actions(x, L, lambdaa, mu1, mu2) for x in range(2 * (L + 1))]

        rewards_vector = get_rewards_vector(L, lambdaa, mu1, mu2)

        mdp = MDP(statespace_size, actionspace_matrix, rewards_vector)

        iter = (0.75 * L) / half_sample_size
        value_iteration_result = mdp.value_iteration(epsilon, [0 for i in range(statespace_size)])

        # sample points are 1, 1+iter, 1+2iter, ... and L + 1 + 1 + iter, L + 1 + 1 + 2iter,...
        sample_points = [[math.floor(iter * i + 1), (value_iteration_result[1][-1][math.floor(iter * i + 1)] - value_iteration_result[1][-1][0])  / 10] for i in range(half_sample_size)] +\
                        [[math.floor(L + 1 + iter * i + 1), (value_iteration_result[1][-1][math.floor(L + 1 + iter * i + 1)] - value_iteration_result[1][-1][0]) / 10] for i in range(half_sample_size)]

        with open('sample_points.txt', 'a') as f:
            f.write("[%s, %s, %s]\n" %(lambdaa, mu1, mu2))
            for item in sample_points:
                f.write("%s\n" % item)
            f.write("---\n")

# Gives the actions starting from a position x
def get_actions(x, L, lambdaa, mu1, mu2):
    odds_list0 = [0 for j in range(2 * (L + 1))]
    odds_list1 = [0 for j in range(2 * (L + 1))]

    if x == 0:
        odds_list0[1] = 1
        return [Action(x, odds_list0)]
    elif x == L:
        odds_list0[x - 1] = mu2
        odds_list0[L + 1 + x - 2] = mu1
        odds_list0[L + 1 + x] = lambdaa
        odds_list1[x - 1] = 1
        return [Action(x, odds_list0), Action(x, odds_list1)]
    elif x == L + 1:
        odds_list0[0] = mu2 / (mu2 + lambdaa)
        odds_list0[L + 2] = lambdaa / (mu2 + lambdaa)
        return [Action(x, odds_list0)]
    elif x == 2 * L + 1:
        odds_list0[2 * L] = mu1 / (mu1 + mu2)
        odds_list0[L] = mu2 / (mu1 + mu2)
        return [Action(x, odds_list0)]
    elif x == 1:
        odds_list0[x - 1] = mu2 / (lambdaa + mu2)
        odds_list0[L + 1 + x] = lambdaa / (lambdaa + mu2)
        odds_list1[x + 1] = lambdaa / (lambdaa + mu1)
        odds_list1[x - 1] = mu1 / (lambdaa + mu1)
        return [Action(x, odds_list0), Action(x, odds_list1)]
    elif x < L:
        odds_list0[x - 1] = mu2
        odds_list0[L + 1 + x - 2] = mu1
        odds_list0[L + 1 + x] = lambdaa
        odds_list1[x + 1] = lambdaa / (lambdaa + mu1)
        odds_list1[x - 1] = mu1 / (lambdaa + mu1)
        return [Action(x, odds_list0), Action(x, odds_list1)]
    elif x > L:
        odds_list0[x + 1] = lambdaa
        odds_list0[x - 1] = mu1
        odds_list0[x - (L + 1)] = mu2
        return [Action(x, odds_list0)]

def get_rewards_vector(L, lambdaa, mu1, mu2):
    # server 2 not used, looking at both actions. First in general, then 3 boundary cases for both actions
    rewards_vector = [[0, x, L + 1 + x, get_reward(L, L + 1 + x)] for x in range(2, L)]
    rewards_vector += [[0, x, L + 1 + x - 2, get_reward(L, L + 1 + x - 2)] for x in range(2, L)]
    rewards_vector += [[0, x, x - 1, get_reward(L, x - 1)] for x in range(2, L)]

    rewards_vector += [[1, x, x + 1, get_reward(L, x + 1)] for x in range(2, L)]
    rewards_vector += [[1, x, x - 1, get_reward(L, x - 1)] for x in range(2, L)]


    rewards_vector += [[0, 1, 0, get_reward(L, 0)], [0, 1, L + 2, get_reward(L, L + 2)]]
    rewards_vector += [[1, 1, 0, get_reward(L, 0)], [1, 1, 2, get_reward(L, 2)]]
    rewards_vector += [[0, 0, 1, get_reward(L, 1)]] # no other action is possible in this case
    rewards_vector += [[0, L, L + L + 1, get_reward(L, L + L + 1)], [0, L, L - 1, get_reward(L, L - 1)], [0, L, L + 1 + L - 2, get_reward(L, L + 1 + L - 2)]]
    rewards_vector += [[1, L, L - 1, get_reward(L, L - 1)]]

    # server 2 is used, looking at the only possible action. First in general, then 2 boundary cases for both actions
    rewards_vector += [[0, L + 1 + x, x, get_reward(L, x)] for x in range(1, L)]
    rewards_vector += [[0, L + 1 + x, L + 1 + x - 1, get_reward(L, L + 1 + x - 1)] for x in range(1, L)]
    rewards_vector += [[0, L + 1 + x, L + 1 + x + 1, get_reward(L, L + 1 + x + 1)] for x in range(1, L)]

    rewards_vector += [[0, L + 1, 0, get_reward(L, 0)], [0, L + 1, L + 1 + 1, get_reward(L, L + 1 + 1)]]
    rewards_vector += [[0, L + 1 + L, L, get_reward(L, L)], [0, L + 1 + L, L + 1 + L - 1, get_reward(L, L + 1 + L - 1)]]


    return rewards_vector

def get_reward(L, result):
    if result < L + 1:
        return -result
    else:
        return -(result - L)