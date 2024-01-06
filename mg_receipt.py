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


def read_barcode():
    device = InputDevice("/dev/input/event3")
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
    p.text("ANCHORS:\n")
    p.text(mall['anchors'])
    p.text("\n")
    p.text("~"*CONFIGS['WIDTH'])
    p.text("MALL MEMORY:\n")
    p.text(mall['memory'])
    p.text("\n")
    p.set(align="right")
    p.text("-{}\n".format(mall['memory_author']))
    p.text("="*CONFIGS['WIDTH'])
    p.text("\n")
    p.set(align="center")
    p.set(align="center")
    p.text(open(CONFIGS['FOOT'],"r").read())
    p.qr(CONFIGS['QRLINK'],size=10)
    p.text("\n")
    p.set(text_type="normal")
    p.cut()


if __name__ == '__main__':
    args = parser.parse_args()
    reader = csv.DictReader(open(CONFIGS['MALLS'],"r"))
    mdb = list()
    for row in reader:
        mdb.append(row)
    if args.barcode:
        while True:
            bc = read_barcode()
            print_receipt(mdb, barcode=bc)
    else:
        print_receipt(mdb, index=args.index)
