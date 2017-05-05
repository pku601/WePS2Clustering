#! usr/bin/python
# -*- coding: UTF-8 -*-
import os
from bs4 import BeautifulSoup, Comment
import re
import string
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sp

import codecs
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
        # clean_lines = [self.get_clean_lines(line.encode("utf-8")) for line in sent]
        clean_lines = [self.get_clean_line_by_sub(line.encode("utf-8")) for line in sent]


        # 3.nltk.word_tokenize分词
        words_list = [self.get_word_tokener(cl) for cl in clean_lines]

        # 4.去停用词和小写化
        clean_words = self.get_clean_words(words_list)

        # 5.使用Wordnet进行词干化
        stem_words = self.get_stem_words(clean_words)

        # 6.合并每一个句子的词成字符串
        str_line = self.words_to_str(stem_words)

        return " ".join(str_line)

    def get_clean_line_by_sub(self, line):
        sub_str = string.punctuation + string.digits + string.whitespace  # ASCII 标点符号，数字
        identify = string.maketrans(sub_str, ' '*len(sub_str))
        clean_line = line.translate(identify)  # 替换ASCII 标点符号
        return clean_line

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
    with codecs.open(html_file, 'r') as f:

        html = f.read()
        soup = BeautifulSoup(html, "lxml")

        # 去掉注释节点
        for element in soup.findAll(text=lambda text: isinstance(text, Comment)):
            element.extract()

        # 去掉script节点
        for element in soup.findAll('script'):
            element.extract()

        # 去掉style节点
        for element in soup.findAll('style'):
            element.extract()

        # 先获取html中的所有text，然后去掉空白符，注释，人名
        clean_strings = []
        for string in soup.stripped_strings:

            # print string

            # clean_string = (re.sub("<!--.*-->", "", string, flags = re.S))
            # clean_string = (re.sub("[.-\/:]+", " ", clean_string, flags = re.S))

            # clean_string = (re.sub("\xa0+", " ", clean_string, re.S))
            clean_string = (re.sub("[^a-zA-Z]", " ", string, re.S))
            clean_string = (re.sub("\s+", " ", clean_string, re.S))

            # print clean_string
            if clean_string:
                clean_strings.append(clean_string)

        text = u" ".join(clean_strings)
        util = PretreatmentUtil()
        return util.get_content(text), util.get_content(name)


def get_clean_title_snippet(file_path):
    title_snippet_dict = {}
    file = codecs.open(file_path, "r", "utf-8")
    for line in file:
        contents = line.strip('\n').split('\t')
        rank = int(contents[0])
        title = contents[1]
        url = contents[2]
        snippet = contents[3]
        text = ''
        if title:
            text = text + ' ' + title
        if snippet:
            text = text + ' ' + snippet

        text = (re.sub("[^a-zA-Z]", " ", text, re.S))
        text = (re.sub("\s+", " ", text, re.S))
        util = PretreatmentUtil()
        title_snippet_dict[rank] = util.get_content(text)
    file.close()
    return title_snippet_dict


def get_clean_title_snippet_url(file_path):
    title_snippet_dict = {}
    file = codecs.open(file_path, "r", "utf-8")
    for line in file:
        contents = line.strip('\n').split('\t')
        rank = int(contents[0])
        title = contents[1]
        url = contents[2]
        snippet = contents[3]
        text = ''
        if title:
            text = text + ' ' + title
        if snippet:
            text = text + ' ' + snippet
        if url:
            text = text + ' ' + url
        util = PretreatmentUtil()
        text = (re.sub("[^a-zA-Z]", " ", text, re.S))
        text = (re.sub("\s+", " ", text, re.S))
        title_snippet_dict[rank] = util.get_content(text)
    file.close()
    return title_snippet_dict

# 定义文件夹目录,包含html文件
base_dir = "./weps2007_data_1.1/training/web_pages"

# 定义title，url，snippet文件夹目录
title_url_snippet_dir = "./training/title_url_snippet"

# 定义token的文件夹目录
token_dir = "./training/tokens"


# 测试文件夹
test_base_dir = "./weps-2-test/data/test/web_pages"

# 定义测试的titile,url,snippet文件夹
test_title_url_snippet_dir = "./test/title_url_snippet"

# 定义test生成的token文件夹目录
test_token_dir = "./test/tokens"


def parse_train_html_data(stage_dir):

    for name in os.listdir(stage_dir):

        # print name


        # 人名
        name_dir = os.path.join(stage_dir, name)
        path_raw = os.path.join(name_dir, "raw")

        # 生成文件，一个人名的所有rank都在一个文件里
        tokens_file = os.path.join(token_dir, name + ".txt")
        tokens_wf = open(tokens_file, "w")

        if not os.path.isdir(path_raw):
            continue

        # 获取真个人名的所有rank的title，url，snippet
        title_url_snippet_file = os.path.join(title_url_snippet_dir, name+".txt")
        title_snippet_dict = get_clean_title_snippet_url(title_url_snippet_file)

        for rank in os.listdir(path_raw):

            rank_dir = os.path.join(path_raw, rank)

            if not os.path.isdir(rank_dir):
                continue

            # 解析raw html文件
            path_index_html = os.path.join(rank_dir, "index.html")
            clean_text, name_text = get_clean_text(path_index_html, name.replace("_", " "))

            # 获取title，snippet的信息
            clean_text = clean_text + " " + title_snippet_dict[int(rank)]

            # print name_text
            # 生成多个tokens文件
            # tokens_file = os.path.join(tokens_dir, rank + ".txt")
            # tokens_wf = open(tokens_file, "w")
            # tokens_wf.write(clean_text)

            # 判断是否含有人名，如果有则去掉人名，并且置is_discard=1；
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

            # tokens小于一定数量(10)，设置is_discard=1
            if len(leave_words) < 1:
                is_discard = 1

            # 只生成一个文件, rank id_discard clean_text
            tokens_wf.write(rank + "\t" + str(is_discard) + "\t" + clean_text + "\n")

        tokens_wf.close()
        # break


def parse_test_html_data(stage_dir):

    for name in os.listdir(stage_dir):

        # if not name == 'AMANDA_LENTZ':
        #     continue

        # 人名
        name_dir = os.path.join(stage_dir, name)

        # 判断文件夹是否存在
        if not os.path.exists(test_token_dir):
            os.mkdir(test_token_dir)

        # 生成文件，一个人名的所有rank都在一个文件里
        tokens_file = os.path.join(test_token_dir, name + ".txt")
        tokens_wf = open(tokens_file, "w")

        if not os.path.isdir(name_dir):
            continue

        # 获取真个人名的所有rank的title，url，snippet
        test_title_url_snippet_file = os.path.join(test_title_url_snippet_dir, name+".txt")
        test_title_snippet_dict = get_clean_title_snippet_url(test_title_url_snippet_file)

        for rank in os.listdir(name_dir):

            rank_file = os.path.join(name_dir, rank)

            if not os.path.isfile(rank_file):
                continue

            # 解析raw html文件
            path_index_html = rank_file
            clean_text, name_text = get_clean_text(path_index_html, name.replace("_", " "))

            # 获取title，snippet的信息
            clean_text = clean_text + " " + test_title_snippet_dict[int(rank.split('.')[0])]

            # print name_text
            # 生成多个tokens文件
            # tokens_file = os.path.join(tokens_dir, rank + ".txt")
            # tokens_wf = open(tokens_file, "w")
            # tokens_wf.write(clean_text)

            # 判断是否含有人名，如果有则去掉人名，并且置is_discard=1；
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

            # tokens小于一定数量(10)，设置is_discard=1
            if len(leave_words) < 1:
                is_discard = 1

            # 只生成一个文件, rank id_discard clean_text
            tokens_wf.write(rank.split('.')[0] + "\t" + str(is_discard) + "\t" + clean_text + "\n")

        tokens_wf.close()
        # break

import sys

if __name__ == "__main__":

    if len(sys.argv) < 2 or not (sys.argv[1] == 'train' or sys.argv[1] == 'test'):
        print "please input train or test"
        exit(0)

    stage = sys.argv[1]

    if stage == 'train':
        stage_dir = base_dir
    else:
        stage_dir = test_base_dir


    # 文件夹不存在
    if not os.path.exists(stage_dir):
        print stage_dir + " not exists"
        exit(0)

    if stage == 'train':
        parse_train_html_data(stage_dir)
    else:
        parse_test_html_data(stage_dir)

# python token_based_features.py train

# python token_based_features.py test


