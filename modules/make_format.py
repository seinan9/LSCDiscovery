#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import gzip
import logging
import random
import time

from docopt import docopt
from fuzzywuzzy import fuzz
import spacy


def main():

    # Get the arguments
    args = docopt("""
    Usage:
        make_format.py <path_usages1> <path_usages2> <path_output> <language> <max_samples>
           
    Arguments:
        <path_usages1>        = File containing uses from corpus 1
        <path_usages2>        = file containing uses from corpus 2
        <path_output>       = output name
        <language>          = en | de | it | ru
        <max_samples>       = maximal number of samples per corpus 

    """)

    path_usages1 = args['<path_usages1>']
    path_usages2 = args['<path_usages2>']
    path_output = args['<path_output>']
    language = args['<language>']
    max_samples = int(args['<max_samples>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load sentences 
    logging.info("Load uses")
    sentences1 = []
    with open(path_usages1, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            sentences1.append(row)

    sentences_token1 = []
    index_token1 =[]

    for sentence in sentences1:
        sentences_token1.append(sentence["sentence_token"])
        index_token1.append(sentence["index_token"])

    sentences2 = []
    with open(path_usages2, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            sentences2.append(row)

    sentences_token2 = []
    index_token2 =[]

    for sentence in sentences2:
        sentences_token2.append(sentence["sentence_token"])
        index_token2.append(sentence["index_token"])

    lemma = sentences1[0]["lemma"]
    
    spacy_languages = {
        "en": "en_core_web_sm",
        "de": "de_core_news_sm",
        "it": "it_core_news_sm",
        "ru": "ru_core_news_sm"
    }
    nlp = spacy.load(spacy_languages[language])
    doc = nlp(lemma)
    pos = doc[0].pos_

    sample_size = min(len(sentences_token1), len(sentences_token2), max_samples)

    rand1 = random.sample(range(len(sentences_token1)), sample_size)
    rand2 = random.sample(range(len(sentences_token2)), sample_size)

    with open(path_output, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
        writer.writerow(["lemmas", "pos", "indexes", "preceding_sentences", "sentences", "following_sentences", "dates", "filenames", "identifiers", "descriptions"])
        for i in rand1:
            writer.writerow([lemma, pos, index_token1[i], " ", sentences_token1[i], " ", "C1", " ", lemma+"-c1-i"+str(i), " "])
        for i in rand2:
            writer.writerow([lemma, pos, index_token2[i], " ", sentences_token2[i], " ", "C2", " ", lemma+"-c2-i"+str(i), " "])


    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")


if __name__ == '__main__':
    main()
