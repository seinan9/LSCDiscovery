from collections import defaultdict
import gzip
import logging
import time

from gensim.models.word2vec import PathLineSentences
from docopt import docopt


def main():
    """
    Preprocess corpus (remove low-frequency words, etc.).
    """

    # Get the arguments
    args = docopt("""Preprocess corpus (remove low-frequency words, etc.).
    Usage:
        preprocess.py <path_corpus> <path_output> <min_count>
        
    Arguments:
       
        <path_corpus>   = path to corpus 
        <path_output>   = output path
        <min_count>     = minimum frequency threshold
        
    """)
    
    path_corpus = args['<path_corpus>']
    path_output = args['<path_output>']        
    min_count = int(args['<min_count>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()
    

    # Get sentence iterator
    sentences = PathLineSentences(path_corpus)

    # Initialize frequency dictionary
    freqs = defaultdict(int)      

    # Iterate over sentences and words
    for sentence in sentences:
        for word in sentence:
            freqs[word] = freqs[word] + 1

    # Get sentence iterator
    sentences = PathLineSentences(path_corpus)            

    # Write output
    with gzip.open(path_output, 'wt', encoding='utf-8') as f_out:
        for sentence in sentences:
            out_sentence = [word for word in sentence if freqs[word] >= min_count]
            if len(out_sentence) > 1:
                f_out.write(' '.join(out_sentence)+'\n')


    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()