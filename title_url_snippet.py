# -*- coding: UTF-8 -*-

import os
import sys
import xml.etree.cElementTree as ET

import sys
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

base_dir = "./weps2007_data_1.1/training/web_pages"
output_dir = './training/title_url_snippet'

test_base_dir = "./weps-2-test/data/test/metadata"
test_output_dir = "./test/title_url_snippet"


def get_file_list(stage):  # 获取文件列表
    result_list = []
    if stage == "train":
        name_dirs = os.listdir(base_dir)
        file_list_r = [os.path.join(base_dir, each + '/' + each + '.xml') for each in name_dirs]
        for each_file in file_list_r:
            if os.path.exists(each_file):
                result_list.append(each_file)
    else:
        name_dirs = [file.split('.')[0] for file in os.listdir(test_base_dir)]
        result_list.extend([os.path.join(test_base_dir, each) for each in os.listdir(test_base_dir)])
    return result_list, name_dirs


def parse_file_list(stage, files, people_name):

    if stage == 'train':
        parse_output_dir = output_dir
    else:
        parse_output_dir = test_output_dir

    f_num = 0
    for each_file in files:

        tree = ET.ElementTree(file=each_file)
        corpus_ele = tree.getroot()

        # fp = open(os.path.join(parse_output_dir, people_name[f_num] + '.txt'), 'w')
        fp = codecs.open(os.path.join(parse_output_dir, people_name[f_num] + '.txt'), 'w', encoding='utf-8')
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


def ensure_dir(stage):
    if stage == 'train':
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    else:
        if not os.path.exists(test_output_dir):
            os.makedirs(test_output_dir)


if __name__ == "__main__":

    if len(sys.argv) < 2 or not (sys.argv[1] == 'train' or sys.argv[1] == 'test'):
        print "please input train or test"
        exit(0)

    # 获取文件列表
    file_list, names = get_file_list(sys.argv[1])

    # 目录不存在则创建
    ensure_dir(sys.argv[1])

    # 解析
    parse_file_list(sys.argv[1], file_list, names)

# python title_url_snippet.py train

# python title_url_snippet.py test
