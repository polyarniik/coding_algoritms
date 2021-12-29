import numpy as np

from BaseCoderDecoder import BaseCoderDecoder


class HammingCoderDecoder(BaseCoderDecoder):
    G = np.array(
        [[1, 1, 0, 1],
         [1, 0, 1, 1],
         [1, 0, 0, 0],
         [0, 1, 1, 1],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]]
    )
    H = np.array([[1, 0, 1, 0, 1, 0, 1],
                  [0, 1, 1, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1]])

    def __init__(self, path, encode_path, decode_path):
        self.path = path
        self.encode_path = encode_path
        self.decode_path = decode_path

    def encode(self):
        file = open(self.path, mode="r", encoding="UTF-8")
        encode_file = open(self.encode_path, mode="w", encoding="UTF-8")
        for line in file.readlines():
            res = "".join(format(i, "08b") for i in line.encode("UTF-8"))
            code = ""
            i = 4
            while i <= len(res):
                code_b = list(map(int, str(res[i - 4: i])))
                vector = np.dot(self.G, code_b, out=None)
                code += "".join([str(x) for x in np.mod(vector, 2)])
                i += 4

            encode_file.write(code)
            encode_file.flush()
        file.close()
        encode_file.close()

    def decode(self):
        with open(self.encode_path, mode="r", encoding="UTF-8") as encode_path:
            code = encode_path.read()
        decode_file = open(self.decode_path, mode="wb")
        out = []
        i = 7
        while i <= len(code):
            out.append(self.fix_wrong_bit(code[i - 7: i]))
            i += 7
        out = "".join(out)
        decode_file.write(bytes(int(out[i: i + 8], 2) for i in range(0, len(out), 8)))

    def fix_wrong_bit(self, decode_k):
        decode_k = list(map(int, str(decode_k)))
        Hk = np.dot(self.H, decode_k, out=None)
        e_string = "".join(str(i) for i in np.mod(Hk, 2))[::-1]
        if e_string != "000":
            place = int(e_string, 2)
            corrected_code = decode_k
            wrong_bit = decode_k[place - 1]
            if wrong_bit == 1:
                corrected_code[place - 1] = 0
            if wrong_bit == 0:
                corrected_code[place - 1] = 1
            corrected_code = "".join(str(i) for i in corrected_code)
            decode_k = corrected_code
            print("Ошибка в:", place, "\nНеправильный код: ", corrected_code)

        r = [decode_k[2], decode_k[4], decode_k[5], decode_k[6]]
        return "".join([str(x) for x in r])


if __name__ == "__main__":
    alg = HammingCoderDecoder("../data/test.txt", "../data/encode.txt", "../data/decode.txt")
    alg.encode()
    alg.decode()
