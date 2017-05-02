#! usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import scipy.cluster.hierarchy as sch
import matplotlib.pylab as plt
import cPickle as pickle
from tfidf_based_feature import get_similarity

cluster_dir = './training/cluster'
test_cluster_dir = './test/cluster'
# skirt-learn cluster


def hierarchy_clustering(name, rank_vec, words_tfidf, is_discard_vec, data_cluster_dir):

    # 生成待聚类的数据点,这里生成了20个点,每个点4维:
    # points=scipy.randn(20,4)

    # 生成点与点之间的距离矩阵,这里用的欧氏距离:
    # disMat = sch.distance.pdist(words_tfidf, 'cosine')       # 存在nan值，增加is_discard判断之后，不会出现nan值
    disMat = sch.distance.pdist(words_tfidf, 'cosine')    # cosine: 1 - u*v/(norm(u)*norm(v)),

    # print disMat.shape
    # print disMat

    # 进行层次聚类:使用min-distance
    Z = sch.linkage(disMat,method='single',metric='cosine')


    # print Z.shape
    # print Z

    # 将层级聚类结果以树状图表示出来并保存为plot_dendrogram.png
    # P = sch.dendrogram(Z)
    # plt.title('Hierarchical Clustering Dendrogram')
    # plt.savefig(os.path.join(cluster_dir, name + '.png'))

    # 根据linkage matrix Z得到聚类结果:
    # 使用 fcluster 方程获取集群信息
    cluster = sch.fcluster(Z, t=1)       # average:1.15,27   single:1.152

    # 合并rank和cluster, cluster:[rank1, rank2]
    cluster_rank = {}
    for rank in range(len(rank_vec)):
        cluster_label = cluster[rank]
        print rank, rank_vec[rank], cluster_label
        if cluster_label not in cluster_rank:
            cluster_rank[cluster_label] = []
        cluster_rank[cluster_label].append(rank_vec[rank])

    # 增加discard的类
    cluster_rank['discard'] = is_discard_vec

    # 生成pickle文件
    # pickle.dump(cluster_rank, open(os.path.join(cluster_dir, name+".pkl"), "w"))

    # 写文件
    cluster_file = os.path.join(data_cluster_dir, name+'.txt')
    with open(cluster_file, "w") as wf:
        for cluster_label, rank_list in cluster_rank.iteritems():
            # print cluster_label, rank_list
            wf.write(str(cluster_label) + '\t' + (' '.join(rank_list)) + '\n')

    # print "Original cluster by hierarchy clustering:\n",cluster

tfidf_dir = "./training/tfidf"
test_tfidf_dir = "./test/tfidf"

if __name__ == "__main__":

    if len(sys.argv) < 2 or not (sys.argv[1] == 'train' or sys.argv[1] == 'test'):
        print "please input train or test"
        exit(0)

    stage = sys.argv[1]
    if stage == 'train':
        data_tfidf_dir = tfidf_dir
        data_cluster_dir = cluster_dir
    else:
        data_tfidf_dir = test_tfidf_dir
        data_cluster_dir = test_cluster_dir

    if not os.path.isdir(data_tfidf_dir):
        print data_tfidf_dir + ' not exist.'

    if not os.path.exists(data_cluster_dir):
        os.mkdir(data_cluster_dir)

    name_files = os.listdir(data_tfidf_dir)
    for name in name_files:

        # if name != 'Guy_Crider.pkl':
        #     continue

        print name
        file_path = os.path.join(data_tfidf_dir, name)
        if not os.path.isfile(file_path):
            continue

        load_dict = pickle.load(open(file_path, "r"))

        rank_vec = load_dict['rank_vec']
        words_tfidf = load_dict['words_tfidf']
        is_discard_vec = load_dict['is_discard_vec']

        hierarchy_clustering(name.split('.')[0], rank_vec, words_tfidf, is_discard_vec, data_cluster_dir)

# python hierarchy_clustering.py train

# python hierarchy_clustering.py test
