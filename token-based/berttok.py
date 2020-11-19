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
    args = docopt("""

    Usage:
        Bert.py <path_usages> <path_output> <language> <type_sentences>
        
    Arguments:
       
        <path_usages>       = Path to the test sentences
        <path_output>       = Path for storing the vectors
        <language>          = eng / ger / swe / lat
        <type_sentences>    = lemma | token

    """)

    path_usages = args['<path_usages>']
    path_output = args['<path_output>']
    language = args['<language>']
    type_sentences = args['<type_sentences>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Load pre-trained model tokenizer (vocabulary) and model (weights)
    logging.info("Load sentences")
    if language == 'eng':
        tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        model = BertModel.from_pretrained('bert-base-cased', output_hidden_states=True)
    elif language == 'ger':
        tokenizer = BertTokenizer.from_pretrained('bert-base-german-cased')
        model = BertModel.from_pretrained('bert-base-german-cased', output_hidden_states=True)
    elif language == 'swe':
        tokenizer = AutoTokenizer.from_pretrained('KB/bert-base-swedish-cased')
        model = AutoModel.from_pretrained('KB/bert-base-swedish-cased', output_hidden_states=True)
    else:
        tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        model = BertModel.from_pretrained('bert-base-multilingual-cased', output_hidden_states=True)

    # Load sentences 
    context_vector_list = []
    test_sentences = []
    with open(path_usages, 'r') as csvFile:
        reader = csv.DictReader(csvFile, delimiter="\t", quoting=csv.QUOTE_NONE, strict=True)
        for row in reader:
            test_sentences.append(dict(row))
        del(test_sentences[1000:])  # some words have over 20000 usages

        # Create the vectors
        logging.info("Create Bert embeddings")
        for i in range(0, len(test_sentences)):
            try:
                # Create target word(s)
                target_word = str(test_sentences[i]["sentence_"+type_sentences].split()[int([test_sentences[i]["index_"+type_sentences]][0])])
                clean_target_word = "".join(char for char in target_word if char.isalnum() or char == "-" or char == "'")
                original_word = test_sentences[i]["lemma"]
                ind = int(test_sentences[i]["index_"+type_sentences])
                target_words = []
                target_words.append(tokenizer.tokenize(original_word))
                target_words = target_words[0]
                
                # Tokenize text
                text = test_sentences[i]["sentence_"+type_sentences]
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
                    print("Indices not found")
                    break

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
                    sum_vec = np.sum([np.array(token[12]), np.array(token[1])], axis=0)
                    vectors.append(np.array(sum_vec))
                context_vector_list.append(np.sum(vectors, axis=0, dtype=float))
            except:
                print('{} {}'.format('Skipped sentence', i))
        
    
    # Normalize vectors in length
    context_vector_list = preprocessing.normalize(context_vector_list, norm='l2')

    # Save contextVectorList_sparse matrix
    logging.info("Save vectors")
    outSpace = Space(matrix=context_vector_list, rows=" ", columns=" ")
    outSpace.save(path_output)

    logging.info("--- %s seconds ---" % (time.time() - start_time))
    print("")



if __name__ == '__main__':
    main()
