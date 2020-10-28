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
        with open(path_output_directory+target_word+".csv", 'w', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["sentence_token", "target_index",
                             "cluster", "original_word"])
    
    if language == 'ger':
         trans_table = {u'aͤ' : u'ä', u'oͤ' : u'ö', u'uͤ' : u'ü', u'Aͤ' : u'Ä',
                    u'Oͤ' : u'Ö', u'Uͤ' : u'Ü', u'ſ' : u's', u'\ua75b' : u'r',
                    u'm̃' : u'mm', u'æ' : u'ae', u'Æ' : u'Ae', u' ,': u',',
                    u' .': u'.', u' ;': u';', u' ?': u'?', u' !': u'!',
                    u'„ ': u'„', u' “': u'“', u' "': u'"', u' :': u':', u' )': u')',
                    u'( ': u'(', u' \'s' : u'\'s', u'- ' : u'-', u'  ' : u' ', 
                    u'göñ' : u'gönn', u'spañ' : u'spann'}
    elif language == 'eng':
         trans_table = {u' ,': u',',
                    u' .': u'.', u' ;': u';', u' ?': u'?', u' !': u'!',
                    u'„ ': u'„', u' “': u'“', u' :': u':', u' )': u')',
                    u'( ': u'(', u' \'s' : u'\'s', u'  ' : u' ',
                    u' n\'t' : u'n\'t', u' \'ve' : u'\'ve', u' \'d' : u'\'d',
                    u' \'re' : u'\'re', u' \'ll' : u'\'ll'}
    elif language == 'swe':
         trans_table = {u' ,': u',',
                    u' .': u'.', u' ;': u';', u' ?': u'?', u' !': u'!',
                    u'„ ': u'„', u' “': u'“', u' "': u'"', u' :': u':', u' )': u')',
                    u'( ': u'(', u' \'s' : u'\'s', u'  ' : u' '}
    else:
        trans_table = {}

    # Read lemmatized corpus
    logging.info("Read corpora ")
    sentences_lemma = []
    with gzip.open(path_corpus_lemma, 'rt', encoding="utf-8") as corpus_lemma:
        for sentence in corpus_lemma:
            sentences_lemma.append(sentence)

    # Read tokenized corpus
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
                    max_ratio = 0
                    for wordT in sentences_token[i].split():
                        ratio = fuzz.ratio(
                            target_word.strip('_nn').lower(), wordT.lower())
                        if ratio > max_ratio:
                            max_ratio = ratio
                            index = sentences_token[i].split().index(wordT)
                    with open(path_output_directory+word+".csv", 'a', encoding="utf-8") as file:
                        writer = csv.writer(file, delimiter='\t')
                        writer.writerow([sentences_token[i], index, 0, target_word])

    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")


if __name__ == '__main__':
    main()
