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
        sample.py <path_freqs1> <path_freqs2> <path_targets> <path_output>

    Arguments:
        <path_freqs1>           = path to frequency list from corpus 1
        <path_freqs2>           = path to frequency list from corpus 2
        <path_targets>          = path to file containing target words
        <path_output>           = directory where the files are saved

    """)

    path_freqs1 = args['<path_freqs1>']
    path_freqs2 = args['<path_freqs2>']
    path_targets = args['<path_targets>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    freqs1 = {}
    with open(path_freqs1, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            freqs1[row[0]] = np.log2(int(row[1]))

    freqs2 = {}
    with open(path_freqs2, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            freqs2[row[0]] = np.log2(int(row[1]))

    with open(path_targets, 'r', encoding='utf-8') as f:
        targets = [line.strip() for line in f]

    intersection = freqs1.keys() & freqs2.keys()
    
    difference = [item for item in intersection if item not in targets]

    cleaned = []

    nlp = spacy.load("de_core_news_sm")

    for word in difference:
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

    area1 = {}
    area2 = {}
    area3 = {}
    area4 = {}
    area5 = {}

    for key in new_freqs:
        if new_freqs[key] < min_ + size:
            area1[key] = new_freqs[key]
        elif new_freqs[key] < min_ + 2 * size:
            area2[key] = new_freqs[key]
        elif new_freqs[key] < min_ + 3 * size:
            area3[key] = new_freqs[key]
        elif new_freqs[key] < min_ + 4 * size:
            area4[key] = new_freqs[key]    
        else:
            area5[key] = new_freqs[key]

    rel1 = len(area1) / len(new_freqs)
    rel2 = len(area2) / len(new_freqs)
    rel3 = len(area3) / len(new_freqs)
    rel4 = len(area4) / len(new_freqs)
    rel5 = len(area5) / len(new_freqs)

    sample_size1 = round(rel1 * 50)
    sample_size2 = round(rel2 * 50)
    sample_size3 = round(rel3 * 50)
    sample_size4 = round(rel4 * 50)
    sample_size5 = round(rel5 * 50)

    samples_area1 = {key:area1[key] for key in random.sample(list(area1), sample_size1)}
    samples_area2 = {key:area2[key] for key in random.sample(list(area2), sample_size2)}
    samples_area3 = {key:area3[key] for key in random.sample(list(area3), sample_size3)}
    samples_area4 = {key:area4[key] for key in random.sample(list(area4), sample_size4)}
    samples_area5 = {key:area5[key] for key in random.sample(list(area5), sample_size5)}

    samples_full = {}
    for i in [samples_area1, samples_area2, samples_area3, samples_area4, samples_area5]:
        samples_full.update(i)

    targets_freq = {key:new_freqs[key] for key in targets}
    samples_full.update(targets_freq)

    with open(path_output+'samples_full.tsv', 'w', encoding='utf-8') as f:
        for sample in samples_full:
            f.write(sample + '\n')

    with open(path_output+'freqs_full.tsv', 'w', encoding='utf-8') as f:
        for sample in samples_full:
            f.write(sample + '\t' + str(samples_full[sample]) + '\n')

    loop_dict = {1: samples_area1, 2:samples_area2, 3:samples_area3, 4:samples_area4, 5:samples_area5}

    for i in range(1,6):
        with open(path_output+'samples_area'+str(i)+'.tsv', 'w', encoding='utf-8') as f:
            for key in loop_dict[i]:
                f.write(key + '\n')

    for i in range(1,6):
        with open(path_output+'freqs_area'+str(i)+'.tsv', 'w', encoding='utf-8') as f:
            for key in loop_dict[i]:
                f.write(key + '\t' + str(loop_dict[i][key]) + '\n')


    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
