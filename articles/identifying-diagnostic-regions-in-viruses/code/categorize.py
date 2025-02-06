import os
import re
import random
import json

files = os.listdir("data")
random.shuffle(files)

adv_types = {
    "A": [12, 18, 31],
    "B": [3, 7, 11, 14, 16, 21, 34, 35, 50, 55],
    "C": [1, 2, 5, 6, 57],
    "D": [
        8,
        9,
        10,
        13,
        15,
        17,
        19,
        20,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        32,
        33,
        36,
        37,
        38,
        39,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        51,
        53,
        54,
        56,
        58,
        59,
        60,
        62,
        63,
        64,
        65,
        67,
        69,
        70,
        71,
        72,
        73,
        74,
        75,
    ],
    "E": [4],
    "F": [40, 41],
    "G": [52],
}


def completed_genomes():
    return [s.replace(".fasta", "") for s in os.listdir("completed_genomes")]


"""
'note': ['genotype: Ad41']}
'note': ['group: F; genotype: 41']}
note: ['genotype: 12']}
'note': ['genotype: C2']}
'note': ['genotype: F41']}
'serotype': ['31'],
'strain': ['B11'],
'isolate': ['Hu/ETH/BD298/AdV-31/2016']
strain': ['Hu/BRA/1998/HAdV-F40/RJ_LVCA1986']
"""


def loadjson(f):
    with open(f) as h:
        return json.loads(h.read())


def extract_number(text):
    match = re.search(r"(\d+)$", text)
    return int(match.group(1)) if match else None


found = {}
none = {}

for gen in completed_genomes():
    done = False
    meta = loadjson(f"data/{gen}.txt")
    note = meta.get("note")
    sero = meta.get("serotype")
    if sero:
        print("sero => ", sero)
        found[gen] = sero[0]
        done = True
    if note:
        n = extract_number(note[0])
        if n:
            for k, v in adv_types.items():
                if n in v:
                    print("note =>", note)
                    found[gen] = k
                    done = True
    if not done:
        none[gen] = meta
        # raise RuntimeError(f"No luck for {gen}")
    # print(found)

print(found.items())
# keys = set()
# for file in files[0:5]:
#     acc = file.replace(".txt", "")
#     print(acc)
#     c = loadjson(f"data/{file}")
#     print(c)
# print(keys)
