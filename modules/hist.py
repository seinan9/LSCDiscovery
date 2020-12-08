import csv
import logging
import sys
sys.path.append('./modules/')
import time 

from docopt import docopt
import matplotlib.pyplot as plt
import numpy as np


from utils_ import Space

def main():
    """
    Compute binary values for target words.
    """

    # Get the arguments 
    args = docopt("""Compute binary values for taget words.
    
    Usage:
        get_binary.py <path_distances> <path_targets> <path_truth>

        <path_distances>    = path to file containing word distance pairs (tab-separated)
        <path_targets>      = path to file containing target words
        <path_truth>        = path to file containing binary gold data
    
    """)

    path_distances = args['<path_distances>']
    path_targets = args['<path_targets>']
    path_truth = args['<path_truth>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load data
    words = []
    distances = np.array([])
    with open(path_distances, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            words.append(row[0])
            distances = np.append(distances, float(row[1]))

    with open(path_targets, 'r', encoding='utf-8') as f:
        targets = [line.strip() for line in f]

    with open(path_truth, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        truth = [int(row[1]) for row in reader]

    mean = np.mean(distances, axis=0)
    std = np.std(distances, axis=0)

    threshold = mean + std

    binary = []
    for word in targets:
        ind = words.index(word)
        if distances[ind] > threshold:
            binary.append(1)
        else:
            binary.append(0)

    green = []
    red = []
    results = []
    for i in range(len(binary)):
        ind = words.index(targets[i])
        if binary[i] == truth[i]:
            green.append(distances[i])
        else:
            red.append(distances[i])   
        
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
    ax1 = plt.hist(distances)
    ax2 = plt.hist(green, color='green')
    #ax.axvline(threshold, color ='black')
    plt.show()

    logging.info("--- %s seconds ---" % (time.time() - start_time))    


if __name__ == '__main__':
    main()
