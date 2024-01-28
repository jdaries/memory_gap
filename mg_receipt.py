#!/usr/bin/env python

import argparse
import csv
import random

import yaml
from yaml import CLoader as Loader

from escpos import config
from evdev import InputDevice, categorize, ecodes

config_file = "config.yaml"

c = config.Config()
p = c.printer()


CONFIGS = yaml.load(open(config_file,"r"), Loader)
parser = argparse.ArgumentParser()
parser.add_argument('-i','--index', type=int,
                    help="row number (zero-indexed starting from first row of data) of the malls.csv file to use, overrides the randomness")
parser.add_argument('-b', '--barcode', action="store_true",
                    help="if set, waits for a barcode input before printing a receipt")
parser.add_argument('-r', '--random', action="store_true",
                    help="if set, prints a random barcode each time a barcode is scanned")
parser.add_argument('-k', '--keys', action="store_true",
                     help="if set, prints the photos, titles, and barcodes of all malls in database")

DEVICE = CONFIGS['DEVICE']

def print_key(mdb):
    for mall in mdb:
        p.image("{}/{}".format(CONFIGS['PHOTO_DIR'],mall['photo']))
        p.text("\n")
        p.text("+"*CONFIGS['WIDTH'])
        p.text("\n")
        p.set(align="center", text_type="b", height=2)
        p.text(mall['title'])
        p.text("\n")
        p.barcode("{}{}".format("{B",mall['code']), "CODE128", function_type="B")
        p.cut()

def read_barcode():
    device = InputDevice(DEVICE)
    code = ""
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            event = categorize(event)
            if event.keystate != 1:
                continue
            if event.keycode == "KEY_ENTER":
                return code
            code += event.keycode.split("_")[-1]


def print_receipt(mall_db, index=None, barcode=None):
    if index is not None:
        mall = mall_db[index]
    else:
        mall = random.choice(mall_db)
        if barcode is not None:
            while barcode == mall['code']:
                mall = random.choice(mall_db)
    head_text = open(CONFIGS['HEAD'],"r").read()
    p.image(CONFIGS['LOGO'])
    p.set(align="center")
    p.text(head_text)
    p.set(text_type="normal")
    p.text("="*CONFIGS['WIDTH'])
    p.text("\n")
    p.barcode("{}{}".format("{B",mall['code']), "CODE128", function_type="B")
    p.text("\n"*2)
    p.set(align="left")
    p.text("MALL:{m}\n".format(m=mall['name']))
    p.text("{c},{s}\n".format(c=mall['city'],s=mall['state']))
    p.text("\n")
    p.image("{}/{}".format(CONFIGS['PHOTO_DIR'],mall['photo']))
    p.text("\n")
    p.text("BIRTH:{:>36}\n".format(mall['birth']))
    p.text("DEATH:{:>36}\n".format(mall['death']))
    p.text("ABOUT THE MALL:\n")
    p.text(mall['anchors'])
    p.text("\n")
    p.text("="*CONFIGS['WIDTH'])
    p.text("\n")
    p.set(align="center", text_type="b")
    p.text(mall['title'])
    p.text("\n")
    p.set(text_type="normal")
    p.text("="*CONFIGS['WIDTH'])
    p.text("\n")
    p.text(mall['memory'])
    p.text("\n")
    p.set(align="right")
    p.text("-{}\n".format(mall['memory_author']))
    p.text("="*CONFIGS['WIDTH'])
    p.text("\n")
    p.set(align="center", font="b")
    p.text(open(CONFIGS['FOOT'],"r").read())
    p.qr(CONFIGS['QRLINK'],size=5)
    p.text("\n")
    p.set(text_type="normal")
    p.cut()


if __name__ == '__main__':
    args = parser.parse_args()
    reader = csv.DictReader(open(CONFIGS['MALLS'],"r", encoding="latin-1"))
    mdb = list()
    mall_mapping = dict()
    i = 0
    for row in reader:
        mdb.append(row)
        mall_mapping[row['code']] = i
        i += 1
    if args.barcode:
        while True:
            bc = read_barcode()
            ix = mall_mapping.get(bc) if not args.random else None
            print_receipt(mdb, barcode=bc, index=ix)
    elif args.keys:
        print_key(mdb)
    else:
        print_receipt(mdb, index=args.index)
