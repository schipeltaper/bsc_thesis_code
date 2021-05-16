import copy


class Function_Tree():
    # nodes list is list of triples of the form: (node_number, character, parent)
    # The highest nodes in the tree get the lowest node_number, it starts at 0.
    def __init__(self, nodes_list):
        self.nodes_list = nodes_list

    def num_elements(self):
        return len(self.nodes_list)

    def __getitem__(self):
        return self.nodes_list

    def replace_node(self, node_index, sub_tree_list):
        if node_index == 0:
            return sub_tree_list

        remove_these_nodes = [node_index]

        # fill in the remove_these_nodes list
        self.recurse_remove(node_index, remove_these_nodes)

        # nodes without the ones that should be removed
        new_nodes_list = [node for node in self.nodes_list if not node[0] in remove_these_nodes]

        # we will create the new subtree so that it can be added nicely
        new_sub_tree = copy.deepcopy(sub_tree_list)

        if not new_sub_tree == []:
            parent = None
            # preparing to connect subtree with main tree
            for i in range(len(self.nodes_list)):
                if self.nodes_list[i][0] == node_index:
                    parent = self.nodes_list[i][2]


            # new subtree, making sure that numbers don't overlap
            for node in new_sub_tree:
                if node[0] == 0:
                    node[0] = -1/2
                elif not node[0] == -1/2:
                    node[0] = -node[0]

                if node[2] == 0:
                    node[2] = -1/2
                elif not node[2] == None and not node[2] == -1/2:

                    node[2] = -node[2]

            new_sub_tree[0][2] = parent

            # connect the two trees
            new_nodes_list += new_sub_tree

        # making the numbers normal again.
        for i in range(len(new_nodes_list)):
            temp = new_nodes_list[i][0]
            new_nodes_list[i][0] = i
            for node in new_nodes_list:
                if node[2] == temp:
                    node[2] = i

        return new_nodes_list

    def recurse_remove(self, current_parent, remove_these_nodes):
        for i in range(len(self.nodes_list)):
            if self.nodes_list[i][2] == current_parent:
                remove_these_nodes.append(self.nodes_list[i][0])
                self.recurse_remove(self.nodes_list[i][0], remove_these_nodes)

    # helps compute outcome tree
    def output_recurse(self, parent, parameters, state):
        return_values = []
        for i in range(len(self.nodes_list)):
            if self.nodes_list[i][2] == parent:
                if self.nodes_list[i][1] == "+":
                    next_values = self.output_recurse(self.nodes_list[i][0], parameters, state)
                    if "ERROR" in next_values or "ERROR" == next_values:
                        return "ERROR"
                    return_values.append(sum(next_values))
                elif self.nodes_list[i][1] == "-":
                    next_values = self.output_recurse(self.nodes_list[i][0], parameters, state)
                    if "ERROR" in next_values or "ERROR" == next_values:
                        return "ERROR"
                    return_values.append(next_values[0] - next_values[1])
                elif self.nodes_list[i][1] == "*":
                    next_values = self.output_recurse(self.nodes_list[i][0], parameters, state)
                    if "ERROR" in next_values or "ERROR" == next_values:
                        return "ERROR"
                    return_values.append(next_values[0] * next_values[1])
                elif self.nodes_list[i][1] == "/":
                    next_values = self.output_recurse(self.nodes_list[i][0], parameters, state)
                    if "ERROR" in next_values or "ERROR" == next_values:
                        return "ERROR"
                    try:
                        return_values.append(next_values[0] / next_values[1])
                    except:
                        return "ERROR"
                elif self.nodes_list[i][1] == "^":
                    next_values = self.output_recurse(self.nodes_list[i][0], parameters, state)
                    if "ERROR" in next_values or "ERROR" == next_values:
                        return "ERROR"
                    try:
                        return_values.append(next_values[0] ** next_values[1])
                    except:
                        return "ERROR"
                elif self.nodes_list[i][1] == "x":
                    return_values.append(state)
                elif self.nodes_list[i][1] == "lambdaa":
                    return_values.append(parameters[0])
                elif self.nodes_list[i][1] == "mu1":
                    return_values.append(parameters[1])
                elif self.nodes_list[i][1] == "mu2":
                    return_values.append(parameters[2])
                else:
                    return_values.append(self.nodes_list[i][1])
        return return_values

    # parameters in the form of [lambda, mu1, mu2]
    # state: the state number x + (L + 1)i
    # outputs the result of the function of this tree, given the parameters and state.
    def output_tree(self, parameters, state):
        nodes_list = self.__getitem__()
        starting_node = nodes_list[0]
        if starting_node[1] == "+":
            next_values = self.output_recurse(starting_node[0], parameters, state)
            if "ERROR" in next_values or "ERROR" == next_values:
                return "ERROR"
            return next_values[0] + next_values[1]
        elif starting_node[1] == "-":
            next_values = self.output_recurse(starting_node[0], parameters, state)
            if "ERROR" in next_values or "ERROR" == next_values:
                return "ERROR"
            return next_values[0] - next_values[1]
        elif starting_node[1] == "*":
            next_values = self.output_recurse(starting_node[0], parameters, state)
            if "ERROR" in next_values or "ERROR" == next_values:
                return "ERROR"
            return next_values[0] * next_values[1]
        elif starting_node[1] == "/":
            next_values = self.output_recurse(starting_node[0], parameters, state)
            if "ERROR" in next_values or "ERROR" == next_values:
                return "ERROR"

            try:
                return next_values[0] / next_values[1]
            except:
                return "ERROR"
        elif starting_node[1] == "^":
            next_values = self.output_recurse(starting_node[0], parameters, state)
            if "ERROR" in next_values or "ERROR" == next_values:
                return "ERROR"

            try:
                return next_values[0] ** next_values[1]
            except:
                return "ERROR"
        elif starting_node[1] == "x":
            return state
        elif starting_node[1] == "lambdaa":
            return parameters[0]
        elif starting_node[1] == "mu1":
            return parameters[1]
        elif starting_node[1] == "mu2":
            return parameters[2]
        else:
            return starting_node[1]

    def subtree_recurse(self, sub_tree, parent):
        # use for i in range...
        for i in range(len(self.nodes_list)):
            if self.nodes_list[i][2] == parent:
                sub_tree.append(self.nodes_list[i])
                self.subtree_recurse(sub_tree, self.nodes_list[i][0])

    def get_subtree(self, node_index):
        sub_tree = []

        for i in range(len(self.nodes_list)):
            if self.nodes_list[i][0] == node_index:
                sub_tree.append(self.nodes_list[i])

                parent = self.nodes_list[i][0]

        self.subtree_recurse(sub_tree, parent)

        # making numbers normal again
        information_saved = []
        for i in range(len(sub_tree)):
            temp = sub_tree[i][0]
            sub_tree[i][0] = i
            information_saved.append([i, temp])
        sub_tree[0][2] = None

        for i in range(len(sub_tree)):
            for tup in information_saved:
                if tup[1] == sub_tree[i][2]:
                    sub_tree[i][2] = tup[0]
                    break

        return sub_tree
