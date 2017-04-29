# -*- coding: UTF-8 -*-
from xml.dom.minidom import Document
import os

# 格式转换为评测需要的XML格式

cluster_dir = "./training/cluster"
output_dir = "./systemsDir/TEAM_A"


def add_doc_node(cur_doc, cur_node, cur_column):  # 添加doc节点
    rank_list = cur_column.split(' ')
    for each_rank in rank_list:
        print each_rank
        each_rank = int(each_rank)
        doc_node = cur_doc.createElement('doc')
        doc_node.setAttribute('rank', str(each_rank))
        cur_node.appendChild(doc_node)


def generate_xml(person_name, file_path):  # 生成XML文件

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
                discarded_node = doc.createElement('discarded')
                clustering.appendChild(discarded_node)
                add_doc_node(doc, discarded_node, second_column)
            else:
                entity_node = doc.createElement('entity')
                entity_node.setAttribute('id', first_column)
                clustering.appendChild(entity_node)
                add_doc_node(doc, entity_node, second_column)

    # 保存文档
    f = open(os.path.join(output_dir, person_name + ".clust.xml"), 'w')
    f.write(doc.toprettyxml(encoding='utf-8'))
    f.close()


def traverse_files():
    name_files = os.listdir(cluster_dir)
    suffix = ".txt"
    for each_file in name_files:
        if each_file.endswith(suffix):  # 后缀要是.txt
            generate_xml(each_file[:-4], os.path.join(cluster_dir, each_file))

if __name__ == "__main__":
    print "begin convert  ==="

    traverse_files()  # 遍历文件

    print "conversion end ==="

# python format_conversion.py
