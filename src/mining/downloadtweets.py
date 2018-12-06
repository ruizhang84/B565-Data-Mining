import tweepy, json

consumer_key = "4mr1fxHElEViDWWNRelD3BuS5"
consumer_secret = "sEbZan1QuTlKUFp1s6F91JQQbjjqLaUsQZxUAcpwRrGeGZKUAD"
access_token = "144254705-LrU0BCWS2a0bWnPnBQFNzFicMEse5PtMq3LEFSPj"
access_token_secret = "L11Xxgvs5mmo3bRwTXARV8S9YutsfHA0epdszSzJdQzvQ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,  access_token_secret)
api = tweepy.API(auth)

def process_idx(fname):
    idx_list = []
    with open(fname, 'r') as f:
        for line in f:
            idx, _ = line.strip().split()
            idx = int(idx)
            idx_list.append(idx)
    return idx_list

def output_tweets(idx_list, out_fname):
    count = 0
    tweets = []
    with open (out_fname, 'w') as f:
        for idx in idx_list:
            try:
                public_tweets = api.get_status(idx)
                tweets.append(public_tweets._json)
                count += 1
                if count == 20:
                    break
            except:
                continue
        json.dump(tweets, f)

idx_list = process_idx("/Users/zhanglaoshi/Documents/Indiana/B565/B565-DataMining-Project/data/flu_annotations/RelatedVsNotRelated2009TweetIDs.txt")
output_tweets(idx_list, "tweets_2009.txt")

idx_list = process_idx("/Users/zhanglaoshi/Documents/Indiana/B565/B565-DataMining-Project/data/flu_annotations/RelatedVsNotRelated2012TweetIDs.txt")
output_tweets(idx_list, "tweets_2012.txt")


