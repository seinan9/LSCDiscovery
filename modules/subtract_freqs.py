import csv
import gzip
import logging
import time

from docopt import docopt
import numpy as np


def main():
    """
    Counts frequency of lemmas in input corpora
    """
    # Get the arguments
    args = docopt("""Counts frequency

    Usage:
        get_frequencies.py <path_freqs1> <path_freqs2> <path_output>

    Arguments:
        <path_freqs1>   = path to frequencies from corpus1 
        <path_freqs2>   = path to frequencies from corpus2
        <path_output>   = output directory.

    """)

    path_freqs1 = args['<path_freqs1>']
    path_freqs2 = args['<path_freqs2>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()


    # Load freqs1
    freqs1 = {}
    with open(path_freqs1, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            freqs1[row[0]] = int(row[1])

    total_freqs1 = sum(freqs1.values())

    # Load freqs2
    freqs2 = {}
    with open(path_freqs2, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            freqs2[row[0]] = int(row[1])

    total_freqs2 = sum(freqs2.values())

    # Calculate difference
    diffs = {}
    for word in freqs1:
        try:
            diffs[word] = np.abs(np.log2(float(freqs1[word]/total_freqs1)) - np.log2(float(freqs2[word]/total_freqs2)))
        except KeyError:
            pass

    diffs_sorted = sorted(diffs.items(), key=lambda x: x[1])

    # Write output
    with open(path_output, mode='w') as f_out:
        for pair in diffs_sorted:
            f_out.write(pair[0] + '\t' + str(pair[1]) + '\n')


    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
