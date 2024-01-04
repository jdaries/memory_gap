#!/usr/bin/env python

import argparse
import csv
import random

from escpos import config

LOGO = "Memory-Gap-B-print.jpg"
HEAD = "mg_receipt_header.txt"
WIDTH = 42
MALLS = "malls.csv"

c = config.Config()
p = c.printer()

if __name__ == '__main__':
    reader = csv.DictReader(open(MALLS,"r"))
    mall_db = list()
    for row in reader:
        mall_db.append(row)
    mall = random.choice(mall_db)
    head_text = open(HEAD,"r").read()
    p.image(LOGO)
    p.set(align="center")
    p.text(head_text)
    p.text("="*WIDTH)
    p.text("\n"*2)
    p.set(align="left")
    p.text("MALL:{m}\n".format(m=mall['name']))
    p.text("{c},{s}\n".format(c=mall['city'],s=mall['state']))
    p.text("BIRTH{:>37}\n".format(mall['birth']))
    p.text("DEATH{:>37}\n".format(mall['death']))
    p.text("~"*WIDTH)
    p.text("MALL MEMORY:\n")
    p.text(mall['memory'])
    p.text("="*WIDTH)
    p.cut()
    
