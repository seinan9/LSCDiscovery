#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import gzip
import logging
import time

from docopt import docopt
from fuzzywuzzy import fuzz


def main():

    # Get the arguments
    args = docopt("""
    Usage:
        extract_uses.py <path_corpus_lemma> <path_corpus_token> <path_target_words> <path_output_directory> <language>
           
    Arguments:
        <path_corpus_lemma>     = Path to the lemmatized corpus
        <path_corpus_token>     = path to the tokenized corpus
        <path_target_words>     = path to the target words list
        <path_output_directory> = directory where the csv-files are saved
        <language>              = Language of the corpora (eng/ger/swe/lat)

    """)

    path_corpus_lemma = args['<path_corpus_lemma>']
    path_corpus_token = args['<path_corpus_token>']
    path_target_words = args['<path_target_words>']
    path_output_directory = args['<path_output_directory>']
    language = args['<language>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Read targetWords into list
    logging.info("Read target words")
    with open(path_target_words) as f:
        target_words = [line.strip("\n") for line in f]

    # create csv-files with the correct structure
    for target_word in target_words:
        with open(path_output_directory+target_word+".csv", 'w', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
            writer.writerow(["sentence_lemma", "sentence_token", "index_lemma", "index_token", "lemma"])
    
    if language == 'ger':
        trans_table = {u'aͤ' : u'ä', u'oͤ' : u'ö', u'uͤ' : u'ü', u'Aͤ' : u'Ä',
                    u'Oͤ' : u'Ö', u'Uͤ' : u'Ü', u'ſ' : u's', u'\ua75b' : u'r',
                    u'm̃' : u'mm', u'æ' : u'ae', u'Æ' : u'Ae', 
                    u'göñ' : u'gönn', u'spañ' : u'spann'}
    elif language == 'eng':
        trans_table = {u' \'s' : u'\'s',
                    u' n\'t' : u'n\'t', u' \'ve' : u'\'ve', u' \'d' : u'\'d',
                    u' \'re' : u'\'re', u' \'ll' : u'\'ll'}
    elif language == 'swe':
        trans_table = {u' \'s' : u'\'s'}
    else:
        trans_table = {}

    # Read and clean lemmatized corpus
    logging.info("Read corpora ")
    sentences_lemma = []
    with gzip.open(path_corpus_lemma, 'rt', encoding="utf-8") as corpus_lemma:
        for sentence in corpus_lemma:
            sentences_lemma.append(sentence)

    # Read and clean tokenized corpus
    sentences_token = []
    with gzip.open(path_corpus_token, 'rt', encoding="utf-8") as corpus_token:
        for sentence in corpus_token:
            for key, value in trans_table.items():
                sentence = sentence.replace(key, value)
            sentences_token.append(sentence)

    # Whenever a targetWord occurs in a sentence, write down sentences, target_index, 0 and the targetWord in the output file
    logging.info("Find word usages")
    for i, sentence in enumerate(sentences_lemma):
        for word in sentence.split():
            for target_word in target_words:
                if word == target_word:
                    max_ratio_lemma = 0
                    max_ratio_token = 0
                    for word_lemma in sentences_lemma[i].split():
                        ratio_lemma = fuzz.ratio(
                            target_word.strip('_nn').lower(), word_lemma.lower())
                        if ratio_lemma > max_ratio_lemma:
                            max_ratio_lemma = ratio_lemma
                            index_lemma = sentences_lemma[i].split().index(word_lemma)
                    for word_token in sentences_token[i].split():
                        ratio_token = fuzz.ratio(
                            target_word.strip('_nn').lower(), word_token.lower())
                        if ratio_token > max_ratio_token:
                            max_ratio_token = ratio_token
                            index_token = sentences_token[i].split().index(word_token)
                    with open(path_output_directory+word+".csv", 'a', encoding="utf-8") as f:
                        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
                        writer.writerow([sentences_lemma[i].strip(), sentences_token[i].strip(), index_lemma, index_token, target_word])

    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")


if __name__ == '__main__':
    main()
