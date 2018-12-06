#!/usr/bin/env python3

import pickle
import numpy as np
from keywordstweets import gen_keyword
from readtweets_small_1 import read_data



X, y, words = read_data(tweet_fname="/Users/zhanglaoshi/Documents/Indiana/B565/B565-DataMining-Project/data/flu_smalldata/train_set_1.json",
                        dict_fname="/Users/zhanglaoshi/Documents/Indiana/B565/B565-DataMining-Project/data/words")

keywords = gen_keyword(X, y, words, 0.05)
print (keywords)
with open('./keywords_small.p', 'wb') as fw:
    pickle.dump(keywords, fw)




