import csv
import logging
import time 

from docopt import docopt
import numpy as np 

def main():
    """Compute various classification measures.
    """

    # Get the argument 
    args = docopt("""Compute various classifcation measures.

    Usage:
        classification_measures.py <path_truth> <path_file> <beta>

        <path_truth>    = path to binary gold data 
        <path_file>     = path to file containing words and binary values (tab-separated)
        <beta>          = parameter for F-measure, >1 weights recall higher, <1 weights precision higher

    """)
    
    path_truth = args['<path_truth>']
    path_file = args['<path_file>']
    beta = int(args['<beta>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    truth = {}
    with open(path_truth, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            truth[row[0].strip()] = int(row[1].strip())
    
    data = {}
    with open(path_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            data[row[0].strip()] = int(row[1].strip())

    positives = 0
    negatives = 0
    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    for word, value in truth.items():
        if truth[word] == 1:
            positives += 1
            if data[word] == 1:
                true_positives += 1
            else:
                false_positives += 1
        else:
            negatives += 1
            if data[word] == 0:
                true_negatives += 1
            else:
                false_negatives += 1

    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives)
    tpr = true_positives / (true_positives + false_negatives)
    tnr = true_negatives / (true_negatives + false_positives)
    balanced_accuracy = (tpr +tnr) / 2
    f_measure = (1 + beta**2) * ((precision * recall) / (precision + recall))

    print('\t'.join((str(precision), str(recall), str(accuracy), str(balanced_accuracy), str(f_measure))))

    logging.info("--- %s seconds ---" % (time.time() - start_time))    
    print("")


if __name__ == '__main__':
    main()
