import datetime
import filecmp
import os

from algoritms.ArithmeticCoderDecoder import ArithmeticCoderDecoder
from algoritms.BWTCoderDecoder import BWTCoderDecoder
from algoritms.HammingCoderDecoder import HammingCoderDecoder
from algoritms.HuffmanCoderDecoder import HuffmanCoderDecoder

if __name__ == "__main__":
    algorithms = {
        "huffman": HuffmanCoderDecoder,
        "arithmetic": ArithmeticCoderDecoder,
        "bwt": BWTCoderDecoder,
        "hamming": HammingCoderDecoder,
    }

    command = input("Выберите алгоритм (huffman, arithmetic, bwt, hamming): ").strip()
    while command not in algorithms:
        print("Такого алгоритма нет!")
        command = input("Выберите алгоритм (huffman, arithmetic, bwt, hamming): ").strip()

    option = int(
        input(
            "Введите число (1. Закодировать файл. 2. Раскодировать файл. 3. Закодировать и раскодировать файл): "
        ).strip()
    )
    while option not in [1, 2, 3]:
        print("Неправильный ввод!")
        option = int(
            input(
                "Введите число (1. Закодировать файл. 2. Раскодировать файл. 3. Закодировать и раскодировать файл): "
            ).strip()
        )

    path = input("Введите абсолютный путь до файла: ").strip()
    while not os.path.isfile(path):
        print("Нет такого файла!")
        path = input("Введите путь до файла: ").strip()

    path = os.path.abspath(path)
    dir_name = os.path.dirname(path)
    alg = algorithms[command](path, os.path.join(dir_name, "encode.txt"), os.path.join(dir_name, "decode.txt"))

    start_time = datetime.datetime.now()
    if option == 1:
        alg.encode()
    elif option == 2:
        alg.decode()
    else:
        alg.encode()
        alg.decode()

    print("Сравнение:", filecmp.cmp(path, os.path.join(dir_name, "decode.txt")))
    print("Выполнено! Время выполнения: ", datetime.datetime.now() - start_time)
