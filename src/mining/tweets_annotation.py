import pickle, json, time
import numpy as np
from keywordstweets import gen_keyword
from readtweets_annotation import read_data

# X, y, words = read_data(tweet_fname="tweets_2012.txt", 
#                         label_fname="/Users/zhanglaoshi/Documents/Indiana/B565/B565-DataMining-Project/data/flu_annotations/RelatedVsNotRelated2012TweetIDs.txt",
#                         dict_fname="/Users/zhanglaoshi/Documents/Indiana/B565/B565-DataMining-Project/data/words")

# with open("temp_read_anno.p", 'wb') as f:
#     pickle.dump((X, y, words), f)


with open("temp_read_anno.p", 'rb') as f:
    X, y, words = pickle.load(f)
    start = time.time()
    keywords = gen_keyword(X, y, words, 0.05)
    print ("time is "+str(time.time()-start))
    print (keywords)

    with open('./keywords_anno.txt', 'wb') as fw:
        pickle.dump(keywords, fw)

    with open('./keywords_list_anno.txt', 'w') as fw:
        json.dump(keywords, fw)



