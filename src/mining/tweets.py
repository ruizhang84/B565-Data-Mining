#!/usr/bin/env python3

import pickle
import numpy as np
from keywordstweets import gen_keyword
from readtweets_labeled import read_data



X, y, words = read_data("/Users/zhanglaoshi/Documents/Indiana/B565/Project/data/labeled_flu_related_2017-10",
                        "/Users/zhanglaoshi/Documents/Indiana/B565/Project/data/words")
with open("tmp.p", 'wb') as f:
    pickle.dump((X, y, words), f)

with open("tmp.p", 'rb') as f:
    X, y, words = pickle.load(f)
    keywords = gen_keyword(X, y, words, 0.05)
    print(keywords)
    with open('./keywords_10.p', 'wb') as fw:
        pickle.dump(keywords, fw)
