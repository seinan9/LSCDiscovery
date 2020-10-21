import logging
import sys
sys.path.append('./modules/')
import time

from docopt import docopt
import numpy as np
from scipy.spatial.distance import cosine as cosine_distance

from utils_ import Space


def main():
    """
    Compute cosine distance between two averaged lists of vectors. 
    """

    # Get the arguments
    args = docopt("""Compute cosine distance for two averaged lists of vectors. 

    Usage:
        cos.py <path_matrix1> <path_matrix2> 

        <path_matrix1> = path to first matrix
        <path_matrix2> = path to second matrix
        
    """)
    
    path_matrix1 = args['<path_matrix1>']
    path_matrix2 = args['<path_matrix2>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Load matrices/vectorLists
    try:
        space1 = Space(path_matrix1, format='npz')   
    except ValueError:
        space1 = Space(path_matrix1, format='w2v')   
    try:
        space2 = Space(path_matrix2, format='npz')
    except ValueError:
        space2 = Space(path_matrix2, format='w2v')

    vectors1 = space1.matrix.toarray()
    vectors2 = space2.matrix.toarray()

    # Compute average vectors for both lists
    avg1 = np.sum(vectors1, axis=0) / len(vectors1)
    avg2 = np.sum(vectors2, axis=0) / len(vectors2)

    # Compute cosine distance between the two average vectors
    cos = cosine_distance(avg1,avg2)

    # Print cosine distance
    print(cos)

    logging.info("--- %s seconds ---" % (time.time() - start_time))              
    print("")     
    
    
if __name__ == '__main__':
    main()
