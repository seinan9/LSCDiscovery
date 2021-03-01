#!/bin/bash
name=$0
data_set_id=$1
corpus1_lemma=$2
corpus2_lemma=$3
corpus1_token=$4
corpus2_token=$5

targets=$6

binary_gold=$7
graded_gold=$8


function usage {
    echo "Bring data in appropriate format."
    echo ""
    echo "  Usage:"
    echo "      prepare_data.sh <data_set_id> <path_corpus1> <path_corpus2>"
    echo "      prepare_data.sh <data_set_id> <path_corpus1_lemma> <path_corpus2_lemma> <path_corpus1_token> <path_corpus2_token> " 
    echo "      prepare_data.sh <data_set_id> <path_corpus1_lemma> <path_corpus2_lemma> <path_corpus1_token> <path_corpus2_token> <path_targets>" 
    echo "      prepare_data.sh <data_set_id> <path_corpus1_lemma> <path_corpus2_lemma> <path_corpus1_token> <path_corpus2_token> <path_targets> <path_binary_gold> <path_graded_gold>" 
    echo ""
    echo "      <data_set_id>           = data set identifier"
    echo "      <path_corpus1_lemma>    = Path to first lemmatized corpus."
    echo "      <path_corpus2_lemma>    = Path to second lemmatized corpus."
    echo "      <path_corpus1_token>    = Path to first raw corpus."
    echo "      <path_corpus2_token>    = Path to second raw corpus."
    echo "      <path_targets>          = Path to target words (optional)."
    echo "      <path_binary_gold>      = Path to binary gold data (optional)."
    echo "      <path_graded_gold>      = Path to graded gold data (optional)."
    echo ""
    echo "  Note:"
    echo "      Select the first, if you only have access to two corpora pairs."
    echo "      Select the second usage, if you have access to two corpora and a set of target words (e.g., to solve SemEval-2020 subtasks)."
    echo "      Select the thrid usage, if you have access to two corpora, a set of target words as well as binary and graded gold data (for evaluation)."
    echo ""
    echo "      The corpora have to be in .txt.gz format."
    echo "      Targets have to be in .txt format. One target word per line."
    echo "      Gold data has to be in .txt, .csv or .tsv format. One target word and the according value (tab-seperated) per line."
    echo "" 
}

if [ $# -ne 3 ] && [ $# -ne 5 ] && [ $# -ne 6 ] && [ $# -ne 8 ]
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi


mkdir -p data/${data_set_id}/corpus1
mkdir -p data/${data_set_id}/corpus2

# If used if a single corpus pair
if [ $# -eq 3 ]
    then
        cp ${corpus1_lemma} data/${data_set_id}/corpus1/lemma.txt.gz
        cp ${corpus2_lemma} data/${data_set_id}/corpus2/lemma.txt.gz

        cp ${corpus1_lemma} data/${data_set_id}/corpus1/token.txt.gz
        cp ${corpus2_lemma} data/${data_set_id}/corpus2/token.txt.gz
fi        

# Store lemma copora and token corpora
if [ $# -eq 6 ] || [ $# -eq 8 ]
    then
        cp ${corpus1_lemma} data/${data_set_id}/corpus1/lemma.txt.gz
        cp ${corpus2_lemma} data/${data_set_id}/corpus2/lemma.txt.gz

        cp ${corpus1_token} data/${data_set_id}/corpus1/token.txt.gz
        cp ${corpus2_token} data/${data_set_id}/corpus2/token.txt.gz
fi

# Store target words
if [ $# -eq 6 ] || [ $# -eq 8 ]
    then 
        mkdir -p data/${data_set_id}/targets
        cp ${targets} data/${data_set_id}/targets/targets.tsv 
fi

# Store gold data
if [ $# -eq 8 ]
    then 
        mkdir -p data/${data_set_id}/truth
        cp ${binary_gold} data/${data_set_id}/truth/binary.tsv
        cp ${graded_gold} data/${data_set_id}/truth/graded.tsv
fi