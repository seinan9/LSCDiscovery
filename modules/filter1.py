import csv
import gzip
import logging
import random
import time

from docopt import docopt
import numpy as np
import spacy


def main():
    """
    Detect whether a word is a NOUN, VERB or ADJ.
    """
    # Get the arguments
    args = docopt("""Detect whether a word is a NOUN, VERB or ADJ.

    Usage:
        filter1.py [-tab] <path_words> <path_output> <language>

    Arguments:
        <path_words>    = changing word
        <path_output>   = path to output
        <language>      = en | de | it | ru

    Options:
        -t --tab   includes tab-seperated values


    """)

    path_words = args['<path_words>']
    path_output = args['<path_output>']
    language = args['<language>']

    is_tab = args['--tab']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    spacy_languages = {
        "en": "en_core_web_sm",
        "de": "de_core_news_sm",
        "it": "it_core_news_sm",
        "ru": "ru_core_news_sm"
    }

    if not is_tab:
        with open(path_words, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f]

    else:
        words_tab = {}
        with open(path_words, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
            for row in reader:
                try:
                    words_tab[row[0]] = float(row[1])
                except ValueError:
                    pass
        words = words_tab.keys()

    filtered = []
    nlp = spacy.load(spacy_languages[language])
    progress_counter=0
    for word in words:
        doc = nlp(word)
        for token in doc:
            pos = token.pos_
        if len(doc) == 1:
            if pos == 'NOUN' or pos == 'VERB' or pos == 'ADJ':
                filtered.append(word)
        progress_counter+=1
        logging.info("PROGRESS :"+str(progress_counter)+"/"+str((len(words))))

    with open(path_output, 'w', encoding='utf-8') as f:
        for word in filtered:
            if not is_tab:
                f.write(word + '\n')
            else:
                f.write(word + '\t' + str(words_tab[word]) + '\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
