import logging
import sys
sys.path.append('./modules/')
import time

from docopt import docopt
import gensim
from gensim.models.word2vec import PathLineSentences


def main():
    """
    Make embedding vector space with Negative Sampling from corpus.
    """

    # Get the arguments
    args = docopt("""Make embedding vector space with Skip-Gram with Negative Sampling from corpus.

    Usage:
        sgns.py [-l] <path_corpus> <path_output> <window_size> <dim> <k> <t> <min_count> <itera>
        
    Arguments:
       
        <path_corpus>   = path to corpus directory with zipped files
        <path_output>   = output path for vectors
        <window_size>   = the linear distance of context words to consider in each direction
        <dim>           = dimensionality of embeddings
        <k>             = number of negative samples parameter (equivalent to shifting parameter for PPMI)
        <t>             = threshold for subsampling
        <min_count>     = number of occurrences for a word to be included in the vocabulary
        <itera>         = number of iterations

    Options:
        -l, --len   normalize final vectors to unit length

    """)

    path_corpus = args['<path_corpus>']
    path_output = args['<path_output>']
    window_size = int(args['<window_size>'])    
    dim = int(args['<dim>'])    
    k = int(args['<k>'])
    if args['<t>']=='None':
        t = None
    else:
        t = float(args['<t>'])        
    min_count = int(args['<min_count>'])    
    itera = int(args['<itera>'])    

    is_len = args['--len']


    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
         
    # Initialize model
    model = gensim.models.Word2Vec(sg=1, # skipgram
    							   hs=0, # negative sampling
    							   negative=k, # number of negative samples
    							   sample=t, # threshold for subsampling, if None, no subsampling is performed
    							   size=dim, window=window_size, min_count=min_count, iter=itera, workers=40)

    # Initialize vocabulary
    vocab_sentences = PathLineSentences(path_corpus)
    logging.getLogger('gensim').setLevel(logging.ERROR)    
    model.build_vocab(vocab_sentences)

    # Train
    sentences = PathLineSentences(path_corpus)
    model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs)

    if is_len:
        # L2-normalize vectors
        model.init_sims(replace=True)

    # Save the vectors and the model
    model.wv.save_word2vec_format(path_output)
    model.save(path_output + '.model')

    logging.info("--- %s seconds ---" % (time.time() - start_time))



if __name__ == '__main__':
    main()
