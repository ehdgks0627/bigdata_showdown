# -*- coding: utf-8 -*-
import sys
import json
from Crawler import *

bad = {}
good = {}
normal = {}

word_count = 0


def sensitivity_analysis(sentence):
    try:
        sentence = sentence.replace("\n", " ")
        global word_count
        word_count += len(sentence.split(" "))
        s = requests.session()
        response = s.get('http://api.datamixi.com/datamixiApi/tms?query=%s&lang=kor&analysis=om' % (sentence))
        j = json.loads(response.text)
        return j["return_object"]["sentence"][0]
    except:
        return None


datas = []

sentences = parse_letter(parse_site("선린인터넷고등학교", 100))

if not sentences:
    print("검색 결과가 없습니다.")
    sys.exit()

for sentence in sentences:
    datas.append(sensitivity_analysis(sentence))

for d in datas:
    if d == None:
        continue
    try:
        if d["sa"]["polarity"] == 1:
            for i in d["morp"]:
                if i["type"] == "NNG" or i["type"] == "NNP":
                    try:
                        good[i["lemma"]] += 1
                    except:
                        good[i["lemma"]] = 1

        elif d["sa"]["polarity"] == -1:
            for i in d["morp"]:
                if i["type"] == "NNG" or i["type"] == "NNP":
                    try:
                        bad[i["lemma"]] += 1
                    except:
                        bad[i["lemma"]] = 1
    except:
        for i in d["morp"]:
            if i["type"] == "NNG" or i["type"] == "NNP":
                try:
                    normal[i["lemma"]] += 1
                except:
                    normal[i["lemma"]] = 1

good_text = ""
bad_text = ""
normal_text = ""

for i in good.items():
    try:
        good_text += "%-5d %s\n" % (i[1], i[0])
    except:
        pass

for i in bad.items():
    try:
        bad_text += "%-5d %s\n" % (i[1], i[0])
    except:
        pass

for i in normal.items():
    try:
        normal_text += "%-5d %s\n" % (i[1], i[0])
    except:
        pass

with open("good.txt", "wb") as f:
    f.write(good_text.encode("utf-8"))

with open("bad.txt", "wb") as f:
    f.write(bad_text.encode("utf-8"))

with open("normal.txt", "wb") as f:
    f.write(normal_text.encode("utf-8"))
