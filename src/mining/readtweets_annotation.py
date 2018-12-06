import json, spacy, pickle
import numpy as np

# "python -m spacy download en"

def en_word(fname):
    """
        input: file name of words dictionary, copied from /usr/share/dict/
        output: a list of all English words
    """
    words = []
    with open(fname, 'r') as f:
        for line in f:
            s = line.strip()
            words.append(s)
    return words

def parse_tweets(tweets, words_map):
    """
        input:  a list of tweets dict, 
                dict of all English words 
                    (from words to index in array)
        output: dict {tweet_id, vector}
    """
    def vectorize(word_list, words_map):
        """
            input: a list of words, a English dictionary
            output: a vector 0/1 
            ---
            convert a list of words into a bag of words
        """
        vec_word = np.zeros(len(words_map))
        for w in word_list:
            if w not in words_map:
                continue
            idx = words_map[w]
            vec_word[idx] = 1
        return vec_word
    def tokenize(msg, nlp):
        """
            input: a tweet message in string
            output: a list of token
            ---
            tokenize a tweet
        """
        tokens = []
        doc =  nlp(msg.lower())
        for t in doc:
            tokens.append(t.lemma_)
        return tokens

    nlp = spacy.load('en')
    tweets_X = {}
    for t in tweets:
        idx = t['id']
        msg = t['text']
        tokens = tokenize(msg, nlp)
        vector = vectorize(tokens, words_map)
        tweets_X[idx] = vector
    return tweets_X

def process_tweets(tweet_fname):
    """
        input: file name of tweets json
        output: a list tweets dict
        --
        read the tweets info
    """
    data = []
    with open(tweet_fname, 'r') as f:
        data = json.load(f)
    return data

def process_labels(fname):
    """
        input: file name of tweets annotations
        output: dict{tweets_id: relevant vs not 0/1}
        ---
        read the related vs not related flu info for tweets
    """
    label = {}
    with open (fname, 'r') as f:
        for line in f:
            idx, related = line.strip().split()

            idx = int(idx)
            related = int (related)
            label[idx] = related
    return label


def read_data(tweet_fname="tweets_2009.txt", 
              label_fname="./flu_annotations/RelatedVsNotRelated2009TweetIDs.txt",
              dict_fname="words"):
    """
        input: file name of english dictionary, 
                            tweet annotations,
                            and flu relavence labels
        output: X and y datasets
    """
    tweets = process_tweets(tweet_fname)
    labels = process_labels(label_fname)
    words = en_word(dict_fname)

    words_map = {}
    for i in range(len(words)):
        w = words[i]
        words_map[w] = i

    X, y = [], []
    tweet_X = parse_tweets(tweets, words_map)
    for idx in labels:
        if idx not in tweet_X:
            continue
        X.append(tweet_X[idx])
        y.append(labels[idx])
    return (np.array(X), np.array(y), words)

  

    