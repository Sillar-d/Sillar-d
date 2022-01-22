# Daniel Sillar 26879026
import sys

string_file = open(sys.argv[1])
for line in string_file:
    my_string = line
string_file.close()


# string containing section we wish to decode, starting decoding from index
# returns decoded integer, index immediately after encoded integer
def elias_decoder(string, index):
    k = 1
    # return 1 if it is just 1
    if string[index] == '1':
        return 1, index+1

    def get_num(start_index, length):
        bin_num = ''
        # first bit is a flipped 1 (0), so we ignore it and add it at the end
        for c in range(start_index + 1, start_index + length):
            bin_num += string[c]
        bin_num = '1' + bin_num
        # add 1, as we subtract 1 when calculating L.n from len(L.n-1)
        return int(bin_num, 2) + 1

    # get index from where binary int starts (index), and index at which the length of binary int is stored (prev_index)
    cur_len = 1     # stores length of current encoded section being analysed
    while string[index] != '1':
        prev_index = index  # stores start of string containing length of binary encoded int
        index += cur_len
        cur_len = get_num(prev_index, cur_len)

    return_bin_int = ''
    for d in range(index, index + cur_len):
        return_bin_int += string[d]

    # returns number, index immediately after the elias encoding
    return int(return_bin_int, 2), index + cur_len


class Node:
    def __init__(self):
        self.char = None       # stores character associated with codeword of edges leading to node
        self.left = None
        self.right = None
    

def decode_lzss(string):
    # get number of unique characters, and the index at which the binary ascii of first character is stored
    unique_chars, char_start_index = elias_decoder(string, 0)

    # store characters in binary tree, to allow retrieval in worst case len(codeword) rather than number of codewords
    huffman_tree = Node()
    # for each character add it into the tree, with path labels to the node = huffman code of character
    for char in range(0, unique_chars):
        character = chr(int(string[char_start_index: char_start_index+7], 2))
        # get codeword length, and the start index of the codeword
        codeword_length, codeword_start_index = elias_decoder(string, char_start_index+7)
        # set where the next character starts, or data if last character (after the current codeword)
        char_start_index = codeword_start_index+codeword_length
        codeword = string[codeword_start_index: char_start_index]
        # traverse the binary tree storing the characters, adding nodes if they dont yet exist, until make leaf node
        cur_node = huffman_tree
        for num in codeword:
            if num == '0':
                if cur_node.left is None:
                    cur_node.left = Node()
                cur_node = cur_node.left
            # current digit is a 1, so go right
            else:
                if cur_node.right is None:
                    cur_node.right = Node()
                cur_node = cur_node.right
        # cur_node now stores leaf node, with path to leaf node = huffman codeword
        cur_node.char = character

    # char_start_index now stores index at which the 'data' section starts
    number_of_fields, field_start_index = elias_decoder(string, char_start_index)
    return_string = ''
    for num in range(0, number_of_fields):
        # if the current field is a 1-field
        if string[field_start_index] == '1':
            # continue reading next character and traversing associated edge in huffman_tree until reach leaf
            k = field_start_index + 1
            if string[k] == '1':
                cur_node = huffman_tree.right
            else:
                cur_node = huffman_tree.left
            # traverse down the tree until we reach a branch that doesnt exist (prefix free property of huffman code
            # implies the node we are at will then be intended character, and the next index in the string is the
            # start of the next field
            while cur_node is not None:
                prev_node = cur_node
                k = k+1
                # make sure k is still in range of string length, if not we are at end so just add prev node and end
                if k > len(string) - 1:
                    break
                elif string[k] == '1':
                    cur_node = cur_node.right
                else:
                    cur_node = cur_node.left
            # prev_node now stores our character, k stores the start index of the next field
            return_string += prev_node.char
            field_start_index = k

        # current field is a 0-field
        else:
            # decode offset into an integer, and save the start index of the length section
            offset, length_start_index = elias_decoder(string, field_start_index+1)
            # decode length into an integer, and save the start index of the next field
            length, field_start_index = elias_decoder(string, length_start_index)
            # get starting index in return string we are copying
            start_index = len(return_string) - offset
            # copy all characters dictated by the 0-field to end of the return string
            for k in range(0, length):
                return_string += return_string[start_index+k]

    return return_string


f = open('output_decoder_lzss.txt', 'w')
f.write(decode_lzss(my_string))
f.close()
