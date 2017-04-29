#! usr/bin/python
# -*- coding: UTF-8 -*-

import cPickle as pickle
import os
from tfidf_based_feature import get_similarity
tfidf_dir = "./training/tfidf"
#
# name = "Abby_Watkins"
#
# file = os.path.join(tfidf_dir, name+".pkl")
#
# words_dict = pickle.load(open(file, "r"))
#
# rank_vec = words_dict["rank_vec"]
# words_tfidf = words_dict["words_tfidf"]
#
# # print len(words_tfidf), len(words_tfidf[0])
# print words_tfidf[0:10]
# # a = [1, 1, 0]
# # b = [1, 1, 0]
# # print get_similarity(a,b)
#
# print sum(sum(words_tfidf, 1))

from bs4 import BeautifulSoup, Comment

base_dir = "./weps2007_data_1.1/training/web_pages/Abby_Watkins/raw/010/index.html"

html = open(base_dir, "r").read()
soup = BeautifulSoup(html, "lxml")
# 去掉注释节点
for element in soup.findAll(text=lambda text: isinstance(text, Comment)):
    element.extract()

# 去掉script节点
for element in soup.findAll('script'):
    element.extract()

# 获取去空白符之后的字符串
# text = u" ".join(soup.stripped_strings)

import re
for string in soup.stripped_strings:
    text = (re.sub("\xa0+", " ", string, re.S))
    text = (re.sub("\n+", " ", text, re.S))
    text = (re.sub("\s+", " ", text, re.S))
    print repr(text)

print repr('ross                        dominique')
print repr('ambler                        bill whitt abby watkins')
