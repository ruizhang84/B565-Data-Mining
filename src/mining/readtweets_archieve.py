#!/usr/bin/env python3

import os, pickle
import numpy as np
from random import shuffle
from dataprocess import process_report, parse_tweets, prev_week, chunks

def build_key_dict(key_list):
    """
        input: a keywords list
        output: a dictionary on keywords
    """
    keys_map = {}
    for i in range(len(key_list)):
        w = key_list[i]
        keys_map[w] = i
    return keys_map

def tweets_readAll(tweet_folder_path, partition=20):
    """
        input:  a folder contains tweets
        output: tweets
        read all tweets from a folder
        and partition into seperate datasets
    """
    X_data = []
    for filename in os.listdir(tweet_folder_path):
        print("Reading {}".format(filename))
        fname = os.path.join(tweet_folder_path, filename)
        tweets = pickle.load(open(fname, "rb"))
        X_data.extend(tweets)
    shuffle(X_data)
    return X_data

def read_tweet(tweets, report, key_list, year=2017):
    """
        input: file name of tweets,
                            CDC report,
                            and keywords
        ---
        output: time by weeks,
                X and y for training predictor
    """
    # map words to array
    keys_map = build_key_dict(key_list)

    # convert tweets into matrix represent
    tf = parse_tweets(tweets, keys_map, year)

    # prepare X, y datasets
    X, y = [], []
    weeek_num = []
    for week in tf:
        if week == 1:
            continue
        # append flu info in the previous weeek
        tempX = np.append(tf[week], report[prev_week((year, week))])

        # prepare X, y datasets
        weeek_num.append(week)
        X.append(tempX)
        y.append(report[(year, week)])
    return (weeek_num, np.array(X), np.array(y))

all_tweets = tweets_readAll("/mnt/data/twitter-processed/2017-10")
print("Finished reading")
report = process_report('./ILINet.csv', 2017)
KEYWORDS = pickle.load(open("keywords-10.p", 'rb'))

weeks, X, y = [], [], []
for rnd, tweets in enumerate(chunks(all_tweets, 20)):
    print("Round {}".format(rnd))
    weeks_i, X_i, y_i = read_tweet(tweets, report, KEYWORDS)
    weeks.extend(weeks_i)
    X.extend(X_i)
    y.extend(y_i)

with open('data-10.p', 'wb') as f:
    pickle.dump((weeks, X, y), f)
