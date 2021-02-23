# LSCDiscovery

  * [General](#general)
  * [Quick Start](#quick-start)
  * [Usage](#usage)
  * [Pepare Data](#prepare-data)
  * [Automated LSC Discovery](#automated-lsc-discovery)
    + [Static Approach](#static-approach)
    + [Contextualized Approach](#contextualized-approach)
  * [Automated Binary Classification and Graded Ranking](#automated-binary-classification-and-graded-ranking)
    + [Static Approach](#static-approach)
    + [Contextualized Approach](#contextualized-approach)
  * [Parameter Settings](#parameter-settings)
  * [BibTex](#bibtex)


### General

The framework utilizes common approaches for Lexical Semantic Change (LSC) Detection to discover changing words:

> Given a corpus pair C1,C2, automatically discover words that undergo a meaning change between C1 and C2.

The framework can also be used for Binary Classification and Graded Ranking:

> Given a corpus pair C1,C2 and a list of target words, automatically decide which target words lost or gained sense(s) between C1 and C2.

> Given a corpus pair C1,C2 and a list of target words, automatically rank the target words according to their degree of LSC between C1 and C2.

Additional tools are provided for evaluation and fine-tuning.

Currently only English and German are fully supported. 

If you use this software for academic research, please [cite](#bibtex) these papers:

Also make sure you give appropriate credit to the below-mentioned software this repository depends on.

Parts of the code rely on [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy), [gensim](https://github.com/rare-technologies/gensim), [numpy](https://pypi.org/project/numpy/), [torch](https://pypi.org/project/torch/), [transformers](https://huggingface.co/transformers/), [scikit-learn](https://pypi.org/project/scikit-learn/), [scipy](https://pypi.org/project/scipy/), [spaCy](https://spacy.io/), [VecMap](https://github.com/artetxem/vecmap)


### Usage

The scripts should be run directly from the main directory. All scripts can be run directly from the command line:

	bash scripts/rank_bert.sh <data_set_id> <language> <type> <layers>

The usage of each script (including .py scripts) can be understood by running it with help option `-h`, e.g.:

	bash scripts/rank_bert.sh -h

It is strongly recommend to run the scripts within a [virtual environment](https://pypi.org/project/virtualenv/) with Python 3.9.1. Install the required packages running `pip install -r requirements.txt`. Download the spaCy trained pipeline for English running `python -m spacy download en_core_web_sm` and German running `python -m spacy download de_core_news_sm`.

### Quick Start

Given a lemmatized corpus pair C1, C2 the following steps need to be executed to obtain a set of discovered changing words:
1. `bash scripts/prepare_data.sh <data_set_id> <path_corpus1> <path_corpus2>`
2. `bash scripts/discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t> <language>`

Consider the following example using the English SemEval-2020 data set:
1. `bash scripts/prepare_data.sh en_semeval corpus1.txt.gz corpus2.txt.gz`
2. `bash scripts/discover_sgns.sh en_semeval 10 50 5 0.001 3 3 5 1.0 en`


### Prepare Data

The minimum required data is a corpus pair C1, C2. The data can be prepared by running `bash scripts/prepare_data.sh <data_set_id> <path_corpus1> <path_corpus2>`. While the framework can be used for automatic discovery with only a single corpus pair, it is sub-optimal and hence not recommended.  

To recommend data is the following:
1. lemmatized corpus pair (in .txt.gz format)
2. raw corpus pair (in .txt.gz format)

The following data is only required for binary classification and graded ranking:
1. a file containing target words (one word per line)

These are required for evaluation and fine-tuning:
1. binary and graded gold data (one word-value pair per line, tab seperated)

Use the following script to bring the data into the required format:

	bash scripts/prepare_data.sh <data_set_id> <path_corpus1_lemma> <path_corpus2_lemma> <path_corpus1_token> <path_corpus2_token> [<path_targets>] [<path_binary_gold>] [<path_graded_gold>]

It is recommeded to choose a unique and descriptive data set identifier <data_set_id>. All automated scripts utilize the data set identifier to obtain the required data. 

The English and German SemEval-2020 data sets can be imported by running `bash scripts/get_semeval_en.sh` and `bash scripts/get_semeval_de.sh` respectively. 


### Automated LSC Discovery

#### Static Approach

The following steps are executed to discover changing words in the intersection of the corpus vacabularies:
1. create static word embeddings (`type-based/sgns.py`)
2. length-normalize, mean-center and align word embeddings (`modules/map_embeddings.py`) 
3. measure differences (`measures/cd.py`)
4. calculate threshold and label changing words (`measures/binary.py`)
5. filter out undesirable words (`modules/filter1.py`)

Optional:
1. filter on a usage-level (`modules/filter2.py`)
2. store usages for predictions in format for DURel annotation system

A shell script is provided that automatically executes the described steps to obtain a set of changing words:

	bash scripts/discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t> <language> [<sample_id>] [<sample_size>] [<max_usages>] [<max_samples>]

Steps (1) to (5) are executed by providing the parameters until (including) `<language>`, e.g.,:

	bash scripts/discover_sgns.sh data/en_semeval 10 50 5 0.001 3 3 5 0.1 en
	
When the script is exectued with values for the optional parameters `[<sample_id>]`, `[<sample_size>]` and `[<max_usages>]`, the optional step (1) is also executed, e.g.:

	bash scripts/discover_sgns.sh data/en_semeval 10 50 5 0.001 3 3 5 0.1 en sample_1 100 25
	
When all parameters are provided, the optional step (2) is also executed, e.g.:

	bash scripts/discover_sgns.sh data/en_semeval 10 50 5 0.001 3 3 5 0.1 en sample_1 100 25 25
	
	
#### Contextualized Approach

BERT requires word usages to generate contextualized word embeddings. Extracting usages for a large amount of words and creating contextualized word embeddings for them afterwards is computationally expensive. We recommend to use a sample of the vocabularies intersection. 

The following steps are executed to discover changing words in the intersection of the corpus vacabularies:
1. filter out undesirable words from the vocabularies intersection (`modules/filter1.py`)
2. sample words (`modules/sample.py`)
3. extract usages for sampled words (`modules/extract_usages.py`)
4. create contextualized word embeddings (`token-based/bert.py`)
5. measure differences (`measures/apd.py` or `measures/cos.py`)
6. calculate threshold and label changing words (`measures/binary.py`)

Note: Filter1 is applied before the sampling (2), to not waste computational power on undesirable words.

Optional:
1. filter on a usage-level (`modules/filter2.py`) 
2. store usages for predictions in format for DURel annotation system (`modules/make_format.py`)

A shell script is provided that automatically executes (1) to (3):

	bash scripts/prepare_sample.sh <data_set_id> <sample_id> <sample_size> <max_usages> <language>

e.g.

	bash scripts/prepare_sample.sh en_semeval sample_1 100 25 en 

A shell script is provided that automatically executes the described steps to obtain a set of changing words:

	bash scripts/discover_bert.sh <data_set_id> <sample_id> <language> <type> <layers> <t> [<f2>] [<max_samples>]

Steps (4) to (6) are executed by providing the parameters until (including) `<t<`, e.g.:

	bash scripts/discover_bert.sh en_semeval sample_1 en token 1+12 0.1 

When the script is exectued with values for the optional parameter `[<f2>]`, the optional step (1) is also executed, e.g.:

	bash scripts/discover_bert.sh en_semeval sample_1 en token 1+12 0.1 f2


When all parameters are provided, the optional step (2) is also executed, e.g.:

	bash scripts/discover_bert.sh en_semeval sample_1 en token 1+12 0.1 25


### Automated Binary Classification and Graded Ranking

#### Static Approach

The following script can be used to automatically decide for a list of target words, which words lost or gained sense(s) between C_1 and C_2:

	bash scripts/classify_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t>

The following script can be used to automatically rank a set of target words according to their degree of LSC between C_1 and C_2:

	bash scripts/classify_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> 

#### Contextualized Approach

Again, BERT requires word usags. If word usages were already extracted for the automatic LSC Discovery, you can use these by providing the `<sample_id>`. Otherwise, the follo

	bash scripts/prepare_sample.sh en_semeval sample_1 100 25 en 

The following script can be used to automatically decide for a list of target words, which words lost or gained sense(s) between C_1 and C_2:

	bash scripts/classify_sgns.sh <data_set_id> <sample_id> <language> <type> <layers> <t>

The following script can be used to automatically rank a set of target words according to their degree of LSC between C_1 and C_2:

	bash scripts/classify_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> 
	
### Parameter Settings
TODO

BibTex
--------

```
@bachelorsthesis{Kurtyigit2021,
title={{Lexical Semantic Change Discovery}},
author={Kurtyigit, Sinan},
year={2021},
school = {Institute for Natural Language Processing, University of Stuttgart},
address = {Stuttgart}
}
```
