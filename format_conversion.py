# -*- coding: UTF-8 -*-
from xml.dom.minidom import Document
import os
import sys

# 格式转换为评测需要的XML格式

cluster_dir = "./training/cluster"
output_dir = "./systemsDir/TEAM_A"

test_cluster_dir = "./test/cluster"
test_output_dir = "./systemsDir/TEAMTest"


def add_doc_node(cur_doc, cur_node, cur_column):  # 添加doc节点
    rank_list = cur_column.split(' ')
    for each_rank in rank_list:
        # print each_rank
        each_rank = int(each_rank)
        doc_node = cur_doc.createElement('doc')
        doc_node.setAttribute('rank', str(each_rank))
        cur_node.appendChild(doc_node)


def generate_xml(person_name, file_path, data_output_dir):  # 生成XML文件

    doc = Document()  # 创建DOM文档对象
    clustering = doc.createElement('clustering')  # 创建根元素
    clustering.setAttribute("name", person_name)
    doc.appendChild(clustering)  # 创建节点后，还需要添加到文档中才有效

    with open(file_path, "r") as fp:
        for line in fp:
            contents = line.strip('\n').split('\t')
            if len(contents) != 2:
                continue
            first_column = contents[0]
            second_column = contents[1]
            if first_column == "discard":
                if second_column != "":
                    discarded_node = doc.createElement('discarded')
                    clustering.appendChild(discarded_node)
                    add_doc_node(doc, discarded_node, second_column)
            else:
                entity_node = doc.createElement('entity')
                entity_node.setAttribute('id', first_column)
                clustering.appendChild(entity_node)
                add_doc_node(doc, entity_node, second_column)

    # 保存文档
    f = open(os.path.join(data_output_dir, person_name + ".clust.xml"), 'w')
    f.write(doc.toprettyxml(encoding='utf-8'))
    f.close()


def traverse_files(data_cluster_dir, data_output_dir):
    name_files = os.listdir(data_cluster_dir)
    suffix = ".txt"
    for each_file in name_files:
        if each_file.endswith(suffix):  # 后缀要是.txt
            generate_xml(each_file[:-4], os.path.join(data_cluster_dir, each_file), data_output_dir)


def ensure_dir(mul_dir):
    if not os.path.exists(mul_dir):
        os.makedirs(mul_dir)

if __name__ == "__main__":

    if len(sys.argv) < 2 or not (sys.argv[1] == 'train' or sys.argv[1] == 'test'):
        print "please input train or test"
        exit(0)

    stage = sys.argv[1]
    if stage == 'train':
        data_cluster_dir = cluster_dir
        data_output_dir = output_dir
    else:
        data_cluster_dir = test_cluster_dir
        data_output_dir = test_output_dir

    ensure_dir(data_output_dir)  # 目录不存在则创建
    traverse_files(data_cluster_dir, data_output_dir)  # 遍历文件

# python format_conversion.py train

# python format_conversion.py test
