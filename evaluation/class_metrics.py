import csv
import logging
import sys
import time 

from docopt import docopt
import numpy as np 
from sklearn import metrics

def main():
    """Compute precission, recall, f_1 and f_0.5.
    """

    # Get the argument 
    args = docopt("""Compute precission, recall, f_1 and f_0.5..

    Usage:
        class_metrics.py <path_truth> <path_file> 

        <path_truth>    = path to binary gold data (tab-separated)
        <path_file>     = path to file containing words and binary values (tab-separated)

    """)
    
    path_truth = args['<path_truth>']
    path_file = args['<path_file>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load gold data
    truth = []
    with open(path_truth, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            truth.append(int(row[1]))

    # Load predictions
    predictions = []
    with open(path_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            predictions.append(int(row[1]))

    # Compute metrics
    precision = metrics.precision_score(truth, predictions, zero_division=0)
    recall = metrics.recall_score(truth, predictions, zero_division=0)
    f1 = metrics.f1_score(truth, predictions, zero_division=0)
    f05 = metrics.fbeta_score(truth, predictions, beta=0.5, zero_division=0)

    precision = round(precision, 3)
    recall = round(recall, 3)
    f1 = round(f1, 3)
    f05 = round(f05, 3)

    # Print output
    print('\t'.join((str(precision), str(recall), str(f1), str(f05))))

    logging.info("--- %s seconds ---" % (time.time() - start_time))    
    print("")


if __name__ == '__main__':
    main()
