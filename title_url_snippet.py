# -*- coding: UTF-8 -*-

import os
import xml.etree.cElementTree as ET

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

base_dir = "./weps2007_data_1.1/training/web_pages"
output_dir = './training/title_url_snippet'


def get_file_list():  # 获取文件列表
    name_dirs = os.listdir(base_dir)
    file_list_r = [os.path.join(base_dir, each + '/' + each + '.xml') for each in name_dirs]
    result_list = []
    for each_file in file_list_r:
        if os.path.exists(each_file):
            result_list.append(each_file)
    return result_list, name_dirs


def parse_file_list(files, people_name):

    f_num = 0
    for each_file in files:

        tree = ET.ElementTree(file=each_file)
        corpus_ele = tree.getroot()

        fp = open(os.path.join(output_dir, people_name[f_num] + '.txt'), 'w')
        for doc_elc in corpus_ele:

            attrib_dict = doc_elc.attrib

            if doc_elc.tag == 'doc' and 'rank' in attrib_dict:
                fp.write(attrib_dict['rank'])

            if doc_elc.tag == 'doc' and 'title' in attrib_dict:
                fp.write('\t' + attrib_dict['title'])
            else:
                fp.write('\t')

            if doc_elc.tag == 'doc' and 'url' in attrib_dict:
                fp.write('\t' + attrib_dict['url'])
            else:
                fp.write('\t')

            if len(doc_elc) == 0:
                fp.write('\t')
            else:
                for snippet_ele in doc_elc:
                    fp.write('\t' + snippet_ele.text)
            fp.write('\n')

        f_num += 1
        fp.close()


def ensure_dir(mul_dir):
    if not os.path.exists(mul_dir):
        os.makedirs(mul_dir)

if __name__ == "__main__":

    # 获取文件列表
    file_list, names = get_file_list()

    # 目录不存在则创建
    ensure_dir(output_dir)

    # 解析
    parse_file_list(file_list, names)

# python title_url_snippet.py
