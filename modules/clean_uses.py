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
        extract_uses.py <path_usefile> <path_output> <language>
           
    Arguments:
        <path_usefile>      = Path to the usefile
        <path_output>       = Path to output
        <language>          = Language of the corpora (eng/ger/swe/lat)

    """)

    path_usefile = args['<path_usefile>']
    path_output = args['<path_output>']
    language = args['<language>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()
    
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

    # Load sentences 
    logging.info("Load uses")
    sentences = []
    with open(path_usefile, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            sentences.append(row)

    sentences_lemma = []
    sentences_token = []
    index_lemma = []
    index_token =[]

    for sentence in sentences:
        sentences_lemma.append(sentence["sentence_lemma"])
        sentences_token.append(sentence["sentence_token"])

    # Clean sentences
    logging.info("Clean uses")
    for i in range(0, len(sentences_lemma)):
        for key, value in trans_table.items():
            #sentences_lemma[i] = sentences_lemma[i].replace(key, value)
            sentences_token[i] = sentences_token[i].replace(key, value)

    lemma = sentences[0]["original_word"]

    # Find new target_index for lemmatized sentence
    for sentence_lemma in sentences_lemma:
        max_ratio = 0
        for word in sentence_lemma.split():
            ratio = fuzz.ratio(lemma, word.lower())
            if ratio > max_ratio:
                max_ratio = ratio
                index = sentence_lemma.split().index(word)
        index_lemma.append(index)

    # Find new target_index for tokenized sentence
    for sentence_token in sentences_token:
        max_ratio = 0
        for word in sentence_token.split():
            ratio = fuzz.ratio(lemma, word.lower())
            if ratio > max_ratio:
                max_ratio = ratio
                index = sentence_token.split().index(word)
        index_token.append(index)

    with open(path_output+".csv", 'w', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
        writer.writerow(["sentence_lemma", "sentence_token", "index_lemma", "index_token", "lemma"])

    # Save cleaned uses
    logging.info("Save cleaned uses")
    with open(path_output+".csv", 'a', encoding="utf-8") as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
        for i in range(0, len(sentences_lemma)):
            writer.writerow([sentences_lemma[i], sentences_token[i], index_lemma[i], index_token[i], lemma])

    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")


if __name__ == '__main__':
    main()
