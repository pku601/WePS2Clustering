# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Comment
import re

import os
import sys

base_dir = "../training/web_pages"

def clean_document(path_index_html):
	print path_index_html
	fp = open(path_index_html, "r")
	try:
		html_doc = fp.read()
		soup = BeautifulSoup(html_doc, "lxml")
		for element in soup(text=lambda text: isinstance(text, Comment)):
		    element.extract()
		all_text = "".join(soup.stripped_strings)
		# all_text = soup.get_text()
		all_text = re.sub("<!--(.*?)-->", "", all_text, flags = re.S)
	finally:
		fp.close()
	return all_text

if __name__ == "__main__":
    print "main begin"
    if not os.path.exists(base_dir):
		print base_dir + "not exists"
    	exit()
    count = 0
    for lists in os.listdir(base_dir):
        path = os.path.join(base_dir, lists)
        path_raw = os.path.join(path, "raw")
        for dirs in os.listdir(path_raw):
        	count += 1
        	if count == 5:
        		exit()
        	tmp_dir = os.path.join(path_raw, dirs)
        	path_index_html = os.path.join(tmp_dir, "index.html")
        	all_text = clean_document(path_index_html)
        	print all_text
    print "main end"
