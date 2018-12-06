import spacy
import numpy as np

# "python -m spacy download en"

def en_word(fname):
    """
        input:  file name of words dictionary, 
                copied from /usr/share/dict/
        output: a list of all English words
                a map from words to index
    """
    words = []
    with open(fname, 'r') as f:
        for line in f:
            s = line.strip()
            words.append(s)
    words_map = {}
    for i in range(len(words)):
        w = words[i]
        words_map[w] = i
    return (words, words_map)

nlp = spacy.load('en_default')

def parse_tweets(tweets, words_map):
    """
        input:  a list of tweets, 
                dict of all English words 
                    (from words to index in array)
        output: X - a list of tweet vectors
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

    X = []
    for msg in tweets:
        tokens = tokenize(msg, nlp)
        vector = vectorize(tokens, words_map)
        X.append(vector)
    return np.array(X)
