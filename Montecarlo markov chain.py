# Daniel Sillar 26879026
import math
import random


# n = size of cycle
def montecarlo_markov_chain(n):
    # stores nodes to quickly access a position
    positions = [None]*n

    class Node:
        def __init__(self):
            self.type = None    # stores type/colour of node, either 0 or 1
            # will use nodes to form double linked list
            self.left = None
            self.right = None

    # allocate number of each type
    one_list = [1]*int(math.ceil(n/2))
    zero_list = [0]*int(math.floor(n/2))
    colour_list = one_list + zero_list
    # create first node
    first_node = Node
    # allocate colour
    colour = random.choice(colour_list)
    colour_list.remove(colour)
    first_node.type = colour
    # point to itself
    first_node.right = first_node
    first_node.left = first_node
    # add to list of nodes
    positions[0] = first_node

    # add rest of nodes, randomly allocating colour
    for k in range(1, n):
        new_node = Node()

        # allocate colour
        colour = random.choice(colour_list)
        colour_list.remove(colour)
        new_node.type = colour

        # add to list and update links
        positions[k] = new_node
        new_node.left = positions[k-1]
        new_node.right = first_node
        new_node.left.right = new_node
        new_node.right.left = new_node

    # attempt to perform swaps until no successful swap has occurred within 'accuracy' attempts
    # as there are n positions, there are 0.5*(n^2 - n) potential pairings. this accuracy attempts approx. 10x as
    # many matches. resultant chance of missing a single match = (1- 2/(n^2 - n))^accuracy [really small number]
    accuracy = 5 * n ** 2
    absorption_time = 0
    attempts_since_swap = 0
    while attempts_since_swap < accuracy:
        # nodes to swap/ 'matching' is defined to be randomly uniform. this means despite two same coloured nodes
        # never swapping, we must still allow those matches to be chosen as they count towards absorption time
        pos_a = random.randint(0, n - 1)
        pos_b = random.randint(0, n - 1)
        # make sure they are different positions, as defined in question
        while pos_b == pos_a:
            pos_b = random.randint(0, n - 1)

        # match has been made, update absorption time
        absorption_time += 1
        # check if swap is good
        # nodes must be of different colours, else will be moving one to unhappy position
        if positions[pos_a].type != positions[pos_b].type:
            # at least one node must have two different neighbours (else both happy already) AND both must have
            # at least one different neighbour (else one will be swapping into unhappy position)
            a_mismatch_neighbours = 0
            if positions[pos_a].type != positions[pos_a].left.type:
                a_mismatch_neighbours += 1
            if positions[pos_a].type != positions[pos_a].right.type:
                a_mismatch_neighbours += 1

            b_mismatch_neighbours = 0
            if positions[pos_b].type != positions[pos_b].left.type:
                b_mismatch_neighbours += 1
            if positions[pos_b].type != positions[pos_b].right.type:
                b_mismatch_neighbours += 1

            if a_mismatch_neighbours >= 2 and b_mismatch_neighbours >= 1 or \
                    b_mismatch_neighbours >= 2 and a_mismatch_neighbours >= 1:
                # swap colours
                positions[pos_a].type, positions[pos_b].type = positions[pos_b].type, positions[pos_a].type
                # reset attempts since swap
                attempts_since_swap = 0
            else:
                attempts_since_swap += 1
        else:
            attempts_since_swap += 1

    # returns only number of iterations before stable state was reached
    return absorption_time - attempts_since_swap


# gives simulated expected value
iterations = 20000
for n in range(4, 11):
    sum_total = 0
    for k in range(0, iterations):
        val = montecarlo_markov_chain(n)
        sum_total += val
    print(sum_total/iterations)


