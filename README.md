# LSCDiscovery

  * [General](#general)
  * [Usage](#usage)
  * [Automated LSC Discovery](#automated-lsc-discovery)
    + [Prepare Data](#prepare-data)
    + [Static Approach](#static-approach)
    + [Contextualized Approach](#contextualized-approach)
  * [Automated Binary Classification and Graded Ranking](#automated-binary-classification-and-graded-ranking)
    + [Prepare Data](#prepare-data)
    + [Static Approach](#static-approach)
    + [Contextualized Approach](#contextualized-approach)
  * [Parameter Settings](#parameter-settings)


### General

A framework that utilizes common approaches for Lexical Semantic Change (LSC) Detection to solve the task of Lexical Semantic Change Discovery:
> Given a corpus pair (C1,C2), decide for the intersection of their vocabularies which words lost or gained sense(s) between $C_1$ and $C_2$.

Furthermore, additional tools are provided to solve task related to the field of Lexical Semantic Change Detection, e.g., the binary classification and graded ranking.

Currently only English and German are fully supported. 

If you use this software for academic research, please [cite](#bibtex) these papers:

Also make sure you give appropriate credit to the below-mentioned software this repository depends on.

Parts of the code rely on [DISSECT](https://github.com/composes-toolkit/dissect), [gensim](https://github.com/rare-technologies/gensim), [numpy](https://pypi.org/project/numpy/), [scikit-learn](https://pypi.org/project/scikit-learn/), [scipy](https://pypi.org/project/scipy/), [VecMap](https://github.com/artetxem/vecmap).


### Usage

The scripts should be run directly from the main directory. All scripts can be run directly from the command line:

	python type-based/count.py <path_corpus> <path_output> <window_size>

e.g.

	python type-based/count.py data/test/corpus1/lemma.txt.gz test_matrix1 1

The usage of each script (including .sh scripts) can be understood by running it with help option `-h`, e.g.:

	python3 type-based/count.py -h

It is strongly recommend to run the scripts within a [virtual environment](https://pypi.org/project/virtualenv/) with Python 3.9.1. Install the required packages running `pip install -r requirements.txt`.


### Automatic LSC Discovery


#### Prepare Data

The minimum required data is the following:
1. lemmatized corpus pair (in .txt.gz format)
2. raw corpus pair (in .txt.gz format)

The following data is optional:
3. a file containing target words (one word per line)
4. binary and graded gold data (one word-value pair per line, tab seperated)

A shell script is provided to bring the data into the required format:

	bash scripts/prepare_data.sh <data_set_id> <path_corpus1_lemma> <path_corpus2_lemma> <path_corpus1_token> <path_corpus2_token> [path_targets] [path_binary_gold] [path_graded_gold]
	
e.g.

	bash scripts/prepare_data.sh test_data test/corpus1_lemma.txt.gz test/corpus2_lemma.txt.gz test/corpus1_token.txt.gz test/corpus2_token.txt.gz

It is recommeded to choose a unique and descriptive data set identifier <data_set_id>. All automated scripts utilize the data set identifier to obtain the required data. 

If you want to use the contextualized approach (BERT), word usages (sentences where the word occurs) from the intersection of the corpus vocabularies have to be extracted from the corpora. Due to the large computational effort, we recommend to take a sample of these words instead. We recommend a sample_size of 500, however, it can be freely extended, if desired. A script is provided that takes samples and extracts usages automatically:

	bash scripts/prepare_sample.sh <data_set_id> <sample_id> <sample_size> <max_usages> <language>
	
e.g.

	bash scripts/prepare_sample.sh test_data sample_1 500 25 en

The sample identifier <sample_id> should also be unique and descriptive. 


#### Static Approach

The following script can be used to automatically discover changing words in the intersection of the corpus vacubaliers:

	bash scripts/discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t> <language> [sample_id] [sample_size] [max_usages] [max_samples]

e.g.
	
	bash scripts/discover_sgns.sh test_data 10 50 5 0.001 3 3 5 1.0 en
	
When the script is exectued with values for the optional parameters [sample_id], [sample_size] and [max_usages], a usage-level filtering is applied at the end.

	bash scripts/discover_sgns.sh test_data 10 50 5 0.001 3 3 5 1.0 en sample_1 100 50
	

When the script is executed with values for the optional parameters [sample_id], [sample_size] and [max_usages] and [max_samples], the final set of discovered changing words is stored in a format so that they can directly be uploaded to the DURel annotation system.

e.g.

	bash scripts/discover_sgns.sh test_data 10 50 5 0.001 3 3 5 1.0 en sample_1 100 50 25
	
	
#### Contextualized Approach

The following script can be used to automatically discover changing words in a sample of the intersection of the corpus vocabularies:

	bash scripts/discover_bert.sh <data_set_id> <sample_id> <language> <type> <layers> <t> [f2] [max_samples]
	
e.g.

	bash scripts/discover_bert.sh test_data sample_1 en token 1+12 0.1

When the script is executed with values for the optional parameter [f2], a usage-level filtering is applied at the end.

e.g.

	bash scripts/discover_bert.sh test_data sample_1 en token 1+12 0.1 f2

When the script is executed with values for the optional parameter [f2] and [max_samples], the final set of discovered changing words is stored in a format so that they can directly be uploaded to the DURel annotation system.

e.g.

	bash scripts/discover_bert.sh test_data sample_1 en token 1+12 0.1 f2 25
	
	
### Automated Binary Classification and Graded Ranking

Scripts are provided to automatically solve the two SemEval-2020 subtasks Binary Classification and Graded Ranking.

### Prepare Data

The minimum required data is the following:
1. lemmatized corpus pair (in .txt.gz format)
2. raw corpus pair (in .txt.gz format)
3. a file containing target words (one word per line)

The following is required for evaluation and fine-tuning:
4. binary and graded gold data (one word-value pair per line, tab seperated)

The previously described prepare_data.sh is used, 

 e.g.
 
	bash scripts/prepare_data.sh test_data test/corpus1_lemma.txt.gz test/corpus2_lemma.txt.gz test/corpus1_token.txt.gz test/corpus2_token.txt.gz test/targets.txt [test/binary_gold.tsv] [test/graded_gold.tsv]
	
Again, BERT requieres a sample and usages. If you allready prepared data for the automatic LSC Discovery, you can use the same sample and usages. Otherwise, 

e.g.

	bash scripts/prepare_sample.sh test_data sample_1 500 25 en

Usages for the target words are also required. A script is provided:

	bash scripts/extract_target_usages.sh <data_set_id> <language> <max_usages>

e.g.

	bash scripts/extract_target_usages.sh test_data en 25


#### Static Approach

The following script can be used to generate binary scores for the target words:

	bash scripts/classify_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t>
	
e.g.

	bash scripts/classify_sgns.sh 10 50 5 0.001 3 3 5 1.0


The following script can be used to generate graded values for the target words:


	bash scripts/classify_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> 

e.g.

	bash scripts/classify_sgns.sh 10 50 5 0.001 3 3 5


#### Contextualized Approach

The following script can be used to generate binary scores for the target words:

	bash scripts/classify_sgns.sh <data_set_id> <sample_id> <language> <type> <layers> <t>
	
e.g.

	bash scripts/classify_sgns.sh test_data sample_1 en token 1+12 0.1


The following script can be used to generate graded values for the target words:


	bash scripts/classify_sgns.sh <data_set_id> <language> <type> <layers> 

e.g.

	bash scripts/classify_sgns.sh test_data en token 1+12 


### Models
