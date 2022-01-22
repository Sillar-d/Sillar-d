# Daniel Sillar 26879026
import sys

string_file = open(sys.argv[1])
for line in string_file:
    my_string = line
string_file.close()


# stores 'new line' in position 0, 'space' in position 1 up to 'DEL' in position 96
chars_list = [None]*97
# stores each unique character, so don't have to iterate over chars_list during insertion step
unique_characters = []


def char_to_list_index(char):
    asci = ord(char)
    # if new line character
    if asci == 10:
        return 0
    else:
        return asci - 31


class Node:
    def __init__(self):
        # self.char = str(char)     ==>   used during debugging
        self.count = 1
        self.huffman_code = None
        self.leaf = True    # true if is a character we need huffman code for, false if internal node
        self.left = None    # stores left child node when constructing tree
        self.right = None   # stores right child node
        self.next = None    # stores next smallest node (via count) in ordered prevalence linked list


# updates chars_list to store occurrence of each character
def count_chars(string):
    for char in string:
        index = char_to_list_index(char)
        # create node if none yet exists, update unique char count
        if chars_list[index] is None:
            chars_list[index] = Node()      # Node(char) is debugging and want to see labels
            unique_characters.append(char)
        # node exists, increment count
        else:
            chars_list[index].count += 1


count_chars(my_string)

# linked list of all character nodes, sorted in ascending order by occurrence
ordered_prevalence = None


def get_huffman_codes():
    # inserts character node into linked list, maintaining order
    def linked_list_insert(node, start):  # start is last node we merged, dont have to iterate over known smaller values
        global ordered_prevalence
        # list is empty, add first node
        if ordered_prevalence is None:
            ordered_prevalence = node
        # else list contains nodes already, find correct position to place
        else:
            next_node = start
            prev_node = None
            # iterate through linked list until reach node larger than one inserting or reach end of list
            while next_node is not None and next_node.count < node.count:
                prev_node = next_node
                next_node = next_node.next
            # next_node is greater than inserting node, insert node before it
            if next_node is not None:
                node.next = next_node
                # check we are not inserting at start of list
                if prev_node is not None:
                    prev_node.next = node
                # else inserting at start of list, update ordered_prevalence to point at new root
                else:
                    ordered_prevalence = node
            # else inserting node is largest in list, add to end
            else:
                prev_node.next = node

    # create ordered linked list
    for char in unique_characters:
        linked_list_insert(chars_list[char_to_list_index(char)], ordered_prevalence)  # start insert from root node as dont know any size yet

    # create binary tree
    cur_min = ordered_prevalence
    next_min = cur_min.next
    # every iteration adds 2 nodes to binary tree and 1 to linked list, so net -1 to count in linked list not yet in
    # binary tree as a child node. Hence we need to do one less iteration than number of unique chars, as final node
    # should be the root node, and hence should not be merged
    for k in range(1, len(unique_characters)):
        # create new node from two smallest nodes in tree
        internal_node = Node()          # Node(cur_min.char + next_min.char)  if want to see labels (debugging)
        # set count equal to sum of children, create sub-tree with new node as root
        internal_node.count = cur_min.count + next_min.count
        internal_node.leaf = False
        internal_node.left = cur_min
        internal_node.right = next_min
        # insert new node into ordered linked list (ordered_prevalence), starting from last known smaller node(next_min)
        linked_list_insert(internal_node, next_min)
        # update cur_min and next_min
        cur_min = next_min.next     # next_min already in binary tree, so cur_min not in tree is next smallest after
        next_min = cur_min.next
    # cur_min now points to last node in linked list, which is the root node of the binary tree
    root_node = cur_min

    # get huffman codes and add to nodes
    def recursive_labelling(node, label):
        left = node.left
        right = node.right
        # store label if leaf, else pass current label + new character to children nodes
        if left.leaf is True:
            left.huffman_code = label + '0'
        else:
            recursive_labelling(left, label + '0')

        if right.leaf is True:
            right.huffman_code = label + '1'
        else:
            recursive_labelling(right, label + '1')

    recursive_labelling(root_node, '')


# if unique characters > 1 need to get huffman codes, else can just make huffman code = 1
if len(unique_characters) > 1:
    get_huffman_codes()
else:
    chars_list[char_to_list_index(unique_characters[0])].huffman_code = '0'


# returns binary of char, set to length of 7
def char_to_binary(char):
    # returned binary string must be of length 7, so pad left with zeros
    binary_string = bin(ord(char)).replace("0b", "")
    return binary_string.rjust(7, '0')


# returns elias omega codeword of number (with binary of number at the end)
def get_elias_code(number):
    if number == 1:
        return '1'
    binary_number = bin(number).replace("0b", "")
    cur_l = str(bin(len(binary_number)-1).replace("0b", ""))
    cur_l = '0' + cur_l[1:]
    return_string = cur_l
    while len(cur_l) > 1:
        cur_l = str(bin(len(cur_l) - 1).replace("0b", ""))
        cur_l = '0' + cur_l[1:]
        return_string = cur_l + return_string
    return return_string + binary_number


# create header
# get elias omega code of number of unique characters and add to header
header = get_elias_code(len(unique_characters))
# for each character in characters: get ascii code, get Elias omega code of length of huffman code, get huffman code
for char in unique_characters:
    huff_code = chars_list[char_to_list_index(char)].huffman_code
    header += str(char_to_binary(char)) + get_elias_code(len(huff_code)) + huff_code


f = open('output_header.txt', 'w')
f.write(header)
f.close()

