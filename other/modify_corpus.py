#!/usr/bin/env python
import csv
import gzip
import logging
import random
import sys
sys.path.append('./modules/')
import time

from docopt import docopt

from utils_ import Space

def main():
    args = docopt("""

    Usage:
        modify_corpus.py <path_corpus> <path_target_words> <dir_usages> <path_output>

    Arguments:
        <path_corpus>       = Path to the corpus in txt.gz format
        <path_target_words> = path to target words
        <dir_usages>        = directory where the usage files are contained
        <path_output>       = path to the output

    """)

    path_corpus = args['<path_corpus>']
    path_target_words = args['<path_target_words>']
    dir_usages = args['<dir_usages>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Read targetWords into list
    logging.info("Read target words")
    with open(path_target_words) as f:
        target_words = [line.strip("\n") for line in f]

    # Read corpus
    logging.info("Read corpus ")
    sentences = []
    with gzip.open(path_corpus, 'rt', encoding='utf-8') as corpus:
        for sentence in corpus:
            sentences.append(sentence)

    # Clean corpus
    logging.info("Clean corpus")
    for sentence in sentences:
        has_target_word = False
        for target_word in target_words:
            if target_word in sentence:
                has_target_word = True
                break
        if has_target_word == True:
            sentences.remove(sentence)
    
    # Inject sentences
    logging.info("Inject usages")
    usages = {}
    for target_word in target_words:
        clean_target_word = target_word.replace('ä', '').replace('ö', '').replace('ü', '').replace('ß', '')
        with open(dir_usages+clean_target_word+'.csv', 'r', encoding='utf-8') as usage_file:            
            reader = csv.DictReader(usage_file, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
            for row in reader:
                identifier = row['identifier'].rsplit('-', 1)[0]
                usages[identifier] = row['sentence_lemma'].replace('$', '').replace('  ', ' ')

    for key in usages:
        sentences.append(usages[key])

    random.shuffle(sentences)

    # Save corpus
    logging.info("Save corpus")
    with gzip.open(path_output+'.txt.gz', 'wt', encoding='utf-8') as corpus: 
        for sentence in sentences:
            corpus.write(sentence)

    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")

    
if __name__ == "__main__":
    main()
