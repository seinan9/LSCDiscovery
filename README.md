# LSCDiscovery

  * [General](#general)
  * [Usage](#usage)
  * [Pepare Data](#prepare-data)
  * [Automated LSC Discovery](#automated-lsc-discovery)
    + [Static Approach](#static-approach)
    + [Contextualized Approach](#contextualized-approach)


### General

A framework that utilizes common approaches for Lexical Semantic Change (LSC) Detection to solve the task of LSC Discovery:
> Given a corpus pair (C1,C2), decide for the intersection of their vocabularies which words lost or gained sense(s) between C_1 and C_2.

The following is provided:
- scripts to automatically solve the LSC Discovery task 
- scripts to automatically solve the Binary Classification subtask
- scripts to automatically solve the Graded Ranking subtask 
- tools to evaluate and fine-tune the results 

Currently only English and German are fully supported. 

If you use this software for academic research, please [cite](#bibtex) these papers:

Also make sure you give appropriate credit to the below-mentioned software this repository depends on.

Parts of the code rely on [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy), [torch](https://pypi.org/project/torch/), [transformers](https://huggingface.co/transformers/), [spaCy](https://spacy.io/), [gensim](https://github.com/rare-technologies/gensim), [numpy](https://pypi.org/project/numpy/), [scikit-learn](https://pypi.org/project/scikit-learn/), [scipy](https://pypi.org/project/scipy/), [VecMap](https://github.com/artetxem/vecmap


### Usage

The scripts should be run directly from the main directory. All scripts can be run directly from the command line:

	python measures/cd.py <path_matrix1> <path_matrix2> <path_targets> <path_output>

The usage of each script (including .sh scripts) can be understood by running it with help option `-h`, e.g.:

	python measures/cd.py -h

It is strongly recommend to run the scripts within a [virtual environment](https://pypi.org/project/virtualenv/) with Python 3.9.1. Install the required packages running `pip install -r requirements.txt`. Download the spaCy trained pipeline for English running `python -m spacy download en_core_web_sm` and German running `python -m spacy download de_core_news_sm`.


#### Prepare Data

The minimum required data is the following:
1. lemmatized corpus pair (in .txt.gz format)
2. raw corpus pair (in .txt.gz format)

The following data is optional:
1. a file containing target words (one word per line)
2. binary and graded gold data (one word-value pair per line, tab seperated)

A shell script is provided to bring the data into the required format:

	bash scripts/prepare_data.sh <data_set_id> <path_corpus1_lemma> <path_corpus2_lemma> <path_corpus1_token> <path_corpus2_token> [path_targets] [path_binary_gold] [path_graded_gold]
	
It is recommeded to choose a unique and descriptive data set identifier <data_set_id>. All automated scripts utilize the data set identifier to obtain the required data. 

The English and German SemEval-2020 data sets can be imported by running `bash scripts/get_semeval_en.sh` and `bash scripts/get_semeval_de.sh` respectively. 


### Automatic LSC Discovery

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

	bash scripts/discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t> <language> [sample_id] [sample_size] [max_usages] [max_samples]

Steps 1a to 4a are executed by providing the parameters until (including) `language`, e.g.,:

	bash scripts/discover_sgns.sh data/en_semeval 10 50 5 0.001 3 3 5 0.1 en
	
When the script is exectued with values for the optional parameters `[sample_id]`, `[sample_size]` and `[max_usages]`, (4b) is also executed, e.g.:

	bash scripts/discover_sgns.sh data/en_semeval 10 50 5 0.001 3 3 5 0.1 en sample_1 100 25
	
When all parameters are provided, (5) is also executed, e.g.:

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
Note: filter1 is applied before the sampling, to not waste computational power on undesirable words.

Optional:
1. filter on a usage-level (`modules/filter2.py`) 
2. store usages for predictions in format for DURel annotation system

A shell script is provided that automatically executes (0a) to (0c):

	bash scripts/prepare_sample.sh <data_set_id> <sample_id> <sample_size> <max_usages> <language>

e.g.

	bash scripts/prepare_sample.sh en_semeval sample_1 100 25 en 

A shell script is provided that automatically executes the described steps to obtain a set of changing words:

	bash scripts/discover_bert.sh <data_set_id> <sample_id> <language> <type> <layers> <t> [f2] [max_samples]

Steps (1) to (3) are executed by providing the parameters until (including) `t`, e.g.:

	bash scripts/discover_bert.sh en_semeval sample_1 en token 1+12 0.1 

When the script is exectued with values for the optional parameter `f2`, (4b) is also executed, e.g.:

	bash scripts/discover_bert.sh en_semeval sample_1 en token 1+12 0.1 f2


When all parameters are provided, (5) is also executed, e.g.:

	bash scripts/discover_bert.sh en_semeval sample_1 en token 1+12 0.1 25
