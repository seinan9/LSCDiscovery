#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import gzip
import logging
import random
import time

from docopt import docopt
from fuzzywuzzy import fuzz
import re
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
    rows1 = []
    with open(path_usages1, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        next(reader, None)
        for row in reader:
            rows1.append(row)

    rows2 = []
    with open(path_usages2, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        next(reader, None)
        for row in reader:
            rows2.append(row)

    lemma = rows1[0][4]
    spacy_languages = {
        "en": "en_core_web_sm",
        "de": "de_core_news_sm",
        "it": "it_core_news_sm",
        "ru": "ru_core_news_sm"
    }
    nlp = spacy.load(spacy_languages[language])
    doc = nlp(lemma)
    pos = doc[0].pos_

    sample_size = min(len(rows1), len(rows2), max_samples)

    rand_idx1 = random.sample(range(len(rows1)), sample_size)
    rand_idx2 = random.sample(range(len(rows2)), sample_size)

    rand_rows1 = []
    rand_rows2 = []

    for i in rand_idx1:
        rand_rows1.append(rows1[i])

    for i in rand_idx2:
        rand_rows2.append(rows2[i])

    header = ["lemma", "pos", "date", "grouping", "identifier", "description", "context", "indexes_target_token", "indexes_target_sentence"]

    final_rows1 = []

    for i in range(0, len(rand_rows1)):
        context_chars = [char for char in rand_rows1[i][1]]
        context_words = re.split(r'(\s+)', rand_rows1[i][1])
        context_words_no_spaces = rand_rows1[i][1].split()

        target = context_words_no_spaces[int(rand_rows1[i][3])]
        index_with_spaces = context_words.index(target)

        before_word = context_words[0:index_with_spaces]
        before_word_chars = [char for char in "".join(before_word)]

        tok_start = len(before_word_chars)
        tok_end = tok_start + len([char for char in target])
        indexes_target_token = str(tok_start) + ":" + str(tok_end)

        sen_end = len(context_chars)
        indexes_target_sentence = "0" + ":" + str(sen_end)

        context = rand_rows1[i][1]

        final_rows1.append([lemma, pos, "C1", " ", lemma+"-c1-i"+str(i), " ", context, indexes_target_token, indexes_target_sentence])

    final_rows2 = []

    for i in range(0, len(rand_rows2)):
        context_chars = [char for char in rand_rows2[i][1]]
        context_words = re.split(r'(\s+)', rand_rows2[i][1])
        context_words_no_spaces = rand_rows2[i][1].split()

        target = context_words_no_spaces[int(rand_rows2[i][3])]
        index_with_spaces = context_words.index(target)

        before_word = context_words[0:index_with_spaces]
        before_word_chars = [char for char in "".join(before_word)]

        tok_start = len(before_word_chars)
        tok_end = tok_start + len([char for char in target])
        indexes_target_token = str(tok_start) + ":" + str(tok_end)

        sen_end = len(context_chars)
        indexes_target_sentence = "0" + ":" + str(sen_end)

        context = rand_rows2[i][1]

        final_rows2.append([lemma, pos, "C2", " ", lemma+"-c2-i"+str(i), " ", context, indexes_target_token, indexes_target_sentence])


    with open(path_output, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
        writer.writerow(header)
        for i in final_rows1:
            writer.writerow(i)
        for i in final_rows2:
            writer.writerow(i)


    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")


if __name__ == '__main__':
    main()
