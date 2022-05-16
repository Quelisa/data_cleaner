# -*- coding: utf-8 -*-

from gensim.corpora.wikicorpus import extract_pages, filter_wiki
import bz2file
import re
from tqdm import tqdm
import codecs
import argparse


def wiki_replace(d):
    s = d[1]
    s = re.sub(':*{\|[\s\S]*?\|}', '', s)
    s = re.sub('<gallery>[\s\S]*?</gallery>', '', s)
    s = re.sub('(.){{([^{}\n]*?\|[^{}\n]*?)}}', '\\1[[\\2]]', s)
    s = filter_wiki(s)
    s = re.sub('\* *\n|\'{2,}', '', s)
    s = re.sub('\n+', '\n', s)
    s = re.sub('\n[:;]|\n +', '\n', s)
    s = re.sub('\n==', '\n\n==', s)
    s = u'【' + d[0] + u'】\n' + s
    return s


def wiki_process(input_file, save_path):
    wiki = extract_pages(bz2file.open(input_file))
    i = 0
    f = codecs.open(save_path, 'w', encoding='utf-8')
    w = tqdm(wiki, desc=u'0 articles have been acquired')
    for d in w:
        if not re.findall('^[a-zA-Z]+:', d[0]) and d[0] and not re.findall(
                u'^#', d[1]):
            s = wiki_replace(d)
            f.write(s + '\n\n\n')
            i += 1
            if i % 100 == 0:
                w.set_description(u'% articles have been acquired' % i)

    f.close()

def adj_1(sting, limit='【'):
    try:
        if sting.index(limit) < 1:
            result = True
        else:
            result = False
    except:
        result = False
    return result


def wiki_clean(txt_path):
    f = open(txt_path, encoding='utf-8')

    f_txt = []
    for line in f.readlines():
        f_txt.append(line)

    judge_list = []
    for txt in tqdm(f_txt):
        txt = txt.strip('\n').strip('\t').strip().strip('-').strip('#').strip()
        if '【' in txt and '】' in txt and adj_1(txt):
            continue
        elif '====' in txt and adj_1(txt, limit='===='):
            continue
        elif '===' in txt and adj_1(txt, limit='==='):
            continue
        elif '==' in txt and adj_1(txt, limit='=='):
            continue
        elif '*' in txt and adj_1(txt, limit='*'):
            continue
        elif '_' in txt and adj_1(txt, limit='_'):
            continue
        elif len(txt) < 6:
            continue
        else:
            judge_list.append(txt)

    return judge_list


def saveData(data, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for text in data:
            f.write(text + '\n')
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default=None, type=str, required=True, help="Input file for wiki dump") # wiki.xml.bz2文件存放位置
    parser.add_argument("--output_file", default=None, type=str, required=True, help="Output file for processed wiki data")
    parser.add_argument("--need_clean", default=False, type=bool, required=True, help="Is wiki need to be cleaned")
    parser.add_argument("--cleaned_file", default=None, type=str, required=False, help="Output file for cleaned wiki data")
    args = parser.parse_args()

    wiki_process(args.input_file, args.output_file)

    if args.need_clean:
        wiki_clean(args.cleaned_file)
