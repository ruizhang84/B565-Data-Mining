import os, codecs
import numpy as np
from textmining import en_word, parse_tweets

def read_labeled_csv(labeled_fname, delimitor=","):
    """
        input: file name of labled tweets csv
        output: tweets with label
        --
        read the flu labled tweets
    """
    def extract_label(tweet):
        """
            input: a tweet
            output: a message and corresponding label
        """
        for i in reversed(tweet):
            if i == '0':
                return 0
            elif i == '1':
                return 1
        return None

    X_data = []
    y_data = []
    with codecs.open(labeled_fname, "r",
        encoding='utf-8', errors='ignore') as f:
        for line in f:
            tweet = line.strip()
            label = extract_label(tweet)
            if label is None:
                continue
            X_data.append(tweet)
            y_data.append(label)
    return (X_data, y_data)

def process_data(folder_path):
    """
        input: a folder path
        output: tweets with labels from all files in the folder
    """
    X = []
    y = []
    for filename in os.listdir(folder_path):
        fname = os.path.join(folder_path, filename)
        X_data, y_data = read_labeled_csv(fname)
        X.extend(X_data)
        y.extend(y_data)
    return (np.array(X), np.array(y))

def filter_words(X, words):
    """
        input:  X datasets
                words array
        output: a new X datasets
                with no appearance words removed
        --
        reduce X dimension by removing words
    """
    X_filtered = np.array([])
    words_filtered = []
    _, n_words = X.shape
    for i in range(n_words):
        if np.sum(X[:,i]) == 0:
            continue
        if len(X_filtered) == 0:
            X_filtered = X[:,i]
            words_filtered.append(words[i])
            continue
        X_filtered = np.vstack((X_filtered, X[:, i]))
        words_filtered.append(words[i])
    X_filtered = np.swapaxes(X_filtered, 0, 1)
    return (X_filtered, words_filtered)

def read_data(folder_path, dict_fname):
    """
        input: a folder path for labeled tweets
        output: X and y datasets
    """
    X, y = process_data(folder_path)
    words, words_map = en_word(dict_fname)
    X = parse_tweets(X, words_map)
    X, words = filter_words(X, words)

    print (X.shape)
    print ("finish reading!")
    return (X, y, words)
