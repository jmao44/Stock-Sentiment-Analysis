import pandas as pd

def read_file(filename):
    f = open(filename)
    words = []
    for l in f:
        words.append(l.strip())
    f.close()
    return words

if __name__ == "__main__":
    negation_words = read_file('categories/negation.txt')
    negative_words = read_file('categories/negative.txt')
    neutral_words = read_file('categories/neutral.txt')
    positive_words = read_file('categories/positive.txt')
    tbd_words = read_file('categories/tbd.txt')

    

