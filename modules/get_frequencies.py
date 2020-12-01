import time
import logging
import gzip

from docopt import docopt


def main():
    """
    Counts frequency of lemmas in input corpora
    """
    # Get the arguments
    args = docopt("""Counts frequency

    Usage:
        get_frequencies.py <path_corpus> <path_output>

    Arguments:
        <path_corpus>   = path to input corpus1 (in .txt.gz format)
        <path_output>   = output directory.

    """)

    path_corpus = args['<path_corpus>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    freqs = {}

    # Load corpus
    with gzip.open(path_corpus, mode="rt") as f_in:
        for line in f_in:
            for word in line.strip().split(' '):
                try:
                    freqs[word] += 1
                except KeyError:
                    freqs[word] = 1
    
    freqs_sorted = sorted(freqs.items(), key=lambda x: x[1])

    # Write output
    with open(path_output, mode='w') as f_out:
        for pair in freqs_sorted:
            if pair[1] >= 4:
                f_out.write(pair[0] + '\t' + str(pair[1]) + '\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
