import logging
import sys
sys.path.append('./modules/')
import time

from docopt import docopt
from scipy.spatial.distance import cosine as cosine_distance

from utils_ import Space


def main():
    """
    Compute cosine distance for targets in two matrices.
    """

    # Get the arguments
    args = docopt("""Compute cosine distance for targets in two matrices.

    Usage:
        cd.py <path_matrix1> <path_matrix2> <path_output>
        cd.py <path_matrix1> <path_matrix2> <path_targets> <path_output>

        <path_matrix1>      = path to first matrix
        <path_matrix2>      = path to second matrix
        <path_targets>      = path to file with target words (optional)
        <path_output>       = output path for result file

     Note:
        Choose the first usage to compute CDs for all word in the intersection of the vocabularies.
        Choose the secondary usage to compute CDs only for <path_targets>. 
        Important: spaces must be already aligned (columns in same order)! Targets in first/second column of testset are computed from matrix1/matrix2.
        
    """)
    
    path_matrix1 = args['<path_matrix1>']
    path_matrix2 = args['<path_matrix2>']
    path_targets = args['<path_targets>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Load matrices and rows
    try:
        space1 = Space(path_matrix1, format='npz')   
    except ValueError:
        space1 = Space(path_matrix1, format='w2v')   
    try:
        space2 = Space(path_matrix2, format='npz')
    except ValueError:
        space2 = Space(path_matrix2, format='w2v')
        
    matrix1 = space1.matrix
    row2id1 = space1.row2id
    matrix2 = space2.matrix
    row2id2 = space2.row2id

    distances = {}
    
    # Usage 1: compute CD for every word in the intersection of the vocabularies
    if path_targets == None:

        # Compute CD
        for key in row2id1:
            try:
                vec1 = matrix1[row2id1[key]].toarray().flatten()
                vec2 = matrix2[row2id2[key]].toarray().flatten()
                cd = cosine_distance(vec1, vec2)
                distances[key] = cd
            except KeyError:
                pass
    # Usage 2: compute CD for every word in <path_targets>
    else:
        # Load targets
        with open(path_targets, 'r', encoding='utf-8') as f:
            targets = [line.strip() for line in f]

        # Compute CD
        for word in targets:
            try:
                vec1 = matrix1[row2id1[word]].toarray().flatten()
                vec2 = matrix2[row2id2[word]].toarray().flatten()
                cd = cosine_distance(vec1, vec2)
                distances[word] = cd
            except KeyError:
                distances[word] = 'nan'
                continue
    
    # Write output to <paht_output>
    with open(path_output, 'w', encoding='utf-8') as f:
        for key in distances:
            f.write(key + '\t' + str(distances[key]) + '\n')
            
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    print("")
    

if __name__ == '__main__':
    main()
