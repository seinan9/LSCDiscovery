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
        filter1.py <word> <language>

    Arguments:
        <word>      = changing word
        <language>  = en | de | it | ru

    """)

    word = str(args['<word>'])
    language = args['<language>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    spacy_langauges = {
        "en": "en_core_web_sm",
        "de": "de_core_news_sm",
        "it": "it_core_news_sm",
        "ru": "ru_core_news_sm"
    }

    nlp = spacy.load(spacy_langauges[language])
    doc = nlp(word)
    if doc[0].pos_ == "NOUN" or doc[0].pos_ == "VERB" or doc[0].pos_ == "ADJ":
        print(1)
    else:
        print(0)

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
