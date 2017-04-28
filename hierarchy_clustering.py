#! usr/bin/python
# -*- coding: UTF-8 -*-

import scipy
import os
import scipy.cluster.hierarchy as sch
from scipy.cluster.vq import vq,kmeans,whiten
import numpy as np
import matplotlib.pylab as plt
import cPickle as pickle
from tfidf_based_feature import get_similarity

cluster_dir = './training/cluster'
# skirt-learn cluster


def hierarchy_clustering(name, rank_vec, words_tfidf):

    #生成待聚类的数据点,这里生成了20个点,每个点4维:
    # points=scipy.randn(20,4)

    #生成点与点之间的距离矩阵,这里用的欧氏距离:
    # disMat = sch.distance.pdist(words_tfidf, 'cosine')       # 存在nan值
    disMat = sch.distance.pdist(words_tfidf, get_similarity)    # cosine: 1 - u*v/(norm(u)*norm(v))

    # print disMat.shape
    # print disMat

    #进行层次聚类:
    Z=sch.linkage(disMat,method='average')

    # print Z.shape
    # print Z

    #将层级聚类结果以树状图表示出来并保存为plot_dendrogram.png
    P=sch.dendrogram(Z)
    plt.savefig(os.path.join(cluster_dir, name + '.png'))

    #根据linkage matrix Z得到聚类结果:
    cluster = sch.fcluster(Z, t=0.1)

    #合并rank和cluster, cluster:[rank1, rank2]
    cluster_rank = {}
    for rank in range(len(rank_vec)):
        cluster_label = cluster[rank]
        # print rank, rank_vec[rank], cluster_label
        if  cluster_label not in cluster_rank:
            cluster_rank[cluster_label] = []
        cluster_rank[cluster_label].append(rank_vec[rank])

    pickle.dump(cluster_rank, open(os.path.join(cluster_dir, name+".pkl"), "w"))

    #写文件
    cluster_file = os.path.join(cluster_dir, name+'.txt')
    with open(cluster_file, "w") as wf:
        for cluster_label, rank_list in cluster_rank.iteritems():
            # print cluster_label, rank_list
            wf.write(str(cluster_label) + '\t' + (' '.join(rank_list)) + '\n')

    # print "Original cluster by hierarchy clustering:\n",cluster

tfidf_dir = "./training/tfidf"

if __name__ == "__main__":

    if not os.path.isdir(tfidf_dir):
        print tfidf_dir + ' not exist.'

    if not os.path.exists(cluster_dir):
        os.mkdir(cluster_dir)

    name_files = os.listdir(tfidf_dir)
    for name in name_files:

        file_path = os.path.join(tfidf_dir, name)
        if not os.path.isfile(file_path):
            continue

        load_dict = pickle.load(open(file_path, "r"))

        rank_vec = load_dict['rank_vec']
        words_tfidf = load_dict['words_tfidf']

        hierarchy_clustering(name.split('.')[0], rank_vec, words_tfidf)
        break