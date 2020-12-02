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
        classification_measures.py <path_truth> <path_file> 

        <path_truth>    = path to binary gold data (tab-separated)
        <path_file>     = path to file containing words and binary values (tab-separated)

    """)
    
    path_truth = args['<path_truth>']
    path_file = args['<path_file>']

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

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    for word, value in data.items():
        if data[word] == 1:
            if truth[word] == 1:
                true_positives += 1
            else:
                false_positives += 1
        else:
            if truth[word] == 0:
                true_negatives += 1
            else:
                false_negatives += 1

    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    tpr = true_positives / (true_positives + false_negatives)
    tnr = true_negatives / (true_negatives + false_positives)
    balanced_accuracy = (tpr +tnr) / 2
    f1 = compute_f_measure(precision, recall, 1)
    f05 = compute_f_measure(precision, recall, 0.5)

    print('\t'.join((str(precision), str(recall), str(balanced_accuracy), str(f1), str(f05))))

    logging.info("--- %s seconds ---" % (time.time() - start_time))    
    print("")

def compute_f_measure(precision, recall, beta):
    f1_measure = (1 + beta**2) * ((precision * recall) / (beta**2 * (precision + recall)))
    return f1_measure


if __name__ == '__main__':
    main()
