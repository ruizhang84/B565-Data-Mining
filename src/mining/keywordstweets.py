from nltk.corpus import stopwords
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import chi2
from scipy.stats import wilcoxon

def sele_chi2(X, y, thresh=0.05):
    """
        input:  X, y datasets
                partition on weak and strong by means
        output: select features
    """
    _, pval= chi2(X, y)
    return pval <= thresh

def gen_keyword(X, y, words, p=0.05):
    """
        input:  training data X and y
                words array (given idx to find a word)
        output: a list of keywords
        --
        generates a list of keywords
        1) performs a wilcoxon test,
        2) filters keywords by a statistic threshold p
        3) convert idx to string for a keyword
    """
    sel = sele_chi2(X, y, p)
    words = np.array(words)
    keywords = words[sel]
    stop_words = set(stopwords.words('english'))
    return [w for w in keywords if w not in stop_words]