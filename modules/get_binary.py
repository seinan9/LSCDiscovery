import csv
import logging
import sys
sys.path.append('./modules/')
import time 

from docopt import docopt
import numpy as np

from utils_ import Space

def main():
    """
    Compute binary values for target words.
    """

    # Get the arguments 
    args = docopt("""Compute binary values for taget words.
    
    Usage:
        get_binary.py <path_distances> <path_targets> <path_output>

        <path_distances>    = path to file containing word distance pairs (tab-separated)
        <path_targets>      = path to file containing target words
        <path_output>       = output path for result file
    
    """)

    path_distances = args['<path_distances>']
    path_targets = args['<path_targets>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    words = []
    distances = np.array([])

    # Load data 
    with open(path_distances, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            words.append(row[0])
            distances = np.append(distances, float(row[1]))

    with open(path_targets, 'r', encoding='utf-8') as f:
        targets = [line.strip() for line in f]

    mean = np.mean(distances, axis=0)
    std = np.std(distances, axis=0)

    threshold = mean + std

    # Compute bianry scores
    binary = {}
    for word in targets:
        ind = words.index(word)
        if distances[ind] >= threshold:
            binary[word] = 1
        else:
            binary[word] = 0

    # Write output
    with open(path_output, 'w', encoding='utf-8') as f:
        for key, value in binary.items():
            f.write(key + '\t' + str(value) + '\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))    


if __name__ == '__main__':
    main()
