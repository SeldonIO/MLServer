import numpy as np

dats = []

for i in range(100):
    a = int(np.random.random() * 100)
    b = int(np.random.random() * 100)
    c = int(np.random.random() * 100)
    op = "+"

    y = a + b + c + np.random.normal(0, 1)

    dat = {"a": a, "b": b, "c": c, "op": op, "y": y}
    dats.append(dat)

for i in range(100):
    a = int(np.random.random() * 100)
    b = int(np.random.random() * 100)
    c = int(np.random.random() * 100)
    op = "-"

    y = a - b - c + np.random.normal(0, 1)

    dat = {"a": a, "b": b, "c": c, "op": op, "y": y}
    dats.append(dat)

# for i in range(100):
#     a = int(np.random.random() * 100)
#     b = int(np.random.random() * 100)
#     c = int(np.random.random() * 100) + 1
#     op = "*"
#
#     y = a * b * c + np.random.normal(0, 1)
#
#     dat = {"a": a, "b": b, "c": c, "op": op, "y": y}
#     dats.append(dat)

import random
random.shuffle(dats)

import csv

with open("342-scripts/data.csv", "w") as f:
    writer = csv.DictWriter(f, list(dats[0].keys()))
    writer.writeheader()
    writer.writerows(dats)

