import logging
import sys
sys.path.append('./modules/')
import time

from docopt import docopt

from utils_ import Space


def main():
    """
    Mean center matrix.
    """

    # Get the arguments
    args = docopt('''Mean center matrix.

    Usage:
        center.py [-l] [-w] <path_matrix> <path_output>

        <path_matrix>   = path to matrix
        <path_output>   = output path for space

    Options:
        -l, --len   normalize vectors to unit length before centering
        -w, --w2v   save in word2vec format

    ''')

    path_matrix = args['<path_matrix>']
    path_output = args['<path_output>']
    
    is_len = args['--len']
    is_w2v = args['--len']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load matrices and rows
    try:
        space = Space(path_matrix, format='npz')   
    except ValueError:
        space = Space(path_matrix, format='w2v')   

    if is_len:
        # L2-normalize vectors
        space.l2_normalize()

    # Mean center    
    space.mean_center()
        
    # Save the matrix
    if is_w2v:
        space.save(path_output, format='w2v')
    else:
        space.save(path_output)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                
    print("")   


if __name__ == '__main__':
    main()
