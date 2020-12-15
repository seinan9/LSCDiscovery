import csv
import gzip
import logging
import time

from docopt import docopt
import numpy as np


def main():
    """
    Subtracts values for two given lists (only for the same keys).
    """
    # Get the arguments
    args = docopt("""Subtracts values for two given lists (only for the same keys).

    Usage:
        subtract.py <path_values1> <path_values2> <path_samples> <path_output>

    Arguments:
        <path_values1>  = path to values from corpus1 
        <path_values2>  = path to values from corpus2
        <path_samples>  = path to samples 
        <path_output>   = output directory.

    """)

    path_values1 = args['<path_values1>']
    path_values2 = args['<path_values2>']
    path_samples = args['<path_samples>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load values1
    values1 = {}
    with open(path_values1, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            values1[row[0]] = float(row[1])

    # Load values2
    values2 = {}
    with open(path_values2, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            values2[row[0]] = float(row[1])

    with open(path_samples, 'r', encoding='utf-8') as f:
        samples = [line.strip() for line in f]

    # Calculate difference
    diffs = {}
    for sample in samples:
        try:
            diffs[sample] = np.abs(values1[sample] - values2[sample])
        except KeyError:
            pass

    # Write output
    with open(path_output, mode='w') as f:
        for key in diffs:
            f.write(key + '\t' + str(diffs[key]) + '\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
