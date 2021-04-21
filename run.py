import pandas as pd
import numpy as np
import math
from pyhanlp import *


def read_file(filename):
    f = open(filename)
    words = []
    for l in f:
        words.append(l.strip())
    f.close()
    return words


def collect_stats(filename):
    result_df = pd.read_csv(filename)
    valid_titles = result_df[result_df['标题'] != "[]"]['标题']
    valid_titles.to_csv('intermediate_data/all_titles.csv')
    print('Entry count:')
    print('\tTotal: {}'.format(result_df.shape[0]))
    print('\tValid: {}'.format(valid_titles.shape[0]))

    stopwords_path = 'hit_stopwords.txt'
    stopwords = read_file(stopwords_path)
    print('Stopword count:')
    print('\tTotal: {}'.format(len(stopwords)))

    TermFrequency = JClass('com.hankcs.hanlp.corpus.occurrence.TermFrequency')
    TermFrequencyCounter = JClass('com.hankcs.hanlp.mining.word.TermFrequencyCounter')
    counter = TermFrequencyCounter()
    for title in valid_titles:
        counter.add(title)
    print('Word count (in the entries):')
    total_word_count = counter.size()
    print('\tTotal: {}'.format(total_word_count))

    freq_dict = {}
    for termFreq in counter:
        if termFreq.getTerm() not in stopwords:
            freq_dict[termFreq.getTerm()] = termFreq.getFrequency()
    df = pd.DataFrame.from_dict(freq_dict, orient='index', columns=['Frequency']).sort_values(by="Frequency", ascending=False)
    df.to_csv('intermediate_data/word_freq.csv')
    print('\tValid: {}'.format(df.shape[0]))

    single_count = df[df['Frequency'] == 1].shape[0]
    threshold = (-1 + math.sqrt(1 + 8 * single_count)) / 2
    print("Frequency threshold:")
    print("\tValue: {}".format(threshold))

    high_freq_df = df[df['Frequency'] >= threshold]

    hf_words = high_freq_df.index.values
    filepath = "intermediate_data/high_freq_words.txt"
    f = open(filepath, "w")
    for hf_word in hf_words:
        f.write(hf_word + '\n')
    f.close()

    print('Categorized word count:')
    print('\tHigh frequency: {}'.format(high_freq_df.shape[0]))
    print('High frequency words have been written to {}'.format(filepath))


def check_combined_freq(word1, word2, all_titles):
    count = 0
    for title in all_titles:
        if word1 in title and word2 in title:
            count += 1
    return count


def pmi(word1, word2, word_freq, total_word_count, all_titles):
    p_word1 = float(word_freq.loc[word1] / total_word_count)
    p_word2 = float(word_freq.loc[word2] / total_word_count)
    p_word12 = float(check_combined_freq(word1, word2, all_titles) / total_word_count)

    val = float(p_word12 / (p_word1 * p_word2))
    if val != 0:
        return math.log(val, 2)
    return 0


def so_pmi(word, pwords, nwords, word_freq, total_word_count, all_titles):
    pmi1 = 0
    for pword in pwords:
        pmi1 += pmi(word, pword, word_freq, total_word_count, all_titles)
    pmi2 = 0
    for nword in nwords:
        pmi2 += pmi(word, nword, word_freq, total_word_count, all_titles)
    return pmi1 - pmi2


def output_so_pmi():
    nwords = read_file('categories/negative.txt')
    pwords = read_file('categories/positive.txt')
    neutral_words = read_file('categories/neutral.txt')

    word_freq = pd.read_csv('intermediate_data/word_freq.csv', index_col=0)
    all_titles = pd.read_csv('intermediate_data/all_titles.csv')['标题']
    total_word_count = word_freq['Frequency'].sum()
    print('Total word count: {}'.format(total_word_count))
    so_pmi_dict = {}
    for word in neutral_words:
        val = so_pmi(word, pwords, nwords, word_freq, total_word_count, all_titles)
        so_pmi_dict[word] = val
    # val = so_pmi('今天', pwords, nwords, word_freq, total_word_count, all_titles)
    # so_pmi_dict['今天'] = val
    print(so_pmi_dict)

    so_pmi_df = pd.DataFrame.from_dict(data=so_pmi_dict, orient='index')
    so_pmi_df.to_csv('intermediate_data/sopmi.csv')


if __name__ == '__main__':
    # collect_stats('result.csv')
    # output_so_pmi()
    print("zzz")