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
        cd.py [(-f | -s)] -d <path_matrix1> <path_matrix2> <path_target_words> <path_output>

        <path_matrix1>      = path to first matrix
        <path_matrix2>      = path to second matrix
        <path_target_words> = path to file with tab-separated word pairs (single column if -d is set)
        <path_output>       = output path for result file

    Options:
        -f, --fst   write only first target in output file
        -s, --scd   write only second target in output file
        -d, --dia   take a single column file as input

     Note:
         Important: spaces must be already aligned (columns in same order)! Targets in first/second column of testset are computed from matrix1/matrix2.
        
    """)
    
    path_matrix1 = args['<path_matrix1>']
    path_matrix2 = args['<path_matrix2>']
    path_target_words = args['<path_target_words>']
    path_output = args['<path_output>']

    is_fst = args['--fst']
    is_scd = args['--scd']
    is_dia = args['--dia']

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
    
    # Load targets
    with open(path_target_words, 'r', encoding='utf-8') as f_in:
        if is_dia:
            targets = [(line.strip().split('\t')[0],line.strip().split('\t')[0]) for line in f_in]
        else:
            targets = [(line.strip().split('\t')[0],line.strip().split('\t')[1]) for line in f_in]
        
    scores = {}
    for (t1, t2) in targets:
        
        # Get row vectors
        try:
            v1 = matrix1[row2id1[t1]].toarray().flatten()
            v2 = matrix2[row2id2[t2]].toarray().flatten()
        except KeyError:
            scores[(t1, t2)] = 'nan'
            continue
        
        # Compute cosine distance of vectors
        distance = cosine_distance(v1, v2)
        scores[(t1, t2)] = distance
        
        
    with open(path_output, 'w', encoding='utf-8') as f_out:
        for (t1, t2) in targets:
            if is_fst: # output only first target string
                f_out.write('\t'.join((t1, str(scores[(t1, t2)])+'\n')))
            elif is_scd: # output only second target string
                f_out.write('\t'.join((t2, str(scores[(t1, t2)])+'\n')))
            else: # standard outputs both target strings    
                f_out.write('\t'.join(('%s,%s' % (t1,t2), str(scores[(t1, t2)])+'\n')))

                
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    print("")
    


if __name__ == '__main__':
    main()
