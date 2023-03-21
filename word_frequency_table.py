# constructs a table of word frequencies from a text file

import json
import re


class Corpus():
    def __init__(self,filepath=None):
        self.filename = filepath
        self.corpus = ""
        self.word_frequency_table = {}
        self.char_frequency_table = {}

    def read_corpus(self):
        """read corpus"""
        file=open(self.filename,"r",encoding="gbk")
        self.corpus = file.read()

    def process_corpus(self):
        # 去除语料库中的标点符号\数字\英文等噪音，只保留中文
        # with open("character.txt","r",encoding="gbk") as file:
        #     characters = file.read()
        with open(self.filename,"r",encoding="gbk") as file:
            # read every line as a json object
            Index = 0
            for line in file:
                line = json.loads(line)
                content = line["html"]
                # remove "原标题：" from the beginning of the content
                content = content[content.find("：")+1:]
                # append the text to corpus
                content = re.sub('[^\u4e00-\u9fa5]+', '.', content)
                for i in range(len(content)):
                    word = content[i:i+2]
                    if "." in word:
                        continue
                    elif word in self.word_frequency_table:
                        self.word_frequency_table[word] += 1
                    else:
                        self.word_frequency_table[word] = 1
                Index += 1
                if Index%1000==0:
                    print("index: ",Index)
                    print("content: ",content)

    def construct_frequency_table(self,threshold=2):
        # 从语料库中构建词频表
        self.word_frequency_table = {k:v for k,v in self.word_frequency_table.items() if v>=threshold}

    def construct_char_frequency_table(self):
        with open("charlist.txt","r",encoding="utf-8") as file:
            characters = file.read()
            character_frequency_table = {}
            for character in characters:
                character_frequency_table[character] = 0
            for character in self.corpus:
                if character in character_frequency_table:
                    character_frequency_table[character] += 1
            with open("character_frequency_table.json","w",encoding="utf-8") as file:
                json.dump(character_frequency_table,file,ensure_ascii=False)




    def output_frequency_table(self):
        # 为词频表添加额外信息
        self.outcome = {"word_frequency_table":self.word_frequency_table}
        self.outcome["total_words"] = len(self.corpus)
        self.outcome["sum_of_frequencies"] = sum(self.word_frequency_table.values())
        # 输出
        with open("word_frequency_table.json","w",encoding="utf-8") as file:
            json.dump(self.outcome,file,ensure_ascii=False)

    def run(self,filepath=None,threshold=2):
        self.__init__(filepath)
        print("Reading corpus...")
        self.read_corpus()
        print("Processing corpus...")
        self.process_corpus()
        print("Constructing frequency table...")
        self.construct_frequency_table(threshold)
        print("Outputting frequency table...")
        self.output_frequency_table()
        print("done.")
        # print("Constructing character frequency table...")
        # self.construct_char_frequency_table()

Corpus().run("2016-02.txt",threshold=10)