import csv
import gzip
import logging
import random
import time

from docopt import docopt
import numpy as np
import spacy
from spacy_langdetect import LanguageDetector


def main():
    """
    Detect, whether less or equal to 10 % of word usages contain "foreign langauge or more than 25 % punctuation". 
    """
    # Get the arguments
    args = docopt("""Detect, whether less or equal to 10 % of word usages contain "foreign langauge or more than 25 % punctuation". 

    Usage:
        filter2.py <path_uses1> <path_uses2> <language>

    Arguments:
        <path_uses1>           = path to file containing uses from corpus 1
        <path_uses2>           = path to file containing uses from corpus 2
        <language>             = en | de | it | ru

    """)

    path_uses1 = args['<path_uses1>']
    path_uses2 = args['<path_uses2>']
    language = args['<language>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load sentences 
    sentences1 = []
    with open(path_uses1, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            sentences1.append(row)

    lemma = sentences1[0]["lemma"]

    token1 = []
    ind1 = []
    for sentence in sentences1:
        token1.append(sentence["sentence_token"])
        ind1.append(int(sentence["index_token"]))

    sentences2 = []
    with open(path_uses2, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            sentences2.append(row)

    token2 = []
    ind2 = []
    for sentence in sentences2:
        token2.append(sentence["sentence_token"])
        ind2.append(int(sentence["index_token"]))

    # Load spacy model 
    spacy_langauges = {
        "en": "en_core_web_sm",
        "de": "de_core_news_sm",
        "it": "it_core_news_sm",
        "ru": "ru_core_news_sm"
    }

    nlp = spacy.load(spacy_langauges[language])
    nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)

    # Count unwanted uses in c1
    counter1 = 0
    for i in range(len(token1)):
        try:
            sentence = token1[i]
            ind = ind1[i]
            word = sentence.split()[ind]
            clean_word = "".join(char for k,char in enumerate(word) if char.isalpha() or char == "-" or (char == "'" and k == len(word)-1))
            if clean_word[-1] == "'":
                clean_word = lemma
                sentence = sentence.replace(word, clean_word) #Absprechen
            doc = nlp(sentence)
            doclist = [str(token) for token in doc]
            index = doclist.index(clean_word)
            pos = doc[index].pos_
            counter_punct1 = np.mean([1 if token.pos_ == 'PUNCT' else 0 for token in doc])
            if not (pos == 'NOUN' or pos == 'VERB' or pos == 'ADJ'):
                counter1 += 1
            elif doc._.language['language'] != language:
                counter1 += 1
            elif counter_punct1 > 0.25:
                counter1 += 1
        except ValueError:
            counter1 += 1

    # Count unwanted uses in c2
    counter2 = 0
    for i in range(len(token2)):
        try:
            sentence = token2[i]
            ind = ind2[i]
            word = sentence.split()[ind]
            clean_word = "".join(char for k,char in enumerate(word) if char.isalpha() or char == "-" or (char == "'" and k == len(word)-1))
            if clean_word[-1] == "'":
                clean_word = lemma
                sentence = sentence.replace(word, clean_word)
            doc = nlp(sentence)
            doclist = [str(token) for token in doc]
            index = doclist.index(clean_word)
            pos = doc[index].pos_
            counter_punct2 = np.mean([1 if token.pos_ == 'PUNCT' else 0 for token in doc])
            if not (pos == 'NOUN' or pos == 'VERB' or pos == 'ADJ'):
                counter2 += 1
            elif doc._.language['language'] != language:
                counter2 += 1
            elif counter_punct2 > 0.25:
                counter2 += 1
        except ValueError:
            counter2 += 1

    percent1 = counter1/len(token1)
    percent2 = counter2/len(token2)
    threshold = 0.1

    # Print 1 if prediction passed the filter else 0
    if percent1 <= threshold and percent2 <= threshold:
        print(1)
    else:
        print(0)

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
