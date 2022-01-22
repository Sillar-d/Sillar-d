# Daniel Sillar 26879026
import sys
import math

size_V = int(sys.argv[1])
edge_file = open(sys.argv[2], 'r')
edges = []
for line in edge_file:
    line = line.strip()
    line = tuple(int(x) for x in line.split(" "))
    edges.append(line)
edge_file.close()


class Node:
    def __init__(self, edge):
        self.key = edge[2]
        self.payload = edge
        self.degree = 0
        self.parent = None
        self.left = self
        self.right = self
        self.child = None
        self.child_count = 0


# builds a fibonacci heap from an unsorted list of edges based on weights, and supports extract_min with consolidate
class FibonacciHeap:
    def __init__(self):
        self.h_min = None
        # maintain number of nodes to know size of auxiliary array in consolidate
        self.node_count = 0
        self.current = None
        self.root_list_length = 0
        # maintain root list length as cant have a start/end node in case that node becomes a child during consolidate

    def insert(self, node: Node):
        if self.node_count == 0:
            self.h_min = node
        # save current left of h_min as left_h_min
        left_h_min = self.h_min.left
        # make new node be to the right of left_h_min, attaching pointers both ways
        left_h_min.right = node
        node.left = left_h_min
        # make new node be to the left of h_min, attaching pointers both ways
        self.h_min.left = node
        node.right = self.h_min
        # check if new node should be new h_min
        if node.key < self.h_min.key:
            self.h_min = node
        # update number of nodes
        self.node_count += 1
        self.root_list_length += 1

    def extract_min(self):
        if self.h_min.child is not None:
            # Promote children to root list, break linked list of children at child.left,
            # changing child.left to h_min.left (pointer both ways)
            # and set child.left.right from child to current (h_min.right, pointer both ways)
            self.h_min.right.left = self.h_min.child.left
            self.h_min.child.left.right = self.h_min.right
            self.h_min.child.left = self.h_min.left
            self.h_min.left.right = self.h_min.child
            # increase root_list_length by number of children of extracted node just moved up
            self.root_list_length += self.h_min.child_count
        # move h_min to right of old h_min (will become proper minimum after consolidate is run)
        self.h_min = self.h_min.right
        # update node count
        self.node_count -= 1
        self.root_list_length -= 1
        # run consolidate/ merge if node_count > 1:
        if self.node_count > 1:
            self.consolidate()
        # return h_min's payload
        return self.h_min.payload

    def merge(self, a: Node, b: Node):
        if a.key < b.key:
            # update b's neighbours to point over b
            b.left.right = b.right
            b.right.left = b.left
            # add b to child linked list of a
            if a.child is None:
                a.child = b
                # remove old left and right pointers and point to itself as is only item
                b.left = b
                b.right = b
            else:
                a.child.left.right = b
                b.left = a.child.left
                a.child.left = b
                b.right = a.child
            # maintain degree
            a.degree += 1
            a.child_count += 1
            self.root_list_length -= 1
            # return only node still in root list
            return a
        # a.key > b.key
        else:
            # update a's neighbours to point over a
            a.left.right = a.right
            a.right.left = a.left
            # add b to child linked list of a
            if b.child is None:
                b.child = a
                # remove old left and right pointers and point to itself as is only item
                a.right = a
                a.left = a
            else:
                b.child.left.right = a
                a.left = b.child.left
                b.child.left = a
                a.right = b.child
            # maintain degree
            b.degree += 1
            b.child_count += 1
            self.root_list_length -= 1
            # return only node still in root list
            return b

    def consolidate(self):
        aux_array = [None]*(int(math.ceil(math.log(self.node_count, 2))) + 1)
        self.current = self.h_min.right
        start_node = self.current
        # set current node to correct position in auxiliary list
        aux_array[self.current.degree] = self.current
        self.current = self.current.right

        # start cycling through root list, ending when back to original current node (start node)
        k = 0
        while k < self.root_list_length:
            # check if new h_min, update if so
            if self.current.key < self.h_min.key:
                self.h_min = self.current
            # if aux pos None at current degree, just add pointer
            if aux_array[self.current.degree] is None:
                aux_array[self.current.degree] = self.current
                # move current pointer to the right
                self.current = self.current.right
            # if aux pos full, merge, clear old, check new pos, repeat
            else:
                # store next self.current
                next_current = self.current.right
                # keep merging until we get to empty pos in auxiliary array
                while aux_array[self.current.degree] is not None:
                    self.current = self.merge(aux_array[self.current.degree], self.current)
                    # remove old pointer
                    aux_array[self.current.degree - 1] = None
                # update auxiliary array
                aux_array[self.current.degree] = self.current
                # reset self.current back to next unchecked element in root list
                self.current = next_current
            k += 1


# takes input size_V = size of vertex set, edge file containing [ vertex 1  vertex 2  weight ] on each line
def kruskals(size_V, edges):

    min_heap = FibonacciHeap()
    for m in edges:
        cur_node = Node(m)
        min_heap.insert(cur_node)

    spanning_edges = []
    parent_array = [-1] * size_V

    # union-by-height with edge compression to make sure no edge we add to spanning tree forms a cycle
    def find(a):
        if parent_array[a] < 0:
            return a
        else:
            parent_array[a] = find(parent_array[a])
            return parent_array[a]

    def union(a, b):
        root_a = find(a)
        root_b = find(b)
        if root_a == root_b:
            return False

        height_a = - parent_array[root_a]
        height_b = - parent_array[root_b]
        if height_a > height_b:
            parent_array[root_b] = root_a
        elif height_b > height_a:
            parent_array[root_a] = root_b
        else:
            parent_array[root_a] = root_b
            parent_array[root_b] = -(height_b + 1)

    # get minimum spanning tree (while E < |V|-1)
    min_spanning_weight = 0
    while len(spanning_edges) < size_V - 1:
        current_edge = min_heap.extract_min()
        if union(current_edge[0], current_edge[1]) is not False:
            spanning_edges.append(current_edge)
            min_spanning_weight += current_edge[2]

    return min_spanning_weight, spanning_edges


min_spanning_weight, spanning_edges = kruskals(size_V, edges)
f = open('output_kruskals.txt', 'w')
f.write(str(min_spanning_weight) + '\n')
for item in spanning_edges:
    f.write(str(item[0]) + ' ' + str(item[1]) + ' ' + str(item[2]) + '\n')
f.close()
