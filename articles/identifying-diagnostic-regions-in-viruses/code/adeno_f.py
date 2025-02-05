# "genotype: F
# F:

import os
import json

def loadjson(f):
    with open(f) as h:
        d = json.loads(h.read())["reports"]
        out = {}
        for r in d:
            out[r["accession"]] = r
        return out


files = os.listdir("data")
hadv = loadjson("../hadv.json")

def read(f):
    with open(f) as h:
        return h.read()


res = []
for file in files:
    txt = read(f"data/{file}")
    if "genotype: F" in txt or "F:" in txt:
        acc = file.replace(".txt", "")
        res.append({ "acc": acc, "len": hadv[acc]["length"] })

print(res)

