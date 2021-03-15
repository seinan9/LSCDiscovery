from collections import defaultdict
import logging
import sys
sys.path.append('./modules/')
import time

from docopt import docopt
from gensim.models.word2vec import PathLineSentences
from scipy.sparse import dok_matrix

from utils_ import Space


def main():
    """
    Make count-based vector space from corpus.
    """

    # Get the arguments
    args = docopt("""Make count-based vector space from corpus.
    Usage:
        count.py [-l] <path_corpus> <path_output> <window_size>
        
    Arguments:
       
        <path_corpus>   = path to corpus or corpus directory (iterates through files)
        <path_output>   = output path for vectors
        <window_size>   = the linear distance of context words to consider in each direction
    Options:
        -l, --len   normalize final vectors to unit length
    """)
    
    path_corpus = args['<path_corpus>']
    path_output = args['<path_output>']
    window_size = int(args['<window_size>'])    
    is_len = args['--len']
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()


    # Build vocabulary
    logging.info("Building vocabulary")
    sentences = PathLineSentences(path_corpus)
    vocabulary = sorted(list(set([word for sentence in sentences for word in sentence if len(sentence)>1]))) # Skip one-word sentences to avoid zero-vectors
    w2i = {w: i for i, w in enumerate(vocabulary)}
    
    # Initialize co-occurrence matrix as dictionary
    cooc_mat = defaultdict(lambda: 0)

    # Get counts from corpus
    sentences = PathLineSentences(path_corpus)
    logging.info("Counting context words")
    for sentence in sentences:
        for i, word in enumerate(sentence):
            lowerwindow_size = max(i-window_size, 0)
            upperwindow_size = min(i+window_size, len(sentence))
            window = sentence[lowerwindow_size:i] + sentence[i+1:upperwindow_size+1]
            if len(window)==0: # Skip one-word sentences
                continue
            windex = w2i[word]
            for contextWord in window:
                cooc_mat[(windex,w2i[contextWord])] += 1

    # Convert dictionary to sparse matrix
    logging.info("Converting dictionary to matrix")
    cooc_mat_sparse = dok_matrix((len(vocabulary),len(vocabulary)), dtype=float)
    try:
        cooc_mat_sparse.update(cooc_mat)
    except NotImplementedError:
        cooc_mat_sparse._update(cooc_mat)

    outSpace = Space(matrix=cooc_mat_sparse, rows=vocabulary, columns=vocabulary)

    if is_len:
        # L2-normalize vectors
        outSpace.l2_normalize()
        
    # Save the matrix
    outSpace.save(path_output)


    logging.info("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
