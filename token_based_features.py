#! usr/bin/python
# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup, Comment
import re
import string
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sp

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 对文本进行预处理


class PretreatmentUtil:

    def __init__(self):
        return

    def get_content(self, content):

        # 1.分割成句子
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sent = sent_tokenizer.tokenize(content)

        # 2.去掉数字标点和非字母字符
        clean_lines = [self.get_clean_lines(line.encode("utf-8")) for line in sent]

        # 3.nltk.word_tokenize分词
        words_list = [self.get_word_tokener(cl) for cl in clean_lines]

        # 4.去停用词和小写化
        clean_words = self.get_clean_words(words_list)

        # 5.使用Wordnet进行词干化
        stem_words = self.get_stem_words(clean_words)

        # 6.合并每一个句子的词成字符串
        str_line = self.words_to_str(stem_words)

        return " ".join(str_line)

    def get_clean_lines(self, line):
        identify = string.maketrans('', '')
        del_str = string.punctuation + string.digits  # ASCII 标点符号，数字
        clean_line = line.translate(identify, del_str)  # 去掉ASCII 标点符号
        return clean_line

    def get_word_tokener(self, sent):  # 将单句字符串分割成词
        words_instr = nltk.word_tokenize(sent)
        return words_instr

    def get_clean_words(self,words_list): # 去掉停用词，小写化
        clean_words = []
        stop_words = set(sp.words('english'))
        for words in words_list:
            clean_words += [[w.lower() for w in words if w.lower() not in stop_words]]
        return clean_words

    def get_stem_words(self, clean_words_list): # 取主干，如果wordnet里面没有这个词，则不操作；去掉在wordnet中长度小于3的词
        stem_words_list = []
        for words in clean_words_list:
            stem_words = []
            for word in words:
                stem_word = wn.morphy(word)

                if stem_word:

                    if len(stem_word) < 3:
                        continue
                    stem_words.append(stem_word)
                else:
                    if len(word) < 3:           # 增加了一个判断不在wordnet中的词的情况，过滤掉长度小于3的词
                        continue
                    stem_words.append(word)
            stem_words_list.append(stem_words)
        return stem_words_list

    def words_to_str(self, stem_words):
        str_line = []
        for words in stem_words:
            str_line += [w for w in words if w is not None]
        return str_line


# 获取html的所有text内容
# in: html 文件地址
# out: text


def get_clean_text(html_file, name):
    with open(html_file, 'r') as f:

        html = f.read()
        soup = BeautifulSoup(html, "lxml")

        # 去掉注释节点
        for element in soup.findAll(text=lambda text: isinstance(text, Comment)):
            element.extract()

        # 去掉script节点
        for element in soup.findAll('script'):
            element.extract()

        # 先获取html中的所有text，然后去掉空白符，注释，人名
        clean_strings = []
        for string in soup.stripped_strings:
            clean_string = (re.sub("\xa0+", " ", string, re.S))
            clean_string = (re.sub("\n+", " ", clean_string, re.S))
            clean_string = (re.sub("\s+", " ", clean_string, re.S))
            clean_string = (re.sub("<!--.*-->", "", clean_string, flags = re.S))
            if clean_string:
                clean_strings.append(clean_string)

        text = u" ".join(clean_strings)

        # 去掉text中的注释
        # text = re.sub("<!--.*-->", "", text, flags = re.S)

        # 去掉空格, html中的&nbsp;&quot;
        # text = (re.sub("\xa0+", " ", text, re.S))
        # text = (re.sub("\n+", " ", text, re.S))
        # text = (re.sub("\s+", " ", text, re.S))

        util = PretreatmentUtil()

        return util.get_content(text), util.get_content(name)
        # return text

# 定义文件夹目录
base_dir = "./weps2007_data_1.1/training/web_pages"

# 定义token的文件夹目录
token_dir = "./training"

if __name__ == "__main__":

    # 文件夹不存在
    if not os.path.exists(base_dir):
        print base_dir + " not exists"
        exit(0)

    count = 0

    for name in os.listdir(base_dir):

        # print name

        # 人名
        name_dir = os.path.join(base_dir, name)
        path_raw = os.path.join(name_dir, "raw")

        # 生成文件，一个人名的所有rank都在一个文件里
        tokens_file = os.path.join(token_dir, name + ".txt")
        tokens_wf = open(tokens_file, "w")

        if not os.path.isdir(path_raw):
            continue

        for rank in os.listdir(path_raw):

            rank_dir = os.path.join(path_raw, rank)

            if not os.path.isdir(rank_dir):
                continue

            # 解析raw html文件
            path_index_html = os.path.join(rank_dir, "index.html")
            clean_text, name_text = get_clean_text(path_index_html, name.replace("_", " "))

            # print name_text
            # 生成多个tokens文件
            # tokens_file = os.path.join(tokens_dir, rank + ".txt")
            # tokens_wf = open(tokens_file, "w")
            # tokens_wf.write(clean_text)

            # 判断是否含有人名，如果有则去掉人名，并且置is_discard=1
            name_flag = [0,0]
            name_list = name_text.split(" ")
            is_discard = 1
            clean_words = clean_text.split(" ")
            leave_words = []            # 去掉人名之后的tokens
            for word in clean_words:
                fg = 0
                for idx in range(len(name_list)):
                    if name_list[idx] == word:
                        name_flag[idx] = 1
                        fg = 1
                if fg == 0:
                    leave_words.append(word)

            clean_text = " ".join(leave_words)
            if name_flag[0] == 1 and name_flag[1] == 1:
                is_discard = 0


            # 只生成一个文件, rank id_discard clean_text
            tokens_wf.write(rank + "\t" + str(is_discard) + "\t" + clean_text + "\n")

        tokens_wf.close()
        # break

# python token_based_features.py
