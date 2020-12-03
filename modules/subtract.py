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
        get_frequencies.py <path_values1> <path_values2> <path_output>

    Arguments:
        <path_values1>  = path to values from corpus1 
        <path_values2>  = path to values from corpus2
        <path_output>   = output directory.

    """)

    path_values1 = args['<path_values1>']
    path_values2 = args['<path_values2>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()


    # Load values1
    values1 = {}
    with open(path_values1, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            values1[row[0]] = float(row[1])

    # Load values2
    values2 = {}
    with open(path_values2, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            values2[row[0]] = float(row[1])

    # Calculate difference
    diffs = {}
    for key in values1:
        try:
            diffs[key] = np.abs(values1[key] - values2[key])
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
