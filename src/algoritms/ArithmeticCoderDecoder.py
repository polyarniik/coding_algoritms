class ArithmeticCoderDecoder:
    def __init__(self, path, encode_path, decode_path):
        self.characters_rate = {}
        self.sections = {}
        self.characters_num = 0
        self.path = path
        self.encode_path = encode_path
        self.decode_path = decode_path
        self.splitter = "==="

    def encode(self):
        self.characters_rate.clear()
        self.sections.clear()
        self.characters_num = 0
        self.calculate_characters_rate()
        self.set_sections()
        self.write_encode_text()

    def write_encode_text(self):

        encode_path = open(self.encode_path, mode="w", encoding="UTF-8")
        for key, value in self.sections.items():
            encode_path.write(chr(key) + str(value[0]) + "\n")
            encode_path.flush()
        encode_path.write(f"{self.splitter}\n")
        encode_path.write(str(self.characters_num) + "\n")
        encode_path.flush()

        left = 0
        right = 999999999999999999
        divider = 100000000000000000
        with open(self.path, mode="r", encoding="UTF-8") as file:
            for line in file.readlines():
                line = line.replace("\n", "")
                for i in range(len(line) + 1):
                    c = ord("\n")
                    if i < len(line):
                        c = ord(line[i])
                    st = int(left + (right - left + 1) * (self.sections[c][0] / self.characters_num))
                    right = int(left + (right - left + 1) * (self.sections[c][1] / self.characters_num) - 1)
                    left = st
                    lt = int((left - left % divider) / divider)
                    rt = int((right - right % divider) / divider)
                    while lt == rt:
                        encode_path.write(format(lt, "04b"))
                        encode_path.flush()
                        left -= left - left % divider
                        left *= 10
                        right -= right - right % divider
                        right = right * 10 + 9
                        lt = int((left - left % divider) / divider)
                        rt = int((right - right % divider) / divider)

        avg = int((left + right) / 2)
        while divider != 1:
            encode_path.write(format(int(avg / divider), "04b"))
            encode_path.flush()
            avg -= avg - avg % divider
            divider //= 10

        encode_path.write(format(int(avg), "04b"))
        encode_path.flush()
        encode_path.close()

    def decode(self):
        dots = []
        characters = []
        with open(self.encode_path, mode="r", encoding="UTF-8") as encode_path:
            line = encode_path.readline().replace("\n", "")
            while line != self.splitter:
                line = line.replace("\n", "")
                if len(line) > 0:
                    c = ord(line[0])
                    dots.append(int(line[1:]))
                    characters.append(c)
                else:
                    dots.append(int(encode_path.readline().replace("\n", "")))
                    characters.append(ord("\n"))

                line = encode_path.readline().replace("\n", "")

            self.characters_num = int(encode_path.readline().replace("\n", ""))
            dots.append(self.characters_num)

            line = encode_path.readline().replace("\n", "")
            code = ""
            for i in range(0, len(line), 4):
                code += str(int(line[i: i + 4], 2))

        self.write_decode_code(dots, characters, code)

    def write_decode_code(self, dots, characters, code):
        left = 0
        right = 999999999999999999
        divider = 100000000000000000
        size = 18
        written = 0

        with open(self.decode_path, mode="w", encoding="UTF-8") as decode_file:
            while size <= len(code) and written < self.characters_num:
                frame = int(code[size - 18: size])
                index = int(((frame - left) * (self.characters_num / (right - left + 1)) - (1 / (right - left + 1))))
                i = 0
                if index > dots[-2]:
                    i = len(dots) - 2
                else:
                    for j in range(len(dots) - 2):
                        if index == dots[j]:
                            i = j
                            break
                        elif index == dots[j + 1]:
                            i = j + 1
                            break
                        elif dots[j] < index < dots[j + 1]:
                            i = j
                            break
                decode_file.write(chr(characters[i]))
                written += 1
                decode_file.flush()
                temp = int(left + (right - left + 1) * (dots[i] / self.characters_num))
                right = int(left + (right - left + 1) * (dots[i + 1] / self.characters_num) - 1)
                left = temp
                lt = int((left - (left % divider)) / divider)
                rt = int((right - (right % divider)) / divider)
                while lt == rt:
                    left -= left - (left % divider)
                    left *= 10
                    right -= right - right % divider
                    right = right * 10 + 9
                    lt = int((left - (left % divider)) / divider)
                    rt = int((right - (right % divider)) / divider)
                    size += 1

    def calculate_characters_rate(self):
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

    def set_sections(self):
        for key, value in self.characters_rate.items():
            section = [self.characters_num]
            self.characters_num += value
            section.append(self.characters_num)
            self.sections[key] = section


if __name__ == "__main__":
    alg = ArithmeticCoderDecoder("../data/war_and_peace.txt", "../data/encode.txt", "../data/decode.txt")
    alg.encode()
    alg.decode()
