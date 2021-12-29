import os
import queue

from BaseCoderDecoder import BaseCoderDecoder


class Node:
    def __init__(self, value, rate, left=None, right=None):
        self.value = value
        self.rate = rate
        self.left = left
        self.right = right

    def __gt__(self, other):
        return self.rate > other.rate

    def __lt__(self, other):
        return self.rate < other.rate

    def __eq__(self, other):
        return self.rate == other.rate


class HuffmanCoderDecoder(BaseCoderDecoder):
    def __init__(self, path, encode_path, decode_path):
        self.characters_rate = {ord("\n"): 0}
        self.codes = {}
        self.path = path
        self.encode_path = encode_path
        self.decode_path = decode_path
        self.splitter = "==="

    def encode(self):
        self.calculate_rate()
        root = self.get_bitree()
        self.get_code_dict(root, "")
        with open(self.encode_path, mode="w", encoding="UTF-8") as file:
            for value, code in self.codes.items():
                file.write(chr(value) + code + "\n")
            file.write(f"{self.splitter}\n")

            with open(self.path, mode="r+") as code_file:
                for line in code_file.readlines():
                    for i in line.replace("\n", ""):
                        file.write(self.codes[ord(i)])
                    file.write(self.codes[ord("\n")])

    def decode(self):
        characters = dict()
        code_file = open(self.encode_path, mode="r", encoding="UTF-8")
        decode_file = open(self.decode_path, mode="w", encoding="UTF-8")
        line = code_file.readline().replace("\n", "")
        while line != self.splitter:
            if line == "":
                characters[code_file.readline().replace("\n", "")] = "\n"
            if len(line) > 0:
                c = line[0].replace("\n", "")
                characters[line[1:].replace("\n", "")] = c
            line = code_file.readline().replace("\n", "")
        line = code_file.readline()
        if line:
            code = ""
            for i in line:
                code += i
                if code in characters:
                    decode_file.write(characters[code])
                    code = ""

    def calculate_rate(self):
        with open(self.path, mode="r", encoding="UTF-8") as file:
            self.characters_rate[ord("\n")] = 0
            for line in file.readlines():
                line = line.replace("\n", "")
                for c in line:
                    c = ord(c)
                    if c in self.characters_rate:
                        self.characters_rate[c] += 1
                    else:
                        self.characters_rate[c] = 1
                self.characters_rate[ord("\n")] += 1

    def get_bitree(self):
        huffman_queue = queue.PriorityQueue()
        for value, rate in self.characters_rate.items():
            huffman_queue.put(Node(value, rate))

        root = None
        while huffman_queue.qsize() > 0:
            left = huffman_queue.get()
            if huffman_queue.qsize() > 0:
                right = huffman_queue.get()
                root = Node(ord("\0"), left.rate + right.rate, left, right)
            else:
                root = Node(ord("\0"), left.rate, left)
            if huffman_queue.qsize() > 0:
                huffman_queue.put(root)
            else:
                return root
        return root

    def get_code_dict(self, node, code):
        if node:
            if node.left and node.right:
                self.get_code_dict(node.left, code + "0")
                self.get_code_dict(node.right, code + "1")
            else:
                self.codes[node.value] = code


if __name__ == "__main__":
    alg = HuffmanCoderDecoder("../data/test.txt", "../data/encode.txt", "../data/decode.txt")
    alg.encode()
    alg.decode()
