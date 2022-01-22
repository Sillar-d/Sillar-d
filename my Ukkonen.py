def ukkonen(string):
    # add terminal character to string
    string = string + '$'
    n = len(string)

    global_end = None

    # Node class, which forms the suffix tree structure
    class Node:
        def __init__(self, edge_label):
            self.edge_label = edge_label  # the label of the edge leading into the node, (start_index, end_index)
            self.leaf = False  # stores whether the node is a leaf or internal node
            self.suffix_link = None  # stores the suffix link to the Node with path 'a' where this node has path 'xa'
            self.children = [None] * 27  # include lowercase letters + '$' terminal, hence max of 27 edges off any node
            # could store list of children indices != None, but sorting list would take O(k log k) worst case

        def get_edge_label(self):
            if self.leaf is True:
                return [self.edge_label[0], global_end]
            else:
                return self.edge_label

    # returns int value of lowercase english letter, with a=0 and z=25
    def get_char_number(char):
        # lowercase letter
        if ord(char) > 36:
            return ord(char) - 96
        # terminal symbol '$'
        else:
            return 0

    # Create Implicit suffix tree containing only the first character
    root_node = Node(None)
    root_node.suffix_link = root_node
    leaf1 = Node([0, 'global_end'])
    leaf1.leaf = True
    root_node.children[get_char_number(string[0])] = leaf1

    # update initial states
    active_node = root_node
    remainder = ''
    last_j = 0
    global_end = 0
    unresolved_suffix_link = None

    # build suffix tree
    for i in range(1, n):
        # begin phase i+1 and perform rapid leaf extension
        global_end += 1
        # break switch to allow skipping of extensions after a rule 3
        break_switch = False

        # explicit extensions from last_j + 1
        for j in range(last_j+1, i+1):
            # check if we have done an extension 3 this phase, if so continue skipping until next phase
            if break_switch is False:
                # skip count down to the extension point
                # if the remainder is not empty, we need to move from the active node
                # until we get to the end of remainder
                if remainder != '':
                    # check if the edge starting with char(remainder[0]) contains the entire remainder
                    cur_edge = active_node.children[get_char_number(remainder[0])].get_edge_label()
                    # if edge is larger than remainder, do nothing as already know where to start

                    # while edge label is smaller than remainder, update active node and remainder and check again
                    while cur_edge[1] - cur_edge[0] < len(remainder):
                        # update active node to point to node at end of current edge
                        active_node = active_node.children[get_char_number(remainder[0])]
                        # chop start off remainder that has already been parsed
                        remainder = remainder[cur_edge[1] - cur_edge[0] + 1:]
                        # if still some remainder, update cur_edge to be the new edge we
                        # are interested in, coming off new active_node
                        if remainder != '':
                            cur_edge = active_node.children[get_char_number(remainder[0])].get_edge_label()
                # if remainder is empty, we start explicit checking immediately at the active node ==> nothing done

                # we now have the appropriate active node, with remainder string ending before next node
                # apply appropriate extension rule
                # if remainder not empty, checking character after len(remainder)-th character along active edge
                if remainder != '':
                    # cur_edge will exist by Lemma 2
                    cur_edge = active_node.children[get_char_number(remainder[0])].get_edge_label()
                    # active_point = cur_edge(start_index) + len(remainder)
                    active_point = cur_edge[0] + len(remainder)
                    # if character at active point does not match the character we are inserting, split the edge
                    # rule 2b, new internal node created
                    if string[active_point] != string[i]:
                        # create new internal node with edge label containing start of split edge up to active_point-1
                        new_internal_node = Node([cur_edge[0], active_point - 1])
                        # shorten edge_label on edge that was just split
                        split_edge = cur_edge
                        split_edge[0] = split_edge[0] + len(remainder)
                        active_node.children[get_char_number(remainder[0])].edge_label[0] = split_edge[0]
                        # make new internal node point to node whose edge was just split
                        new_internal_node.children[get_char_number(string[active_point])] = \
                            active_node.children[get_char_number(remainder[0])]
                        # replace the old node which was just split with new node in active_node.children
                        active_node.children[get_char_number(remainder[0])] = new_internal_node
                        # create new leaf with label of i+1
                        new_leaf = Node([i, 'global_end'])
                        new_leaf.leaf = True
                        # add new leaf as child of new internal node
                        new_internal_node.children[get_char_number(string[i])] = new_leaf
                        # update last j
                        last_j += 1
                        # if we have unresolved suffix link, it points to the newly created node
                        if unresolved_suffix_link is not None:
                            unresolved_suffix_link.suffix_link = new_internal_node
                        # store newly created node as it has an unresolved suffix link
                        unresolved_suffix_link = new_internal_node
                        # follow suffix link, checking if root node cycle as would need to remove start of remainder
                        # if suffix link points to itself (at root node), remove first character from remainder
                        if active_node.suffix_link == active_node:
                            remainder = remainder[1:]
                        # if suffix link changes active_node, first character removed implicitly
                        else:
                            active_node = active_node.suffix_link

                    # else remainder not empty and character at active point does match i+1, rule 3 (break early)
                    else:
                        # update remainder to include extra char
                        remainder = remainder + string[active_point]
                        # terminate this phase (no more extensions)
                        break_switch = True

                # if remainder is empty, checking all children of active_node to
                # see if i+1 char already there, if not rule 2a
                else:
                    # edge starting with char string(i+1) already exists, rule 3 (add char to remainder)
                    if active_node.children[get_char_number(string[i])] is not None:
                        # update remainder to include extra char
                        remainder = string[i]
                        # resolve suffix link
                        if unresolved_suffix_link is not None:
                            unresolved_suffix_link.suffix_link = active_node
                            unresolved_suffix_link = None       # or do i make active node the unresolved????
                        # terminate this phase (no more extensions)
                        break_switch = True

                    # no valid edge exists, create new leaf node, rule 2a no new internal node
                    else:
                        # create new leaf with label of i+1
                        new_leaf = Node([i, 'global_end'])
                        new_leaf.leaf = True
                        # add new leaf as child of active node
                        active_node.children[get_char_number(string[i])] = new_leaf

                        # if unresolved_suffix_link not None, it points to active_node,
                        # and there is now no unresolved_suffix_link
                        if unresolved_suffix_link is not None:
                            unresolved_suffix_link.suffix_link = active_node
                            unresolved_suffix_link = None

                        # follow suffix link, either was root so phase ends, or
                        # move up edge with 1 char in label (explicitly removed)
                        active_node = active_node.suffix_link

                        last_j += 1

    return root_node, global_end
