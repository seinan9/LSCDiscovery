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
        freqs.py [-n] [-l] <path_corpus> <path_output>
        freqs.py [-n] [-l] <path_corpus> <path_corpus2> <path_output>


    Arguments:
        <path_corpus>   = path to input corpus1 (in .txt.gz format)
        <path_corpus2>  = path to input corpus2 (in .txt.gz format)
        <path_output>   = output directory.

    Options:
        -n --norm   normalize frequencies
        -l --log    log-transform frequencies

    """)

    path_corpus = args['<path_corpus>']
    path_corpus2 = args['<path_corpus2>']
    path_output = args['<path_output>']
    is_norm = args['--norm']
    is_log = args['--log']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    freqs = {}
    total_freq = 0

    # Load corpus
    with gzip.open(path_corpus, mode="rt") as f_in:
        for line in f_in:
            for word in line.strip().split(' '):
                try:
                    total_freq += 1
                    freqs[word] += 1
                except KeyError:
                    freqs[word] = 1

    for word in list(freqs.keys()):
        if freqs[word] < 3:
            del(freqs[word])

    if path_corpus2 != None:
        freqs2 = {}
        total_freq2 = 0

        # Load corpus
        with gzip.open(path_corpus2, mode="rt") as f_in:
            for line in f_in:
                for word in line.strip().split(' '):
                    try:
                        total_freq2 += 1
                        freqs2[word] += 1
                    except KeyError:
                        freqs2[word] = 1

        for word in list(freqs2.keys()):
            if freqs2[word] < 3:
                del(freqs2[word])

        intersection_keys = freqs.keys() & freqs2.keys() 
        intersection = {}
        for word in intersection_keys:
            intersection[word] = freqs[word] + freqs2[word]

        if is_norm:
            for key in intersection:
                intersection[key] = float(intersection[key]/(total_freq+total_freq2))

        if is_log:
            for key in intersection:
                intersection[key] = np.log2(intersection[key])
        
        freqs_sorted = sorted(intersection.items(), key=lambda x: x[1])

    else:
        if is_norm:
            for key in freqs:
                freqs[key] = float(freqs[key]/total_freq)

        if is_log:
            for key in freqs:
                freqs[key] = np.log2(freqs[key])
    
        freqs_sorted = sorted(freqs.items(), key=lambda x: x[1])

    # Write output
    with open(path_output, mode='w') as f_out:
        for pair in freqs_sorted:
            f_out.write(pair[0] + '\t' + str(pair[1]) + '\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
