import requests
import random
from hashlib import md5
import time
from tqdm import tqdm
import argparse


def baidu_translate(query, from_lang, to_lang, appid='20220516001217727', appkey='bbwv3ufCQkn9_Am1SDOO'):
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    # Generate salt and sign
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    trans = ""
    # Send request
    try:
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()
        if "trans_result" in result and "dst" in result["trans_result"][0]:
            trans = result["trans_result"][0]["dst"]
            time.sleep(1)
        else:
            print("[inner error:"+query+"]")
            time.sleep(1)
    except Exception as e:
        print("[outer error:"+query+"]")
        time.sleep(3)
    return trans

def loadData(filename):
    data = []
    with open(filename, "r", encoding="UTF-8") as f:
        for line in f:
            line = line.strip('\n').strip()
            data.append(line)
    f.close()
    return data

def translate(data, source, target):
    trans_data = []
    for sent in tqdm(data):
        sent_trans = baidu_translate(sent, source, target)
        print("sent_trans:", sent_trans)
        if sent_trans != "":
            trans_data.append(sent_trans)
    return trans_data

def saveData(data, filename):
    with open(filename,"w",encoding="UTF-8") as f:
        for sent in data:
            f.write(sent+"\n")
    f.close()

def main(args):
    data = loadData(args.input_file)
    trans_data = translate(data, args.source_language, args.target_language)
    saveData(trans_data, args.output_file)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default=None, type=str, help="input file to be translated")
    parser.add_argument("--output_file", default=None, type=str, help="output file for translated data")
    parser.add_argument("--source_language", default="zh", type=str, help="source language type")
    parser.add_argument("--target_language", default="yue", type=str, help="target language type")
    args = parser.parse_args()

    main(args)
