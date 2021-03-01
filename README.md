# LSCDiscovery

  * [General](#general)
  * [Usage](#usage)
  * [Quick Start](#quick-start)
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

Given a corpus pair (C1,C2) (e.g., from different time periods, domains, genres etc.), this repository can be used to discover semantically changing words between them. 

The repository can also be used to decide for a set of words, which words gained or lost sense(s) between C1 and C2 (binary classification task) or rank the words according to their degree of semantic change between C1 and C2 (graded ranking task) ([SemEval-2020](https://arxiv.org/abs/2007.11464)).

Additional tools are provided for evaluation and fine-tuning.

Currently only English and German are fully supported. However, large parts of the repository can still be used for other languages. Please take a look at the documentation in the code for more details.

If you use this software for academic research, please [cite](#bibtex) these papers:

Also make sure you give appropriate credit to the below-mentioned software this repository depends on.

Parts of the code rely on [LSCDetection](https://github.com/Garrafao/LSCDetection), [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy), [gensim](https://github.com/rare-technologies/gensim), [numpy](https://pypi.org/project/numpy/), [torch](https://pypi.org/project/torch/), [transformers](https://huggingface.co/transformers/), [scikit-learn](https://pypi.org/project/scikit-learn/), [scipy](https://pypi.org/project/scipy/), [spaCy](https://spacy.io/), [VecMap](https://github.com/artetxem/vecmap)


### Usage

The scripts should be run directly from the main directory. All scripts can be run directly from the command line:

	bash scripts/rank_bert.sh <data_set_id> <language> <type> <layers>

The usage of each script (including .py scripts) can be understood by running it with help option `-h`, e.g.:

	bash scripts/rank_bert.sh -h

It is strongly recommend to run the scripts within a [virtual environment](https://pypi.org/project/virtualenv/) with Python 3.9.1. Install the required packages running `pip install -r requirements.txt`. Download the spaCy trained pipeline for English running `python -m spacy download en_core_web_sm` and German running `python -m spacy download de_core_news_sm`.

### Quick Start

Given a corpus pair C1, C2 the following steps need to be executed to discover changing words:
1. `bash scripts/prepare_data.sh <data_set_id> <path_corpus1> <path_corpus2>`
2. `bash scripts/discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t> <language>`

Consider the following example:
1. `bash scripts/prepare_data.sh test_data path_to_corpus1/corpus1.txt.gz path_to_corpus2/corpus2.txt.gz`
2. `bash scripts/discover_sgns.sh test_data 10 50 5 0.001 3 3 5 1.0 en`


### Prepare Data

The repository can be used with only one corpus pair (raw or lemmatized). The data can be prepared by running `bash scripts/prepare_data.sh <data_set_id> <path_corpus1> <path_corpus2>`.<sup>[1](#myfootnote1)</sup>

However, the recommend input data is the following:
1. lemmatized corpus pair (in .txt.gz format)
2. raw corpus pair (in .txt.gz format)

To classify (binary classification task) or rank (graded ranking task) a set of target words, the following is also required:

3. a file containing target words (one word per line in .txt, .csv or .tsv format)

If the models shall be evaluated or tuned on exisiting gold data, the following has to be provided as well:

4. binary and graded gold data (one word-value pair per line, tab seperated in .txt, .csv or .tsv format)

Use the following script to bring the data into the required format:

	bash scripts/prepare_data.sh <data_set_id> <path_corpus1_lemma> <path_corpus2_lemma> <path_corpus1_token> <path_corpus2_token> [<path_targets>] [<path_binary_gold>] [<path_graded_gold>]

It is recommeded to choose a unique and descriptive data set identifier <data_set_id>. All automated scripts utilize the data set identifier to obtain the required data. 

The English and German [SemEval-2020 data sets](https://www.ims.uni-stuttgart.de/en/research/resources/corpora/sem-eval-ulscd/) can be imported by running `bash scripts/get_semeval_en.sh` and `bash scripts/get_semeval_de.sh` respectively. 

Note that you can use all data sets found in [LSCDetection](https://github.com/Garrafao/LSCDetection).

### Automated LSC Discovery

#### Static Approach

The following steps are executed to discover changing words in the vocabulary intersection:
1. create static word embeddings (`type-based/sgns.py`)
2. length-normalize, mean-center and align word embeddings (`modules/map_embeddings.py`) 
3. measure differences (`measures/cd.py`)
4. calculate threshold and label changing words (`measures/binary.py`)
5. filter out undesirable words (`modules/filter1.py`)

Optional:

6. filter on a usage-level (`modules/filter2.py`)
7. store usages for predictions in format for DURel annotation system

A shell script is provided that automatically executes the described steps to obtain a set of changing words:

	bash scripts/discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t> <language> [<sample_id>] [<sample_size>] [<max_usages>] [<max_samples>]

Steps 1 to 5 are executed by providing the parameters until (including) `<language>`, e.g.,:

	bash scripts/discover_sgns.sh data/en_semeval 10 50 5 0.001 3 3 5 0.1 en
	
When the script is exectued with values for the optional parameters `[<sample_id>]`, `[<sample_size>]` and `[<max_usages>]`, 6 is also executed, e.g.:

	bash scripts/discover_sgns.sh data/en_semeval 10 50 5 0.001 3 3 5 0.1 en sample_1 100 25
	
When all parameters are provided, 7 is also executed, e.g.:

	bash scripts/discover_sgns.sh data/en_semeval 10 50 5 0.001 3 3 5 0.1 en sample_1 100 25 25
	
	
#### Contextualized Approach

BERT requires word usages to generate contextualized word embeddings. Extracting usages for a large amount of words and creating contextualized word embeddings for them afterwards is computationally expensive. We recommend to use a sample of the vocabularies intersection. 

The following steps are executed to discover changing words in the vocabulary intersection:
1. filter out undesirable words from the vocabulary intersection (`modules/filter1.py`)
2. sample words from filtered vocabulary intersection (`modules/sample.py`)
3. extract usages for sampled words (`modules/extract_usages.py`)
4. extract contextualized word embeddings (`token-based/bert.py`)
5. measure differences (`measures/apd.py` or `measures/cos.py`)
6. calculate threshold and label changing words (`measures/binary.py`)

Note: Filter1 is applied before the sampling (2), to not waste computational power on undesirable words.

Optional:

7. filter on a usage-level (`modules/filter2.py`)
8. store usages for predictions in format for DURel annotation system (`modules/make_format.py`)

A shell script is provided that automatically executes 1 to 3:

	bash scripts/prepare_sample.sh <data_set_id> <sample_id> <sample_size> <max_usages> <language>

e.g.

	bash scripts/prepare_sample.sh en_semeval sample_1 100 25 en 

A shell script is provided that automatically executes the described steps to obtain a set of changing words:

	bash scripts/discover_bert.sh <data_set_id> <sample_id> <language> <type> <layers> <t> [<f2>] [<max_samples>]

Steps 4 to 6 are executed by providing the parameters until (including) `<t<`, e.g.:

	bash scripts/discover_bert.sh en_semeval sample_1 en token 1+12 0.1 

When the script is exectued with values for the optional parameter `[<f2>]`, 7 is also executed, e.g.:

	bash scripts/discover_bert.sh en_semeval sample_1 en token 1+12 0.1 f2


When all parameters are provided, 8 is also executed, e.g.:

	bash scripts/discover_bert.sh en_semeval sample_1 en token 1+12 0.1 f2 25


### Automated Binary Classification and Graded Ranking

#### Static Approach

The following script can be used to solve the binary classification task:

	bash scripts/classify_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t>

The following script can be used to solve the graded ranking task:

	bash scripts/classify_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> 

#### Contextualized Approach

BERT requires word usages. If word usages were already extracted earlier, you can use these by providing the `<sample_id>`. Otherwise, the following can be executed:

	bash scripts/prepare_sample.sh en_semeval sample_1 100 25 en 

The following script can be used to solve the binary classification task:

	bash scripts/classify_sgns.sh <data_set_id> <sample_id> <language> <type> <layers> <t>

The following script can be used to solve the graded ranking task:

	bash scripts/classify_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> 
	
### Parameter Settings

In this section a description of the parameters as well as their recommended values for both languages are provided. Find detailed notes on model performances and optimal parameter settings in [these papers](#bibtex).


#### Static Approach

	bash scripts/discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t> <language> [<sample_id>] [<sample_size>] [<max_usages>] [<max_samples>]

| Parameter | Description | Recommended EN | Recommended DE |
| --- | --- | --- | --- |
| `<data_set_id>` | Data set identifier | an expressive id | a expressive id |
| `<window_size>` | The linear distance of context words to consider in each direction | 10 | 10 |
| `<dim>` | Dimensionality of embeddings | 300 | 300 |
| `<k>` | Number of negative parameter | 5 | 5 |
| `<s>` | Threshold for subsampling | 0.001 | 0.001 |
| `<min_count1>` | Number of occurences for a word to be included in the vocabulary of C1 | 4 | 39 |
| `<min_count2>` | Number of occurences for a word to be included in the vocabulary of C2 | 4 | 39 |
| `<itera>` | Number of iterations | 5 | 5 |
| `<t>` | Threshold = mean + t * standard deviation | 1.0 | 1.0 |
| `<language` | English or German | en | de |
| `<sample_id>` | Sample identifer | an expressive id | an expressive id |
| `<sample_size>` | Number of words to be sampled from filtered words (after filter1)  | 500 | 500 | 
| `<max_usages>` | Max. number of usages to be extracted from each corpus | 100 | 100 |
| `<max_samples>` | Max. number of samples stored for annotation | 50 | 50 |


#### Contextualized Approach

	bash scripts/prepare_sample.sh <data_set_id> <sample_id> <sample_size> <max_usages> <language>

| Parameter | Description | Recommended EN | Recommended DE |
| --- | --- | --- | --- |
| `<data_set_id>` | Data set identifier | an expressive id | an expressive id |
| `<sample_id>` | Sample identifier | an expressive id | an expressive id |
| `<sample_size>` | Number of words to be sampled from vocabulary intersection | 500 | 500 | 
| `<max_usages>` | Max. number of usages to be extracted from each corpus | 100 | 100 |
| `<language>` | English or German | en | de |

	bash scripts/discover_bert.sh <data_set_id> <sample_id> <language> <type> <layers> <t> <f2> <max_samples> 

| Parameter | Description | Recommended EN | Recommended DE |
| --- | --- | --- | --- |
| `<data_set_id>` | Data set identifier | an expressive id | an expressive id |
| `<sample_id>` | Sample identifier | an expressive id | an expressive id |
| `<language>` | En or de | en | de |
| `<type>` | Lemma or token or toklem | token | toklem |
| `<layers>` | Which layers to extract embeddings from. All possible combinations including numbers from 1 to 12 seperated by `+` | 1+12 | 1+12 | 
| `<t>` | Threshold = mean + t * standard deviation | 0.1 | 1.0 |
| `<f2>` | If you want to apply the second filter write f2 | f2 | f2 |
| `<max_samples>` | Max. number of usages to be extracted from each corpus | 50 | 50 |


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
```
@inproceedings{Kaiser2021effects,
    title = "Effects of Pre- and Post-Processing on type-based Embeddings in Lexical Semantic Change Detection",
    author = "Kaiser, Jens and Kurtyigit, Sinan and Kotchourko, Serge and Schlechtweg, Dominik",
    booktitle = "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics",
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics"
}
```
```
@InProceedings{Laicher2021explaining,
author = {Laicher, Severin and Kurtyigit, Sinan and Schlechtweg, Dominik and Kuhn, Jonas and {Schulte im Walde}, Sabine},
title = {{Explaining and Improving BERT Performance on Lexical Semantic Change Detection}},
    booktitle = "{Proceedings of the Student Research Workshop at the 16th Conference of the European Chapter of the Association for Computational Linguistics}",
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
}
```
<a name="myfootnote1">1</a>: While the framework can be used for automatic discovery with only a single corpus pair, it is sub-optimal and hence not recommended.

