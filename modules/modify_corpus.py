#!/usr/bin/env python
# coding: utf-8
import gzip
import logging
import sys
sys.path.append('./modules/')
import time

from docopt import docopt

from utils_ import Space

def main():
    args = docopt("""

    Usage:
        modify_corpus.py <path_corpus> <path_target_words> <path_ssages> <path_output>

    Arguments:
        <path_corpus>       = Path to the corpus in txt.gz format
        <path_target_words> = path to target words
        <path_usages>       = path to the usage file
        <path_output>       = path to the output

    """)

    path_corpus = args['<path_corpus>']
    path_target_words = args['<path_target_words>']
    path_usages = args['<path-usages>']
    path_output = args['<path_output>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Read targetWords into list
    logging.info("Read target words")
    with open(path_target_words) as f:
        targetWords = [line.strip("\n") for line in f]

    # Read corpus
    logging.info("Read corpus ")
    sentences = []
    with gzip.open(path_corpus, 'rt', encoding="utf-8") as corpus:
        for sentence in corpus:
            sentences.append(sentence)

    # Clean corpus
    logging.info("Clean corpus")
    for sentence in sentences:
        hasTargetWord = False
        for targetWord in targetWords:
            if targetWord in sentence:
                hasTargetWord = True
                break
        if hasTargetWord == True:
            sentences.remove(sentence)


if __name__ == "__main__":
    main()
