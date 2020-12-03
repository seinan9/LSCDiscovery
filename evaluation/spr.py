import logging
import sys
sys.path.append('./modules/')
import time

from docopt import docopt
import numpy as np
from scipy.stats import spearmanr


def main():
    """
    Calculate spearman correlation coefficient for specified columns of two files. 
    """

    # Get the arguments
    args = docopt("""Calculate spearman correlation coefficient for specified columns of two files.                     


    Usage:
        spr.py <path_file1> <path_file2> <col1> <col2>
        
    Arguments:
        <path_file1>    = path to first file
        <path_file2>    = path to second file
        <col1>          = target column in file1
        <col2>          = target column in file2

    Note:
        Assumes tap-separated CSV files as input. Assumes that rows are in same order and columns have same length. Nan values are omitted.
        
    """)

    path_file1 = args['<path_file1>']
    path_file2 = args['<path_file2>']
    col1 = int(args['<col1>'])
    col2 = int(args['<col2>'])
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Get data
    with open(path_file1, 'r', encoding='utf-8') as f_in:
        data1 = np.array([float(line.strip().split()[col1]) for line in f_in])
        
    with open(path_file2, 'r', encoding='utf-8') as f_in:
        data2 = np.array([float(line.strip().split()[col2]) for line in f_in])

    # Check if there are non-number values    
    nan_list1 = [x for x in data1 if np.isnan(x)]   
    nan_list2 = [x for x in data2 if np.isnan(x)]
    if len(nan_list1)>0 or len(nan_list2)>0:
        print('nan encountered!')      

    # compute correlation
    try:
        rho, p = spearmanr(data1, data2, nan_policy='omit')
    except ValueError as e:
        logging.info(e)
        rho, p = float('nan'), float('nan')

    print('\t'.join((str(rho), str(p))))
              
    logging.info("--- %s seconds ---" % (time.time() - start_time))            
    print("")

   
if __name__ == '__main__':
    main()
