import csv
import gzip
import logging
import random
import time

from docopt import docopt
import numpy as np
import spacy


def main():
    """
    Counts frequency of lemmas in input corpora
    """
    # Get the arguments
    args = docopt("""Counts frequency

    Usage:
        sample.py <path_freqs1> <path_freqs2> <path_output>

    Arguments:
        <path_freqs1>           = path to frequency list from corpus 1
        <path_freqs2>           = path to frequency list from corpus 2
        <path_output>           = output directory.

    """)

    path_freqs1 = args['<path_freqs1>']
    path_freqs2 = args['<path_freqs2>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    freqs1 = {}
    with open(path_freqs1, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            freqs1[row[0]] = np.log2(int(row[1]))

    freqs2 = {}
    with open(path_freqs2, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            freqs2[row[0]] = np.log2(int(row[1]))

    intersection = freqs1.keys() & freqs2.keys()

    cleaned = []

    nlp = spacy.load("de_core_news_sm")

    for word in intersection:
        doc = nlp(word)
        for token in doc:
            pos = token.pos_
        if len(doc) == 1:
            if pos == 'NOUN' or pos == 'VERB' or pos == 'ADJ':
                cleaned.append(word)

    freqs = {}
    for word in cleaned:
        freqs[word] = freqs1[word]
    
    freqs_sorted = sorted(freqs.items(), key=lambda x: x[1])

    new_freqs = {}
    for pair in freqs_sorted:
        new_freqs[pair[0]] = pair[1]
    
    max_ = list(new_freqs.values())[-1]
    min_ = list(new_freqs.values())[0]
    range_ = max_ - min_
    size = range_ / 5

    area_one = {}
    area_two = {}
    area_three = {}
    area_four = {}
    area_five = {}

    for key in new_freqs:
        if new_freqs[key] < min_ + size:
            area_one[key] = new_freqs[key]
        elif new_freqs[key] < min_ + 2 * size:
            area_two[key] = new_freqs[key]
        elif new_freqs[key] < min_ + 3 * size:
            area_three[key] = new_freqs[key]
        elif new_freqs[key] < min_ + 4 * size:
            area_four[key] = new_freqs[key]    
        else:
            area_five[key] = new_freqs[key]

    rel1 = len(area_one) / len(new_freqs)
    rel2 = len(area_two) / len(new_freqs)
    rel3 = len(area_three) / len(new_freqs)
    rel4 = len(area_four) / len(new_freqs)
    rel5 = len(area_five) / len(new_freqs)

    sample_size1 = round(rel1 * 500)
    sample_size2 = round(rel2 * 500)
    sample_size3 = round(rel3 * 500)
    sample_size4 = round(rel4 * 500)
    sample_size5 = round(rel5 * 500)
    

    # with open(path_output, 'w') as f:
    #     for pair in freqs_sorted:
    #         f.write(pair[0] + '\t' + str(pair[1]) + '\n')

    # # Write output
    # with open(path_output+'2', mode='w') as f_out:
    #     for key in new_freqs2:
    #         f_out.write(key + '\t' + str(new_freqs2[key]) + '\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
