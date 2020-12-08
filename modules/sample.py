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

    # Load frequencies
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

    # Load target words
    with open(path_targets, 'r', encoding='utf-8') as f:
        targets = [line.strip() for line in f]

    # Make intersection and remove targets from the list 
    intersection = freqs1.keys() & freqs2.keys()
    difference = [item for item in intersection if item not in targets]

    # Clean list with pos_tagging. Only NOUNs, VERBs and ADJs survive. 
    cleaned = []
    nlp = spacy.load("de_core_news_sm")
    for word in difference:
        doc = nlp(word)
        for token in doc:
            pos = token.pos_
        if len(doc) == 1:
            if pos == 'NOUN' or pos == 'VERB' or pos == 'ADJ':
                cleaned.append(word)

    # Convert to dict and get frequencies from freqs1 
    freqs_cleaned = {}
    for word in cleaned:
        freqs_cleaned[word] = freqs1[word]
    
    # Sort by freqeuncy and convert back to dict
    sorted_tmp = sorted(freqs_cleaned.items(), key=lambda x: x[1])
    freqs_sorted = {}
    for pair in sorted_tmp:
        freqs_sorted[pair[0]] = pair[1]
    
    # Compute range and area_size
    max_ = list(freqs_sorted.values())[-1]
    min_ = list(freqs_sorted.values())[0]
    range_ = max_ - min_
    size = range_ / 5

    # Create and fill areas accordingly
    area1 = {}
    area2 = {}
    area3 = {}
    area4 = {}
    area5 = {}

    for key in freqs_sorted:
        if freqs_sorted[key] < min_ + size:
            area1[key] = freqs_sorted[key]
        elif freqs_sorted[key] < min_ + 2 * size:
            area2[key] = freqs_sorted[key]
        elif freqs_sorted[key] < min_ + 3 * size:
            area3[key] = freqs_sorted[key]
        elif freqs_sorted[key] < min_ + 4 * size:
            area4[key] = freqs_sorted[key]    
        else:
            area5[key] = freqs_sorted[key]

    # Compute percentages to determine how many samples to take from each area
    rel1 = len(area1) / len(freqs_sorted)
    rel2 = len(area2) / len(freqs_sorted)
    rel3 = len(area3) / len(freqs_sorted)
    rel4 = len(area4) / len(freqs_sorted)
    rel5 = len(area5) / len(freqs_sorted)

    sample_size1 = round(rel1 * 500)
    sample_size2 = round(rel2 * 500)
    sample_size3 = round(rel3 * 500)
    sample_size4 = round(rel4 * 500)
    sample_size5 = round(rel5 * 500)

    samples_area1 = {key:area1[key] for key in random.sample(list(area1), sample_size1)}
    samples_area2 = {key:area2[key] for key in random.sample(list(area2), sample_size2)}
    samples_area3 = {key:area3[key] for key in random.sample(list(area3), sample_size3)}
    samples_area4 = {key:area4[key] for key in random.sample(list(area4), sample_size4)}
    samples_area5 = {key:area5[key] for key in random.sample(list(area5), sample_size5)}

    # Put the target words in the according area behind the samples 
    for key in targets:
        if freqs1[key] < min_ + size:
            samples_area1[key] = freqs1[key]
        elif freqs1[key] < min_ + 2 * size:
            samples_area2[key] = freqs1[key]
        elif freqs1[key] < min_ + 3 * size:
            samples_area3[key] = freqs1[key]
        elif freqs1[key] < min_ + 4 * size:
            samples_area4[key] = freqs1[key]
        else:
            samples_area5[key] = freqs1[key]

    # Write output
    loop_dict = {1: samples_area1, 2:samples_area2, 3:samples_area3, 4:samples_area4, 5:samples_area5}

    for i in range(1,6):
        with open(path_output+'samples.tsv', 'a', encoding='utf-8') as f:
            for key in loop_dict[i]:
                f.write(key + '\n')

    with open(path_output+'areas.tsv', 'w', encoding='utf-8') as f:
        f.write('\t'.join((str(sample_size1), str(sample_size2), str(sample_size3), str(sample_size4), str(sample_size5))))
        f.write('\t'.join((str(len(samples_area1)), str(len(samples_area2)), str(len(samples_area3)), str(len(samples_area4)), str(len(samples_area5)))))

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
