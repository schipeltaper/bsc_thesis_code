import numpy as np
# numpy argmax
# sum, max, min, ...

# Defines a complete finite markov decision process
class MDP:
    def __init__(self, statespace_size, actionspace_matrix, rewards_vector):
        # statespace_size is just an integer
        self.statespace_size = statespace_size

        # actionspace_matrix is a matrix with actions, where the r'th row represents the actions for the r'th state.
            # Action is a class which represents an action.
        self.actionspace_matrix = actionspace_matrix

        # rewards_vector is a vector of quadruples of the form [action_number, state1, state2, reward]
        self.rewards_vector = rewards_vector

        # average_rewards_dic is a dictionary of the form with key value: "action_state" giving the value of the average reward
        self.average_rewards_dic = {}

        # loop over actions so per state so that we can calculate the average reward per action
        for i in range(statespace_size):
            action_amount = len(actionspace_matrix[i])

            for action_number in range(action_amount):
                average_reward = 0

                # look at all possible routes within this specific action
                for element in rewards_vector:
                    if element[0] == action_number and element[1] == i:

                        # odds of going through this route
                        odds = self.actionspace_matrix[i][element[0]].probabilities_vector[element[2]]

                        average_reward += odds * element[3]
                self.average_rewards_dic["{}_{}".format(action_number, i)] = average_reward

    def __str__(self):
        # state space size
        to_print = "________________________\n"
        to_print += "This MDP has {} states\n\n".format(self.statespace_size)

        # action space
        to_print += \
        "Here follows a matrix in which each row represents a state. \n\
Each entry represents an action of that row in the form of a vector. \n\
The n'th entry of the vector represents the odds of going to that state.\n\n"
        for i in range(self.statespace_size):
            for j in range(len(self.actionspace_matrix[i])):
                to_print += str(self.actionspace_matrix[i][j])
                to_print += "   "

            to_print += "\n"

        # reward space
        to_print += "\nHere follows all the rewards that can be received in the form of [action_number, state 1, state 2, reward]\n"

        for reward in self.rewards_vector:
            to_print += "[{}, {}, {}, {}]\n".format(reward[0], reward[1], reward[2], reward[3])

        return to_print

    # The function of Value Iteration with the starting function being 0 everywhere.
    def value_iteration(self, epsilon, v_0):
        outcome_matrix = [v_0]

        # Shows the best choice of actions in each step in the iteration.
        strategy_matrix = []
        it = 0

        # Successive Approximation algorithm (AKA Value Iteration)
        while True:
            # see equation (2.19) in dictaat
            v_next = [max([float(self.average_rewards_dic["{}_{}".format(action_number, i)]) +
            sum([self.actionspace_matrix[i][action_number].probabilities_vector[j] * outcome_matrix[it][j] for j in range(self.statespace_size)])
            for action_number in range(len(self.actionspace_matrix[i]))]) for i in range(self.statespace_size)]

            outcome_matrix.append(v_next)

            # Represents in each step the function of which action to choose
            strategy_next = [np.argmax([float(self.average_rewards_dic["{}_{}".format(action_number, i)]) +
            sum([self.actionspace_matrix[i][action_number].probabilities_vector[j] * outcome_matrix[it][j] for j in range(self.statespace_size)])
            for action_number in range(len(self.actionspace_matrix[i]))]) for i in range(self.statespace_size)]

            # just appending a vector of numbers where each number represents the position of the optimal action
            strategy_matrix.append(strategy_next)

            # A tad different than the dictaat
            big_M = max([outcome_matrix[it][i] - outcome_matrix[it - 1][i] for i in range(self.statespace_size)])
            small_m = min([outcome_matrix[it][i] - outcome_matrix[it - 1][i] for i in range(self.statespace_size)])

            if big_M - small_m < epsilon or it == 100:
                break

            it += 1

        return (it, outcome_matrix, strategy_matrix)


# Action class represents an action:
    # We present this as a tuple
        # first entry: the state that we start in
        # second entry: vector where the r'th entry presents the probability that we will go to the r'th state
class Action:
    def __init__(self, state, probabilities_vector):
        self.state = state
        self.probabilities_vector = probabilities_vector

    def __str__(self):
        to_print = "["
        for odds in self.probabilities_vector:
            to_print += "{}, ".format(odds)
        to_print = to_print[:-2]
        to_print += "]"

        return to_print
