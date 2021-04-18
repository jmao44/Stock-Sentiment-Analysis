import pandas as pd
import numpy as np
import math
from pyhanlp import *

if __name__ == "__main__":
    result_df = pd.read_csv('result.csv')
    valid_titles = result_df[result_df['标题'] != "[]"]['标题']
    print('Entry count:')
    print('\tTotal: {}'.format(result_df.shape[0]))
    print('\tValid: {}'.format(valid_titles.shape[0]))

    stopwords_path = 'hit_stopwords.txt'
    f = open(stopwords_path)
    stopwords = []
    for l in f:
        stopwords.append(l.strip())
    f.close()
    print('Stopword count:')
    print('\tTotal: {}'.format(len(stopwords)))

    TermFrequency = JClass('com.hankcs.hanlp.corpus.occurrence.TermFrequency')
    TermFrequencyCounter = JClass('com.hankcs.hanlp.mining.word.TermFrequencyCounter')
    counter = TermFrequencyCounter()
    for title in valid_titles:
        counter.add(title)
    print('Word count (in the entries):')
    print('\tTotal: {}'.format(counter.size()))

    freq_dict = {}
    for termFreq in counter:
        if termFreq.getTerm() not in stopwords:
            freq_dict[termFreq.getTerm()] = termFreq.getFrequency()
    df = pd.DataFrame.from_dict(freq_dict, orient='index', columns=['Frequency']).sort_values(by="Frequency", ascending=False)
    print('\tValid: {}'.format(df.shape[0]))

    single_count = df[df['Frequency'] == 1].shape[0]
    threshold = (-1 + math.sqrt(1 + 8 * single_count)) / 2
    print("Frequency threshold:")
    print("\tValue: {}".format(threshold))

    high_freq_df = df[df['Frequency'] >= threshold]
    low_freq_df = df[df['Frequency'] < threshold]

    hf_words = high_freq_df.index.values
    filepath = "high_freq_words.txt"
    f = open(filepath, "w")
    for hf_word in hf_words:
        f.write(hf_word + '\n')
    f.close()

    print('Categorized word count:')
    print('\tHigh frequency: {}'.format(high_freq_df.shape[0]))
    print('\tLow frequency: {}'.format(low_freq_df.shape[0]))
    print('High frequency words have been written to {}'.format(filepath))
