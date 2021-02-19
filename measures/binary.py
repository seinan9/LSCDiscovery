import csv
import logging
import time 

from docopt import docopt
import numpy as np


def main():
    """
    Compute binary scores for target words.
    """

    # Get the arguments 
    args = docopt("""Compute binary scores for taget words.
    
    Usage:
        binary.py <path_distances> <path_output> <deviation_factor>
        binary.py <path_distances> <path_targets> <path_output> <deviation_factor> 
 
        <path_distances>    = path to file containing word distance pairs (tab-separated)
        <path_targets>      = path to file containing target words (optional for binary classification)
        <path_output>       = output path for result file
        <deviaton_factor>   = threshold = mean + deviation_factor * std   
        
    Note:
        Choose the first usage to discover changing words in <path_distances>.
        Choose the second usage to compute binary scores for words in <path_targets>.

    """)

    path_distances = args['<path_distances>']
    path_targets = args['<path_targets>']
    path_output = args['<path_output>']
    deviation_factor = float(args['<deviation_factor>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load data 
    distances = {}
    with open(path_distances, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            distances[row[0]] = float(row[1])

    # Compute mean, std and threshold
    list_distances = np.array(list(distances.values()))

    mean = np.mean(list_distances, axis=0)
    std = np.std(list_distances, axis=0)
    threshold = mean + deviation_factor * std

    # Usage 1: discover changing words 
    if path_targets == None:
        changing_words = []
        for key in distances:
            if distances[key] >= threshold:
                changing_words.append(key)

        # Write changing words to <path_output>
        with open(path_output, 'w', encoding='utf-8') as f:
            for word in changing_words:
                f.write(word + '\n')

    # Usage 2: label target words according to threshold (binary classification)
    else:
        # Load data
        target_distances = {}
        with open(path_targets, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
            for row in reader:
                target_distances[row[0]] = float(row[1])

        # Compute binary scores
        binary_scores = {}
        for key in target_distances:
            if target_distances[key] >= threshold:
                binary_scores[key] = 1
            else:
                binary_scores[key] = 0

        # Write binary scores to <path_output>
        with open(path_output, 'w', encoding='utf-8') as f:
            for key, value in binary_scores.items():
                f.write(key + '\t' + str(value) + '\n')


    logging.info("--- %s seconds ---" % (time.time() - start_time))    


if __name__ == '__main__':
    main()
