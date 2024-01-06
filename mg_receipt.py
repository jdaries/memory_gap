#!/usr/bin/env python

import argparse
import csv
import random

from escpos import config

LOGO = "logos/Memory-Gap-B-print.jpg"
HEAD = "mg_receipt_header.txt"
FOOT = "mg_receipt_footer.txt"
QRLINK = "https://linktr.ee/madonno_productions"
WIDTH = 42
MALLS = "malls.csv"
PHOTO_DIR = "./mall_photos"
STORY_DIR = "/mall_stories"

c = config.Config()
p = c.printer()

parser = argparse.ArgumentParser()
parser.add_argument('-i','--index', type=int,
                    help="row number (zero-indexed starting from first row of data) of the malls.csv file to use, overrides the randomness")

if __name__ == '__main__':
    args = parser.parse_args()
    reader = csv.DictReader(open(MALLS,"r"))
    mall_db = list()
    for row in reader:
        mall_db.append(row)
    if args.index is not None:
        mall = mall_db[args.index]
    else:
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
    p.text("\n")
    p.image("{}/{}".format(PHOTO_DIR,mall['photo']))
    p.text("\n")
    p.text("BIRTH:{:>36}\n".format(mall['birth']))
    p.text("DEATH:{:>36}\n".format(mall['death']))
    p.text("ANCHORS:\n")
    p.text(mall['anchors'])
    p.text("\n")
    p.text("~"*WIDTH)
    p.text("MALL MEMORY:\n")
    p.text(mall['memory'])
    p.text("\n")
    p.set(align="right")
    p.text("-{}\n".format(mall['memory_author']))
    p.text("="*WIDTH)
    p.text("\n")
    p.set(align="center")
    p.set(align="center")
    p.text(open(FOOT,"r").read())
    p.qr(QRLINK,size=10)
    p.text("\n")
    p.set(text_type="normal")
    p.cut()
    
