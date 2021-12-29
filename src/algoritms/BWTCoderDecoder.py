from collections import deque

from BaseCoderDecoder import BaseCoderDecoder


class BWTCoderDecoder(BaseCoderDecoder):
    BATCH = 1000

    def __init__(self, path, encode_path, decode_path):
        self.rotations = []
        self.alphabet = set()
        self.bwt_code = []
        self.start_index = -1
        self.path = path
        self.encode_path = encode_path
        self.decode_path = decode_path
        self.splitter = "=="

    def encode(self):
        self.clear_data()

        encode_file = open(self.encode_path, mode="w", encoding="UTF-8")
        batch = ""
        with open(self.path, mode="r", encoding="UTF-8") as file:
            for line in file.readlines():
                line = line.replace("\n", "")
                border = 0
                while border < len(line) or len(batch) == self.BATCH:
                    if (len(batch) + len(line[border:])) < self.BATCH:
                        batch += line[border:]
                        border = len(line)
                    else:
                        old_border = border
                        border += self.BATCH - len(batch)
                        batch += line[old_border:border]
                    if len(batch) == self.BATCH:
                        self.fill_batch(batch)
                        for i in self.alphabet:
                            encode_file.write(i + "\n")
                        encode_file.write(f"{self.splitter}\n")
                        encode_file.write(str(self.start_index) + "\n" + self.mtf_encode() + "\n")
                        encode_file.flush()
                        batch = ""
                        self.clear_data()

                batch += "\n"
        if len(batch) > 0:
            self.fill_batch(batch)
            for i in self.alphabet:
                encode_file.write(i + "\n")
            encode_file.flush()
            encode_file.write(f"{self.splitter}\n")
            encode_file.write(str(self.start_index) + "\n" + self.mtf_encode())

        encode_file.close()

    def decode(self):
        self.clear_data()
        encode_path = open(self.encode_path, mode="r", encoding="UTF-8")
        decode_path = open(self.decode_path, mode="w", encoding="UTF-8")
        line = encode_path.readline()
        while line:
            line = line.replace("\n", "")
            if line != self.splitter and len(line) > 0:
                self.alphabet.add(ord(line[0]))
            elif len(line) == 0:
                self.alphabet.add(ord("\n"))
            else:
                self.start_index = int(encode_path.readline().replace("\n", ""))
                self.mtf_decode(encode_path.readline().replace("\n", ""))
                sorted_alphabet_list = sorted(self.alphabet)
                indices = {}
                count = []
                for i in range(len(sorted_alphabet_list)):
                    count.append(0)
                    indices[sorted_alphabet_list[i]] = i
                for c in self.bwt_code:
                    count[indices[c]] += 1
                sum = 0
                for c in sorted_alphabet_list:
                    sum += count[indices[c]]
                    count[indices[c]] = sum - count[indices[c]]

                rev = [0 for _ in self.bwt_code]
                for i in range(len(self.bwt_code)):
                    rev[count[indices[self.bwt_code[i]]]] = i
                    count[indices[self.bwt_code[i]]] = count[indices[self.bwt_code[i]]] + 1

                index = rev[self.start_index]
                for _ in rev:
                    decode_path.write(chr(self.bwt_code[index]))
                    index = rev[index]

                self.clear_data()
            line = encode_path.readline()

        encode_path.close()
        decode_path.close()

    def clear_data(self):
        self.alphabet.clear()
        self.bwt_code.clear()
        self.rotations.clear()
        self.start_index = -1

    def fill_batch(self, batch):
        for _ in batch:
            self.rotations.append(batch)
            batch += batch[0]
            batch = batch[1::]
        self.rotations.sort()
        for i in range(len(self.rotations)):
            if self.rotations[i] == batch:
                self.start_index = i
            self.alphabet.add(self.rotations[i][0])
            self.bwt_code.append(self.rotations[i][-1])

    def mtf_encode(self):
        alphabet_deque = deque(sorted(self.alphabet))
        code = ""
        block_size = len(bin(len(self.alphabet) - 1)) - 2
        for i in self.bwt_code:
            k = alphabet_deque.index(i)
            del alphabet_deque[k]
            alphabet_deque.appendleft(i)
            character = bin(k)[2:]
            for _ in range(block_size - len(character)):
                code += "0"
            code += character
        return code

    def mtf_decode(self, code):
        alphabet_deque = deque(sorted(self.alphabet))
        block_size = len(bin(len(self.alphabet) - 1)) - 2
        for i in range(0, len(code), block_size):
            k = int(code[i : i + block_size], 2)
            c = alphabet_deque[k]
            del alphabet_deque[k]
            alphabet_deque.appendleft(c)
            self.bwt_code.append(c)


if __name__ == "__main__":
    alg = BWTCoderDecoder(
        "../data/hello.txt",
        "../data/encode.txt",
        "../data/decode.txt",
    )
    alg.encode()
    alg.decode()
