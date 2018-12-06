import time, datetime, spacy
import pandas as pd
import numpy as np
from collections import Counter
from datetime import date, timedelta

# chunks fun
# cite: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
def chunks(l, n):
    step = len(l) // n
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), step):
        yield l[i:i + step]

def process_report(fname, year=None):
    """
        input: a file name of Flu CDC report
        output: a gound truth y by week
    """
    data = pd.read_csv(fname, sep=",")
    data = data[['YEAR', 'WEEK', '% WEIGHTED ILI']]

    report = {}
    if year is None:
        for _, row in data.iterrows():
            year_i = row['YEAR']
            week_i = row['WEEK']
            percent_i = row['% WEIGHTED ILI']
            report[(year_i, week_i)] = percent_i
    else:
        for _, row in data.iterrows():
            year_i = row['YEAR']
            week_i = row['WEEK']
            percent_i = row['% WEIGHTED ILI']
            if int(year_i) == year:
                report[(year, week_i)] = percent_i
    return report

def tweet_week(str_time):
    """
        input: a twitter time string
        output: the week number in year
    """
    tm = time.strptime(str_time, '%a %b %d %H:%M:%S +0000 %Y')
    year, week, _ = datetime.date(tm.tm_year, tm.tm_mon, tm.tm_mday).isocalendar()
    return (year, week)

def prev_week(dates):
    """
        input: a (year, week)
        output: previous week
    """
    year, week = dates
    if week > 1:
        return (year, week-1)
    else:
        return (year-1, date(year, 12, 28).isocalendar()[1])

nlp = spacy.load('en')

def parse_tweets(tweets, keys_map, year=False):
    """
        input:  a collection of tweets,
                a map of keywords to array
                consider year (or not)
        output: a data tf contains
                1) term frequency
                2) time info
        --
        count the term freq of words by week
    """
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

    def sentence_count(sentence, w):
        """
            Count the number occurrences of a character in a string
        """
        return sentence.count(w)

    term_freq = {}

    if year:
        for tw in tweets:
            msg = tw['text']
            week = tw['week']
            if week not in term_freq:
                term_freq[week] = np.zeros(len(keys_map))

            for w in keys_map:
                term_freq[week][keys_map[w]] += sentence_count(msg, w)/len(tweets)
                
    else:
        for tw in tweets:
            year = tw['year']
            week = tw['week']
            msg = tw['text']
            tokens = tokenize(msg, nlp)
            freqs = Counter(tokens)

            if week not in term_freq:
                term_freq[(year, week)] = np.zeros(len(keys_map))
            for w in freqs:
                if w not in keys_map:
                    continue
                term_freq[(year, week)][keys_map[w]] += freqs[w]
    return term_freq
