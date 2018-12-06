#!/usr/bin/env python3

# This script recursively walks from the base directory, processes every json
# file based on the geo location and filters out the ones that we are interested
# in. We extract the location data and the tweet text from the json.

from data_proc.geo_filter import geo_filter
from data_proc.utils import *
from termcolor import cprint
from tqdm import tqdm
import json
import pickle
import argparse
import termcolor
import os
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('basedir', type=str, help='The base directory')
    parser.add_argument('-o', '--output', dest='output', type=str, default='results.p', help='The output file path')
    args = parser.parse_args()
    cprint('Hi! We are walking from {}'.format(args.basedir), 'blue', attrs=['bold'])
    tweet_files = []
    for dirname, subdirs, filenames in os.walk(args.basedir):
        for filename in filenames:
            if filename.endswith('.json'):  # for every json file
                full_path = os.path.join(dirname, filename)
                tweet_files.append(full_path)
    cprint('There are {} json files to process'.format(len(tweet_files)), 'blue')

    results = []
    for full_path in tqdm(tweet_files):
        year, month, date, _, _ = parse_full_path(full_path)
        week = datetime.date(int(year), int(month), int(date)).isocalendar()[1]
        tweets = []
        with open(full_path, 'r') as f:
            for line in f:
                try:
                    tweets.append(json.loads(line))
                except json.decoder.JSONDecodeError:
                    print("Oooops at file {}".format(full_path))
                    continue
        tweets_filtered = geo_filter(tuple(tweets))
        for tweet in tweets_filtered:
            results.append({'week' : week,
                            'date' : year + '-' + month + '-' + date,
                            'location' : tweet['user']['location'],
                            'text' : tweet['text']})
    cprint('{} results retrieved from {} files'.format(len(results), len(tweet_files)), 'green')
    cprint('We are outputing to {}'.format(args.output), attrs=['bold'])
    with open(args.output, 'wb') as output_f:
        pickle.dump(results, output_f)
