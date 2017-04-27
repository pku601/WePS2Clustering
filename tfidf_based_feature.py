#! usr/bin/python
# -*- coding: UTF-8 -*-
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import os
import cPickle as pickle
import numpy as np
from scipy.linalg.misc import norm

train_dir = "./training"
tfidf_dir = "./training/tfidf"

# 计算两个向量之间的相似度


def get_similarity(a, b):
    na = np.array(a)
    nb = np.array(b)
    return np.vdot(na,nb)/(norm(na)*norm(nb))


# in: 文件
# out: 每个人名对应的所有网页的词频向量


def get_word_frequency_vector(name_file):

    # rank向量
    rank_vec = []

    # 组合所有文件的words成语料
    words_vec = []

    with open(name_file, "r") as name_read_file:

        for line in name_read_file:
            contents = line.strip('\n').split('\t')
            rank = contents[0]
            if len(contents) == 2:
                words = contents[1]
            else:
                words = []
            words_vec.append(words)
            rank_vec.append(rank)

        #将文本中的词语转换为词频矩阵
        vectorizer = CountVectorizer()

        #计算个词语出现的次数
        words_count = vectorizer.fit_transform(words_vec)

    return rank_vec, words_count.toarray()

# 计算文本的TF_IDF值 tf * log(n/nt)
# 改进：采用拉普拉斯平滑 (1+log(tf)/(1+log(avg(tf))) * log(n/nt)


def get_tfidf_vector(words_count):

    transformer = TfidfTransformer()

    #将词频矩阵X统计成TF-IDF值
    tfidf = transformer.fit_transform(words_count)

    #tfidf[i][j]表示i类文本中的第j个词的tf-idf权重
    return tfidf.toarray()


if __name__ == "__main__":

    names = os.listdir(train_dir)

    if not os.path.exists(tfidf_dir):
        os.mkdir(tfidf_dir)

    for name in names:

        # 打开每个人名的文件
        name_file = os.path.join(train_dir, name)

        if os.path.isdir(name_file):
            continue

        # 获取词频向量
        rank_vec, words_vec = get_word_frequency_vector(name_file)

        # 计算tf-idf值
        words_tfidf = get_tfidf_vector(words_vec)

        # 存储
        pickle.dump({"rank_vec": rank_vec, "words_tfidf": words_tfidf}, open(os.path.join(tfidf_dir, name.split('.')[0]+".pkl"), "w"))

