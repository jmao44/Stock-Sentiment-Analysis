import pandas as pd
import numpy as np
import math
from pyhanlp import *

if __name__ == "__main__":
    file = pd.read_csv('result.csv')
    print("Total count of entries: {}".format(file.shape[0]))
    valid_titles = file[file['标题'] != "[]"]['标题']
    print("Total valid count of entries: {}".format(valid_titles.shape[0]))

    f = open('hit_stopwords.txt')
    stopwords = []
    for l in f:
        stopwords.append(l.strip())
    f.close()
    print("Total count of stopwords: {}".format(len(stopwords)))

    TermFrequency = JClass('com.hankcs.hanlp.corpus.occurrence.TermFrequency')
    TermFrequencyCounter = JClass('com.hankcs.hanlp.mining.word.TermFrequencyCounter')
    counter = TermFrequencyCounter()
    for title in valid_titles:
        counter.add(title)

    print("Total count of words: {}".format(counter.size()))

    freq_dict = {}
    for termFreq in counter:
        if termFreq.getTerm() not in stopwords:
            freq_dict[termFreq.getTerm()] = termFreq.getFrequency()
    df = pd.DataFrame.from_dict(freq_dict, orient='index', columns=['Frequency']).sort_values(by="Frequency", ascending=False)

    single_count = df[df['Frequency'] == 1].shape[0]
    threshold = (-1 + math.sqrt(1 + 8 * single_count)) / 2

    high_freq_df = df[df['Frequency'] >= threshold]
    low_freq_df = df[df['Frequency'] < threshold]

    hf_words = high_freq_df.index.values
    f = open("high_freq_words.txt", "w")
    for hf_word in hf_words:
        f.write(hf_word + '\n')
    f.close()

    print('High frequency word count: {}'.format(high_freq_df.shape[0]))
    print('Low frequency word count: {}'.format(low_freq_df.shape[0]))

    print("Top 10: ", df.head(10))


