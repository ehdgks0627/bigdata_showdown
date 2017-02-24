import requests
import json
from pprint import pprint

bad = {}
good = {}

word_count = 0

def sensitivity_analysis(sentence):
    sentence = sentence.replace("\n", " ")
    global word_count
    word_count += len(sentence.split(" "))
    s = requests.session()
    response = s.get('http://api.datamixi.com/datamixiApi/tms?query=%s&lang=kor&analysis=om' % (sentence))
    j = json.loads(response.text)
    return j["return_object"]["sentence"][0]


d = sensitivity_analysis("""""")

if d["sa"]["polarity"] == 1:
    for i in d["word"]:
        if "NNG" in i["tagged_text"]:
            try:
                good[i["text"]] += 1
            except:
                good[i["text"]] = 1

elif d["sa"]["polarity"] == -1:
    for i in d["word"]:
        if "NNG" in i["tagged_text"]:
            try:
                bad[i["text"]] += 1
            except:
                bad[i["text"]] =1
good_text = ""
bad_text = ""

for i in good.items():
    good_text += "%s %d\n"%(i[0], i[1])

for i in bad.items():
    bad_text += "%s %d\n"%(i[0], i[1])

with open("good.txt", "w") as f:
    f.write(good_text)

with open("bad.txt", "w") as f:
    f.write(bad_text)