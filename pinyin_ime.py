""" an ime for pinyin to chinese characters"""
import sys
import json
import math


class character_node:
    def __init__(self, character=None, frequency=0):
        self.character = character
        self.frequency = frequency
        self.last = None
        self.last_index = -1
        self.sum_of_log_of_probability = 0
        self.sum_of_frequency = 0
        self.py = None


class Pinyin:
    def __init__(self):
        self.pinyin = {}
        self.chinese = {}
        self.py2hz = {}
        self.frequency_table = {}
        self.total_words = 0
        self.total_frequency = 0
        self.char_frequency_table = {}
        self.read_databases()

    def read_databases(self):
        """read databases"""
        # self.pinyin = open("pinyin.txt", "r")
        with open("py2hz.txt", "r", encoding="gbk") as file:
            for line in file.readlines():
                line = line.strip()
                if line == "":
                    continue
                hz = line.split(" ")
                # get the first character as the key(py)
                py = hz[0]
                hz = hz[1:]
                self.py2hz[py] = hz

        with open("word_frequency_table.json", "r", encoding="utf-8") as file:
            frequency_json = json.load(file)
            self.frequency_table = frequency_json.get("word_frequency_table")
            self.total_words = frequency_json.get("total_words")
            self.total_frequency = frequency_json.get("sum_of_frequencies")

        with open("character_frequency_table.json", "r", encoding="utf-8") as file:
            self.char_frequency_table = json.load(file)

    def print_table(self, table):
        for list in table:
            print("=====================================")
            for node in list:
                print(
                    "character: ",
                    node.character,
                    "frequency: ",
                    node.frequency,
                    "last: ",
                    node.last,
                    "last_index: ",
                    node.last_index,
                    "sum_of_log_of_probability: ",
                    node.sum_of_log_of_probability,
                    "sum_of_frequency: ",
                    node.sum_of_frequency,
                    "py: ",
                    node.py,
                )

    def viterbi_agorithms(self, pinyin_list):
        """Viterbi algorithms"""
        # initialize
        tmp_list = []
        for pinyin in pinyin_list:
            character_node_list = []
            for character in self.py2hz[pinyin]:
                node = character_node(character)
                node.py = pinyin
                character_node_list.append(node)
            tmp_list.append(character_node_list)

        for character_list in tmp_list[1:]:
            prev_list = tmp_list[tmp_list.index(character_list) - 1]
            for character in character_list:
                tmp_min_sum_frequency = sys.maxsize #infinity
                for last_character in prev_list:
                    word = last_character.character + character.character
                    if word in self.frequency_table:
                        frequency = self.frequency_table[word]
                    else:
                        frequency = 1
                    frequency = frequency / self.total_frequency
                    frequency = -1 * math.log(frequency)
                    sum_frequency = last_character.sum_of_frequency + frequency
                    if sum_frequency < tmp_min_sum_frequency:
                        tmp_min_sum_frequency = sum_frequency
                        character.last_index = prev_list.index(last_character)
                        character.sum_of_frequency = sum_frequency
                    else:
                        continue

        # self.print_table(tmp_list)
        # get the best result

        last_character_list = tmp_list[-1]
        min_sum_frequency = sys.maxsize
        last_index = -1
        for character in last_character_list:
            if character.sum_of_frequency < min_sum_frequency:
                min_sum_frequency = character.sum_of_frequency
                last_index = last_character_list.index(character)
            else:
                continue

        # print the result
        path = []
        length = len(tmp_list)
        while length > 0:
            length -= 1
            last_character = tmp_list[length][last_index]
            path.append(last_character.character)
            last_index = last_character.last_index

        path.reverse()
        # translate to chinese string
        chinese_string = ""
        for character in path:
            chinese_string += character

        return chinese_string

    def read_input(self, input_file):
        """read input"""
        with open(input_file, "r") as file:
            with open("output.txt", "w", encoding="utf-8") as output_file:
                for line in file:
                    line = line.strip()
                    pinyin_list = line.split(" ")
                    answer = self.viterbi_agorithms(pinyin_list)
                    output_file.write(answer + "\n")

    def run(self):
        """run"""
        print("running...")
        print("reading databases...")
        self.__init__()
        self.read_databases()
        print("reading input...")
        self.read_input("input.txt")


if __name__ == "__main__":
    pinyin = Pinyin()
    pinyin.run()
