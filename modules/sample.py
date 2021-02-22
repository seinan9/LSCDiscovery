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
    Sample words from the intersection of the corpus vocabularies.
    """
    # Get the arguments
    args = docopt("""Sample words from the intersection of the corpus vocabularies.

    Usage:
        sample.py [-s] <path_freqs> <path_output> <sample_size> 

    Arguments:
        <path_freqs>    = path to frequency list from corpus 1
        <path_output>   = directory where the files are saved
        <sample_size>   = size of the sample
    
    Options:
        -s --simple     randomly samples words from a list

    """)

    path_freqs = args['<path_freqs>']
    path_output = args['<path_output>']
    sample_size = int(args['<sample_size>'])

    is_simple = args['--simple']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    if not is_simple:
        # Load frequencies
        freqs = {}
        with open(path_freqs, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
            for row in reader:
                try:
                    freqs[row[0]] = float(row[1])
                except ValueError:
                    pass

        # Compute range and area_size
        max_ = list(freqs.values())[-1]
        min_ = list(freqs.values())[0]
        range_ = max_ - min_
        size = range_ / 5

        # Create and fill areas accordingly
        area1 = {}
        area2 = {}
        area3 = {}
        area4 = {}
        area5 = {}

        for key in freqs:
            if freqs[key] < min_ + size:
                area1[key] = freqs[key]
            elif freqs[key] < min_ + 2 * size:
                area2[key] = freqs[key]
            elif freqs[key] < min_ + 3 * size:
                area3[key] = freqs[key]
            elif freqs[key] < min_ + 4 * size:
                area4[key] = freqs[key]    
            else:
                area5[key] = freqs[key]

        # Compute percentages to determine how many samples to take from each area
        rel1 = len(area1) / len(freqs)
        rel2 = len(area2) / len(freqs)
        rel3 = len(area3) / len(freqs)
        rel4 = len(area4) / len(freqs)
        rel5 = len(area5) / len(freqs)

        sample_size1 = round(rel1 * sample_size)
        sample_size2 = round(rel2 * sample_size)
        sample_size3 = round(rel3 * sample_size)
        sample_size4 = round(rel4 * sample_size)
        sample_size5 = round(rel5 * sample_size)

        samples_area1 = {key:area1[key] for key in random.sample(list(area1), sample_size1)}
        samples_area2 = {key:area2[key] for key in random.sample(list(area2), sample_size2)}
        samples_area3 = {key:area3[key] for key in random.sample(list(area3), sample_size3)}
        samples_area4 = {key:area4[key] for key in random.sample(list(area4), sample_size4)}
        samples_area5 = {key:area5[key] for key in random.sample(list(area5), sample_size5)}

        # Write output
        loop_dict = {1: samples_area1, 2:samples_area2, 3:samples_area3, 4:samples_area4, 5:samples_area5}

        for i in range(1,6):
            with open(path_output, 'a', encoding='utf-8') as f:
                for key in loop_dict[i]:
                    f.write(key + '\n')

    else:
        words = []
        with open(path_freqs, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
            for row in reader:
                try:
                    words.append(row[0])
                except ValueError:
                    pass

        random_sample = random.sample(words, sample_size)

        with open(path_output, 'w', encoding='utf-8') as f:
            for word in random_sample:
                f.write(word + '\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
