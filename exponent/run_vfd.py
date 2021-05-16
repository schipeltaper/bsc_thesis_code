import random
import copy

from tree import *

# values straight from the paper
population_size = 1000
children_size = 500
max_element_tree = 125
min_error = 0.5
diversity_threshold = 0.01
apply_mutation_prob = 0.2

from_good_prob = 0.8
good_pct = 0.32

prob_divide = 0.1
prob_exp = 0.2
prob_plus = 0.23
prob_minus = 0.23
prob_multiply = 0.23
prob_parameter = 0.45
prob_variable = 0.45
prob_constant = 0.1
max_constant_value = 1

# test
laagste_error = 100000
largest_size = 1

# helps generate trees
node_number = 0


def run_vfd(Q, L, half_sample_size):
    # get all the sample data from the file
    data = get_data_from_file("sample_points_thesis.txt")

    # initialize a random population of functions, in the form
    # of [[tree, error], [tree, error], [tree, error], ...]
    population = [0 for k in range(population_size)]
    init_population(population, Q, L, half_sample_size, data)

    it_check = 0

    while population[0][1] > min_error:
        global largest_size
        for i in range(len(population)):
            if len(population[i][0].nodes_list) > largest_size:
                largest_size = len(population[i][0].nodes_list)
                print(largest_size)


        # when the algorithm is not diverse enough, it probably means we're a little bit stuck
        # so we try the whole process again
        if not is_population_diverse(population):
            print("hey")
            init_population(population, Q, L, half_sample_size, data)

        # amount of children that are produced
        current_children = 0

        # here we will save all children
        children = [0 for k in range(children_size)]

        while current_children < children_size:
            if random.uniform(0, 1) < apply_mutation_prob:
                children[current_children] = [apply_mutation(population), 0]
            else:
                [child1, child2] = apply_recombination(population)

                children[current_children] = [child1, 0]
                if current_children < children_size - 1:
                    current_children += 1
                    if current_children == children_size:
                        break
                    children[current_children] = [child2, 0]
            current_children += 1

        if not is_population_valid(children):
            print("creating_children")
            return

        set_error(children, Q, L, half_sample_size, data)

        population = population + children

        # lowest error comes first (with slight disadvantage for large trees)
        population = sorted(population, key=lambda tup: tup[1] + len(tup[0].nodes_list) / 100)

        # delete the worst estimates
        del population[population_size:]

        it_check += 1
        # print(it_check)


    return population[0][0]

# return the 3 parameters and
# a list [(state, value), (state, value), ...]
# in the form of [[[parameters], [tuples]], [[parameters], [tuples]]...]
def get_data_from_file(file_name):
    f = open(file_name, "r")
    data = []
    parameters = 0
    value_list = []
    for line in f:
        if line == "---\n":
            data.append([parameters, value_list])
            parameters = 0
            value_list = []
        else:
            converted_line = make_list_from_string(line)
            if parameters == 0:
                parameters = converted_line
            else:
                value_list += [converted_line]

    return data

def make_list_from_string(the_string):
    the_list = []
    number = ""
    for char in the_string:
        if char == ',' or char == ']':
            the_list.append(float(number))
            number = ""
        elif not char == '[' and not char == ' ':
            number += char

    return the_list


def init_population(population, Q, L, half_sample_size, data):
    for k in range(population_size):
        population[k] = [generate_random_tree(), 0]
    set_error(population, Q, L, half_sample_size, data)

    # lowest error comes first (with slight disadvantage for large trees)
    population = sorted(population, key=lambda tup: tup[1] + len(tup[0].nodes_list) / 100)

def set_error(population, Q, L, half_sample_size, data):
    for tree in population:
        max_error = 0
        for q in range(Q):
            error = calc_error(q, tree[0], data)
            max_error = max(error, max_error)
        tree[1] = max_error
        global laagste_error
        if max_error < laagste_error:
            laagste_error = max_error
            print("error:")
            print(max_error)
            print("nodes:")
            print(tree[0].nodes_list)

def calc_error(q, tree, data):
    # return the highest difference between
    # what the tree outputs with those parameters
    # what the sample gives
    # for each of the 20 states (sample spots)
    max_error = 0

    # in the form of [[state, value], [state, value], ...]
    relevant_data = copy.deepcopy(data[q][1])

    # in the form of [lambdaa, mu1, mu2]
    parameters = copy.deepcopy(data[q][0])

    for state in relevant_data:
        temp_tree = copy.deepcopy(tree)

        # make sure that the error with an impossible function is so high, it won't survive
        try:
            output_tree = temp_tree.output_tree(parameters, state[0])
        except:
            output_tree = "ERROR"
            print("NOOOOOO")
        if output_tree == "ERROR" or len(tree.nodes_list) > max_element_tree:
            err = 1000000
        else:
            err = abs((output_tree - state[1]) / state[1])
        max_error = max(max_error, err)

    return max_error


# generates a random tree
def generate_random_tree():
    # we start with a high probability to have an operator in the tree
    prob_operator = 0.8

    the_random_tree = []

    global node_number
    node_number = -1

    generate_tree_recurse(the_random_tree, prob_operator, None)

    random_tree = Function_Tree(the_random_tree)
    return random_tree

def generate_tree_recurse(the_random_tree, prob_operator, parent):
    global node_number
    node_number += 1
    # when we create an operator
    if random.uniform(0, 1) < prob_operator:
        which_operator = random.uniform(0, 1)
        if which_operator < prob_plus:
            the_random_tree.append([node_number, "+", parent])
            new_parent = node_number
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
        elif which_operator < prob_plus + prob_minus:
            the_random_tree.append([node_number, "-", parent])
            new_parent = node_number
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
        elif which_operator < prob_plus + prob_minus + prob_multiply:
            the_random_tree.append([node_number, "*", parent])
            new_parent = node_number
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
        elif which_operator < prob_plus + prob_minus + prob_multiply + prob_divide:
            the_random_tree.append([node_number, "/", parent])
            new_parent = node_number
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
        else:
            the_random_tree.append([node_number, "^", parent])
            new_parent = node_number
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
            generate_tree_recurse(the_random_tree, prob_operator / 2, new_parent)
    # when we create a non-operator node
    else:
        which_value = random.uniform(0, 1)
        if which_value < prob_variable:
            the_random_tree.append([node_number, "x", parent])
        elif which_value < prob_variable + prob_parameter:
            which_parameter = random.uniform(0, 1)
            if which_parameter < 0.33:
                the_random_tree.append([node_number, "lambdaa", parent])
            elif which_parameter < 0.67:
                the_random_tree.append([node_number, "mu1", parent])
            else:
                the_random_tree.append([node_number, "mu2", parent])
        else:
            the_random_tree.append([node_number, random.uniform(0, 1), parent])


# Return a child
def apply_mutation(population):
    parent_index = random.randint(0, population_size - 1)
    parent_temp = population[parent_index][0]
    parent = copy.deepcopy(parent_temp)

    # which node will be selected for the mutation
    node_index = random.randint(0, parent.num_elements() - 1)

    sub_tree = generate_random_tree()

    child_list = parent.replace_node(node_index, sub_tree.nodes_list)
    child = Function_Tree(child_list)

    return child


# Return two children
def apply_recombination(population):
    parent_index1 = random.randint(0, population_size - 1)
    parent_index2 = random.randint(0, population_size - 1)

    parent1_temp = population[parent_index1][0]
    parent2_temp = population[parent_index2][0]

    parent1 = copy.deepcopy(parent1_temp)
    parent2 = copy.deepcopy(parent2_temp)

    # which nodes will be selected for the recombination
    node_index1 = random.randint(0, parent1.num_elements() - 1)
    node_index2 = random.randint(0, parent2.num_elements() - 1)

    sub_tree1_list = parent1.get_subtree(node_index1)
    sub_tree2_list = parent2.get_subtree(node_index2)

    parent1 = copy.deepcopy(parent1_temp)
    parent2 = copy.deepcopy(parent2_temp)

    child1_list = parent1.replace_node(node_index1, sub_tree2_list)
    child2_list = parent2.replace_node(node_index2, sub_tree1_list)

    child1 = Function_Tree(child1_list)
    child2 = Function_Tree(child2_list)

    return [child1, child2]


def is_population_diverse(population):
    lowest = population[0][1]
    highest = population[-1][1]

    return (highest - lowest) / lowest > diversity_threshold


# check wether the population is a valid one
# does every operator have exactly two children?
# does every indicated parent exist?
# does every non-operator have exactly 0 children?
# is the identity unique for a node in a tree?
# is there exactly one node with None parent
def is_population_valid(population):
    for i in range(len(population)):
        nodes = population[i][0].nodes_list
        if not is_tree_valid(nodes):
            return False
    return True

def is_tree_valid(nodes):
    is_tree_valid = operator_two_children(nodes) and every_parent_exist(nodes) and\
            every_non_operator_zero_children(nodes) and node_identity_unique(nodes) and\
                exactly_one_none_parent(nodes)

    return is_tree_valid

def operator_two_children(nodes):
    for node in nodes:
        if node[1] == '+' or node[1] == '-' or node[1] == '/' or node[1] == '*' or node[1] == '^':
                children_amount = 0
                for other_node in nodes:
                    if other_node[2] == node[0]:
                        if other_node [0] == node[0]:
                            return False
                        children_amount += 1

                if not children_amount == 2:
                    return False
    return True


def every_parent_exist(nodes):
    for node in nodes:
        exists = False
        for other_node in nodes:
            if other_node[0] == node[2]:
                exists = True
        if not exists and not node[2] == None:
            return False
    return True

def every_non_operator_zero_children(nodes):
    for node in nodes:
        if not (node[1] == '+' or node[1] == '-' or node[1] == '/' or node[1] == '*' or node[1] == '^'):
            for other_node in nodes:
                if other_node[2] == node[0]:
                    return False
    return True


def node_identity_unique(nodes):
    identities = []
    for node in nodes:
        if node[0] in identities:
            return False
        else:
            identities.append(node[0])

    return True

def exactly_one_none_parent(nodes):
    none_parent_amount = 0
    for node in nodes:
        if node[2] == None:
            none_parent_amount += 1
            if none_parent_amount > 1:
                return False
    if none_parent_amount == 0:
        return False
    return True
