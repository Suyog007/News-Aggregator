import math
import numpy as np
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize



def SplitWord(title):

    nltk_stopwords = nltk.corpus.stopwords.words('english')
    tokens = nltk.tokenize.word_tokenize(title)
    tokens = [token for token in tokens if not token in nltk_stopwords]
    
    return tokens

def ComputeTF(wordDict, bow):
    TFDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        TFDict[word] = count / float(bowCount)
    return TFDict


def ComputeIDF(docList):
    N = len(docList)
    
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))
    
    return idfDict



def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val * idfs[word]
    return tfidf


def cos_sim(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)
