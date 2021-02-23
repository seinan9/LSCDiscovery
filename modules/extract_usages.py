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
        extract_usages.py <path_corpus_lemma> <path_corpus_token> <path_target_words> <path_output_directory> <language> <max_usages>
           
    Arguments:
        <path_corpus_lemma>     = Path to the lemmatized corpus
        <path_corpus_token>     = path to the tokenized corpus
        <path_target_words>     = path to the target words list
        <path_output_directory> = directory where the csv-files are saved
        <language>              = en | de | sw
        <max_usages>            = maximum number of usages to be extracted 

    """)

    path_corpus_lemma = args['<path_corpus_lemma>']
    path_corpus_token = args['<path_corpus_token>']
    path_target_words = args['<path_target_words>']
    path_output_directory = args['<path_output_directory>']
    language = args['<language>']
    max_usages = int(args['<max_usages>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Read targetWords into list
    with open(path_target_words) as f:
        target_words = [line.strip("\n") for line in f]

    # create csv-files with the correct structure
    for target_word in target_words:
        with open(path_output_directory+target_word+".tsv", 'w', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
            writer.writerow(["sentence_lemma", "sentence_token", "index_lemma", "index_token", "lemma"])
    
    if language == 'de':
        trans_table = {u'aͤ' : u'ä', u'oͤ' : u'ö', u'uͤ' : u'ü', u'Aͤ' : u'Ä',
                    u'Oͤ' : u'Ö', u'Uͤ' : u'Ü', u'ſ' : u's', u'\ua75b' : u'r',
                    u'm̃' : u'mm', u'æ' : u'ae', u'Æ' : u'Ae', 
                    u'göñ' : u'gönn', u'spañ' : u'spann'}
    elif language == 'en':
        trans_table = {u' \'s' : u'\'s',
                    u' n\'t' : u'n\'t', u' \'ve' : u'\'ve', u' \'d' : u'\'d',
                    u' \'re' : u'\'re', u' \'ll' : u'\'ll'}
    elif language == 'sw':
        trans_table = {u' \'s' : u'\'s'}
    else:
        trans_table = {}

    # Read and clean lemmatized corpus
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

    # Find uses and write in tab seperated file 
    progress_counter=0
    for target_word in target_words:
        uses = 0
        for i, sentence in enumerate(sentences_lemma):
            target_found = False
            for word in sentence.split():
                lemma = target_word.replace('_nn', '').replace('_vb', '')
                if word == target_word:
                    max_ratio_lemma = 0
                    max_ratio_token = 0
                    for word_lemma in sentences_lemma[i].split():
                        ratio_lemma = fuzz.ratio(
                            target_word.lower(), word_lemma.lower()) 
                        if ratio_lemma > max_ratio_lemma:
                            max_ratio_lemma = ratio_lemma
                            index_lemma = sentences_lemma[i].split().index(word_lemma)
                    for word_token in sentences_token[i].split():
                        ratio_token = fuzz.ratio(
                            lemma.lower(), word_token.lower())
                        if ratio_token > max_ratio_token:
                            max_ratio_token = ratio_token
                            index_token = sentences_token[i].split().index(word_token)
                    with open(path_output_directory+word+".tsv", 'a', encoding="utf-8") as f:
                        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
                        writer.writerow([sentences_lemma[i].strip().replace(target_word, lemma), sentences_token[i].strip(), index_lemma, index_token, lemma])
                    uses += 1
                    target_found = True
                if target_found:
                    break
            if uses == max_usages:
                break
        progress_counter+=1
        logging.info("PROGRESS :"+str(progress_counter)+"/"+str((len(target_words))))

    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")


if __name__ == '__main__':
    main()
