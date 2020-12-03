import csv
import logging
import sys
import time 

from docopt import docopt
import numpy as np 
from sklearn import metrics

def main():
    """Compute various classification measures.
    """

    # Get the argument 
    args = docopt("""Compute various classifcation measures.

    Usage:
        classification_measures.py <path_truth> <path_file> 

        <path_truth>    = path to binary gold preds (tab-separated)
        <path_file>     = path to file containing words and binary values (tab-separated)

    """)
    
    path_truth = args['<path_truth>']
    path_file = args['<path_file>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    truth = []
    with open(path_truth, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            truth.append(int(row[1]))
    
    preds = []
    with open(path_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            preds.append(int(row[1]))

    precision = metrics.precision_score(truth, preds, zero_division=0)
    recall = metrics.recall_score(truth, preds, zero_division=0)
    bal_acc = metrics.balanced_accuracy_score(truth, preds)
    f1 = metrics.f1_score(truth, preds, zero_division=0)
    f05 = metrics.fbeta_score(truth, preds, beta=0.5, zero_division=0)

    precision = round(precision, 3)
    recall = round(recall, 3)
    bal_acc = round(bal_acc, 3)
    f1 = round(f1, 3)
    f05 = round(f05, 3)

    print('\t'.join((str(precision), str(recall), str(bal_acc), str(f1), str(f05))))


    logging.info("--- %s seconds ---" % (time.time() - start_time))    
    print("")


if __name__ == '__main__':
    main()
