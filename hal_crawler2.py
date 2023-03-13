#!/usr/bin/env python
# This top line makes it possible to run this from sbatch

# HAL French Thesis web crawler
# Author: @Richard Yue
# e-mail richard.samuel.yue@outlook.com

import requests
from bs4 import BeautifulSoup
import io,os,re,sys,json,argparse
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfReader 

parser = argparse.ArgumentParser()
parser.add_argument("-q", "--query", help="French phrase", required=True)
parser.add_argument("-N", "--number_of_urls", type=int, help="defaults to 10k", default=10000)
parser.add_argument("-O", "--output", help="output directory", required=True)
args = parser.parse_args()

url_str = 'http://api.archives-ouvertes.fr/search/?q=' + args.query + '&wt=xml&rows=' + str(args.number_of_urls)

def get_abstract_en(url):
    try:
        # print(f"Getting EN abstract from page: {url}")
        html_content = requests.get(url).text
        page_soup = BeautifulSoup(html_content, 'html.parser')
        abstract_en = page_soup.findAll("div",{"class":"abstract-content en"})
        
        if len(abstract_en) > 0:
            return abstract_en[0].text
        else:
            return None
    except:
        # print('get_abstract_en failed')
        return None

def get_abstract_fr(url):
    try:
        # print(f"Getting FR abstract from page: {url}")
        html_content = requests.get(url).text
        page_soup = BeautifulSoup(html_content, 'html.parser')
        abstract_fr = page_soup.findAll("div",{"class":"abstract-content fr active"})
    
        if len(abstract_fr) > 0:
            return abstract_fr[0].text
        else:
            return None
    except:
        # print('get_abstract_fr failed')
        return None

def main():
    req = requests.get(url_str)
    soup = BeautifulSoup(req.content, "xml")

    # print(soup.prettify())
    # print(soup.get_text())
    
    doc_urls = soup.findAll("str",{"name":"uri_s"})

    # for url in doc_urls:
    doc_num = 1
    for i,doc_url in enumerate(doc_urls):
        try:
            dir = '%s/%03d' % (args.output, i % 1000)
            if not os.path.exists(dir):
                os.makedirs(dir)
            if abstract_en and abstract_fr:
                with open(dir + '/%06d.json' % i, 'w') as fd:
                    j = { 'url' : doc_url.text ,
                          'abstract_en' : get_abstract_en(doc_url.text),
                          'abstract_fr' : get_abstract_fr(doc_url.text)}
                    fd.write(json.dumps(j))
        except:
            continue


if __name__ == "__main__":
    main()
