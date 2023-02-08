#!/usr/bin/env python
import csv
import gzip
import logging
import sys
sys.path.append('./modules/')
import time

from docopt import docopt
import numpy as np
from sklearn import preprocessing
import torch
from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModel

from utils_ import Space


def main():

    # Get the arguments
    args = docopt("""Create token-based embeddings with BERT.

    Usage:
        bert.py [-l] <path_usages> <path_output> <language> <type_sentences> <layers>
        
    Arguments:
       
        <path_usages>       = Path to the test sentences
        <path_output>       = Path for storing the vectors
        <language>          = en | de
        <type_sentences>    = lemma | token | toklem
        <layers>            = TODO
    
    Options:
        -l, --len           normalize vectors to unit length 

    """)

    path_usages = args['<path_usages>']
    path_output = args['<path_output>']
    language = args['<language>']
    type_sentences = args['<type_sentences>']
    layers = args['<layers>']

    is_len = args['--len']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load pre-trained model tokenizer (vocabulary) and model (weights)
    model_language = {
        'en-large': 'bert-large-cased', 
        'en': 'bert-base-cased', 
        'de': 'bert-base-german-cased', 
        'sw': 'KB/bert-base-swedish-cased', 
        'multi': 'bert-base-multilingual-cased'
        }

    tokenizer = BertTokenizer.from_pretrained(model_language[language])
    model = BertModel.from_pretrained(model_language[language], output_hidden_states=True)

    if type_sentences == 'toklem':
        type_ = 'token'
    else:
        type_ = type_sentences


    # Load sentences 
    context_vector_list = []
    test_sentences = []
    with open(path_usages, 'r') as csvFile:
        reader = csv.DictReader(csvFile, delimiter="\t", quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            test_sentences.append(dict(row))

        # Create the vectors
        for i in range(0, len(test_sentences)):
            try:
                # Create target word(s)
                target_words = []
                target_word = str(test_sentences[i]["sentence_"+type_].split()[int([test_sentences[i]["index_"+type_]][0])])
                if type_sentences == 'toklem':
                    original_word = test_sentences[i]["lemma"]
                    target_words.append(tokenizer.tokenize(original_word))
                else:
                    clean_target_word = "".join(char for k,char in enumerate(target_word) if char.isalpha() or char == "-" or (char == "'" and k == len(target_word)-1))
                    if clean_target_word[-1] == "'":
                        clean_target_word = test_sentences[i]["lemma"]
                    target_words.append(tokenizer.tokenize(clean_target_word))
                target_words = target_words[0]
                
                # Tokenize text
                text = test_sentences[i]["sentence_"+type_]
                if type_sentences == 'toklem':
                    text = text.replace(target_word, original_word) 
                marked_text = "[CLS] " + text + " [SEP]"
                tokenized_text = tokenizer.tokenize(marked_text)
            
                # Search the indices of the tokenized target word in the tokenized text
                target_word_indices = []
                for j in range(0, len(tokenized_text)):
                    if tokenized_text[j] == target_words[0]:
                        for l in range(0, len(target_words)):
                            if tokenized_text[j+l] == target_words[l]:
                                target_word_indices.append(j+l)
                            if len(target_word_indices) == len(target_words):
                                break
                
                if len(target_word_indices) == 0:
                    logging.info("INDICES NOT FOUND. SKIPPED SENTENCE "+str(i))
                    continue

                # Trim tokenized_text if longer than 512
                if len(tokenized_text) > 512:
                    while (len(tokenized_text) > 512):
                        if tokenized_text[-1] != tokenized_text[target_word_indices[-1]]:
                            del(tokenized_text[-1])
                        else:
                            del(tokenized_text[0])
                            for index, value in enumerate(target_word_indices):
                                target_word_indices[index] -= 1
                
                # Create BERT Token Embeddings
                indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
                segments_ids = [1] * len(tokenized_text)
                tokens_tensor = torch.tensor([indexed_tokens])
                segments_tensors = torch.tensor([segments_ids])
                model.eval()
                with torch.no_grad():
                    outputs = model(tokens_tensor, segments_tensors)
                    hidden_states = outputs[2]
                token_embeddings = torch.stack(hidden_states, dim=0)
                token_embeddings = torch.squeeze(token_embeddings, dim=1)
                token_embeddings = token_embeddings.permute(1, 0, 2)
                vectors = []
                for number in target_word_indices:
                    token = token_embeddings[number]
                    layers_list = layers.split('+')
                    layers_list = list(map(int, layers_list))
                    #vec = [np.array(token[l]) for l in layers_list]
                    sum_vec = np.sum([np.array(token[l]) for l in layers_list], axis=0)
                    #sum_vec = np.sum([np.array(token[12]), np.array(token[1])], axis=0)
                    vectors.append(np.array(sum_vec))
                context_vector_list.append(np.sum(vectors, axis=0, dtype=float))
            except:
                logging.info("SKIPPED SENTENCE "+str(i))
        
    
    # Normalize vectors in length
    if is_len:
        context_vector_list = preprocessing.normalize(context_vector_list, norm='l2')

    # Save contextVectorList_sparse matrix
    outSpace = Space(matrix=context_vector_list, rows=" ", columns=" ")
    outSpace.save(path_output)

    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")



if __name__ == '__main__':
    main()
