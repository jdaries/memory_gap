#!/usr/bin/env python

import argparse
import csv
import random

import yaml
from yaml import CLoader as Loader
from escpos import config

config_file = "config.yaml"

c = config.Config()
p = c.printer()


configs = yaml.load(open(config_file,"r"), Loader)
parser = argparse.ArgumentParser()
parser.add_argument('-i','--index', type=int,
                    help="row number (zero-indexed starting from first row of data) of the malls.csv file to use, overrides the randomness")

if __name__ == '__main__':
    reader = csv.DictReader(open(configs['MALLS'],"r"))
    mall_db = list()
    for row in reader:
        mall_db.append(row)
    if args.index is not None:
        mall = mall_db[args.index]
    else:
        mall = random.choice(mall_db)
    head_text = open(configs['HEAD'],"r").read()
    p.image(config['LOGO'])
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
    
