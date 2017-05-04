#! usr/bin/python
# -*- coding: UTF-8 -*-
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import os
import cPickle as pickle
import numpy as np
from scipy.linalg.misc import norm
import sys

train_dir = "./training"
tfidf_dir = "./training/tfidf"

test_dir = "./test/tokens"
test_tfidf_dir = "./test/tfidf"

# 计算两个向量之间的相似度


def get_similarity(a, b):
    na = np.array(a)
    nb = np.array(b)
    suma = sum(na)
    sumb = sum(nb)
    if  suma== 0 and sumb == 0:
        return 0
    elif suma == 0 or sumb == 0:
        return 1
    else:
        return 1 - np.vdot(na, nb)/(norm(na)*norm(nb))


# in: 文件: rank, is_discard, tokens
# out: 每个人名对应的所有网页的词频向量


def get_word_frequency_vector(name_file):

    # 只记录is_discard=0的文本的rank向量
    rank_vec = []

    # 只记录is_discard=1的文本的rank向量
    is_discard_vec = []

    # 组合所有is_discard=0的文件的words成语料
    corpus = []

    with open(name_file, "r") as name_read_file:

        for line in name_read_file:
            contents = line.strip('\n').split('\t')
            rank = contents[0]
            is_discard = contents[1]
            if len(contents) == 3:
                words = contents[2]
            else:
                words = ''
            if is_discard == '0':
                corpus.append(words)
                rank_vec.append(rank)
            else:
                is_discard_vec.append(rank)

        # 将文本中的词语转换为词频矩阵, 可以增加stop_words, max_df, min_df， 也可以使用LDA，LSA，LSI
        # Convert a collection of text documents to a matrix of token counts
        vectorizer = CountVectorizer()

        # 计算个词语出现的次数
        # Learn the vocabulary dictionary and return term-document matrix.
        words_count = vectorizer.fit_transform(corpus)

    return rank_vec, words_count.toarray(), is_discard_vec

# 计算文本的TF_IDF值 (1+log(tf)) * (1+log(n/nt)) + norm
# 改进：采用拉普拉斯平滑 (1+log(tf)/(1+log(avg(tf))) * log(n/nt)


def get_tfidf_vector(words_count):

    # Transform a count matrix to a normalized tf or tf-idf representation
    transformer = TfidfTransformer(norm=None, use_idf=True, smooth_idf=False, sublinear_tf=True)
    # transformer = TfidfTransformer(norm=True, use_idf=True, smooth_idf=True, sublinear_tf=True)

    # 将词频矩阵X统计成TF-IDF值
    tfidf = transformer.fit_transform(words_count)

    #tfidf[i][j]表示i类文本中的第j个词的tf-idf权重
    return tfidf.toarray()


if __name__ == "__main__":

    if len(sys.argv) < 2 or not (sys.argv[1] == 'train' or sys.argv[1] == 'test'):
        print "please input train or test"
        exit(0)

    stage = sys.argv[1]

    if stage == 'train':
        data_dir = train_dir
        data_tfidf_dir = tfidf_dir
    else:
        data_dir = test_dir
        data_tfidf_dir = test_tfidf_dir

    names = os.listdir(data_dir)

    if not os.path.exists(data_tfidf_dir):
        os.mkdir(data_tfidf_dir)

    for name in names:

        # 打开每个人名的文件
        name_file = os.path.join(data_dir, name)

        if os.path.isdir(name_file):
            continue

        # 获取文本中的词频向量
        rank_vec, words_vec, is_discard_vec = get_word_frequency_vector(name_file)

        # 计算tf-idf值 元素a[i][j]表示j词在第i个文本中的tf-idf权重
        words_tfidf = get_tfidf_vector(words_vec)

        # 存储
        pickle.dump({"rank_vec": rank_vec, "words_tfidf": words_tfidf, "is_discard_vec":is_discard_vec}, open(os.path.join(data_tfidf_dir, name.split('.')[0]+".pkl"), "w"))

        # break

# python tfidf_based_feature.py train

# python tfidf_based_feature.py test