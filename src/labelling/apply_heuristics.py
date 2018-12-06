#!/usr/bin/env python3

import json
import pickle
import argparse
import os

flatten = lambda l: [item for sublist in l for item in sublist]

def load_heuristics(fname):
    with open(fname, 'r') as conf_f:
        conf = json.load(conf_f)
    return flatten(conf.values())

def process(data_fname, heu):
    with open(data_fname, 'rb') as data_f:
        data = pickle.load(data_f)
    for entry in data:
        if any((h in entry['text'] for h in heu)):
            yield entry['text']

def walkdir(basedir):
    for dirname, subdirs, filenames in os.walk(basedir):
        for filename in filenames:
            if filename.endswith(".p"):
                yield os.path.join(dirname, filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('basedir', type=str, help="The base directory to walk from")
    parser.add_argument('-o', "--output", dest='output', type=str, default='.',
                        help="The output directory")
    args = parser.parse_args()
    heuristics = load_heuristics("heuristics.json")
    for fname in walkdir(args.basedir):
        output_fname = os.path.join(args.output, os.path.splitext(os.path.basename(fname))[0] + '.csv')
        with open(output_fname, 'w+') as output_f:
            for relev in process(fname, heuristics):
                output_f.write('\"' + relev.replace('\n', '').replace('\r', '').replace('\t', '').replace('\"', '') + '\",0\n')

