import logging
import sys
sys.path.append('./modules/')
import time

from docopt import docopt
import numpy as np
from scipy.stats import entropy

from utils_ import Space
            

def main():
    """
    Compute entropy for rows of targets from vector space.
    """

    # Get the arguments
    args = docopt("""Compute entropy for rows of targets from vector space.
    Usage:
        entropy.py [-n] [-l] <path_matrix> <path_output>

        <path_matrix> = path to matrix (needs to be count based)
        <path_output> = output path for result file
        
    Options:
        -n, --norm  normalize values by log of number of types
        -l, --log   log-transforms values 
    """)
    
    path_matrix = args['<path_matrix>']
    path_output = args['<path_output>']        
    is_norm = args['--norm']
    is_log = args['--log']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load matrices and rows
    try:
        space = Space(path_matrix, format='npz')
    except ValueError:
        space = Space(path_matrix, format='w2v')
    
    matrix = space.matrix
    row2id = space.row2id
    
    scores = {}
    norms = {}

    for key in row2id:
        row = matrix[row2id[key]]
        counts = row.data
        H = entropy(counts, base=2)
        scores[key] = H

        if is_norm:
            types = row.getnnz()
            norms[key] = np.log2(types)

    if is_norm:
        for key in scores:
            scores[key] = float(scores[key] / norms[key])

    if is_log:
        for key in scores:
            scores[key] = np.log2(scores[key])

    scores_sorted = sorted(scores.items(), key=lambda x: x[1])

    # Write output
    with open(path_output, mode='w') as f_out:
        for pair in scores_sorted:
            f_out.write(pair[0] + '\t' + str(pair[1]) + '\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()