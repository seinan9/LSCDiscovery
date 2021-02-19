#!/bin/bash
name=$0
id=$1
corpus1_token=$2
corpus2_token=$3
corpus1_lemma=$4
corpus2_lemma=$5
targets=$6
binary_gold=$7
graded_gold=$8

function usage {
    echo "Bring data in appropriate format."
    echo ""
    echo "  Usage:"
    echo "      prepare_data.sh <id> <path_corpus1_token> <path_corpus2_token> <path_corpus1_lemma> <path_corpus2_lemma> " 
    echo "      prepare_data.sh <id> <path_corpus1_token> <path_corpus2_token> <path_corpus1_lemma> <path_corpus2_lemma> <path_targets>" 
    echo "      prepare_data.sh <id> <path_corpus1_token> <path_corpus2_token> <path_corpus1_lemma> <path_corpus2_lemma> <path_targets> <path_binary_gold> <path_graded_gold>" 
    echo ""
    echo "      <id>                = Identifier for data set. Give a good name!"
    echo "      <path_corpus1>      = Path to first corpus."
    echo "      <path_corpus2>      = Path to second corpus."
    echo "      <path_targets>      = Path to target words (optional)."
    echo "      <path_binary_gold>  = Path to binary gold data (optional)."
    echo "      <path_graded_gold>  = Path to graded gold data (optional)."
    echo ""
    echo "  Note:"
    echo "      Select the first, if you only have access to two corpora."
    echo "      Select the second usage, if you have access to two corpora and a set of target words (e.g., to solve SemEval-2020 subtasks)."
    echo "      Select the thrid usage, if you have access to two corpora, a set of target words as well as binary and graded gold data (for evaluation)."
    echo ""
    echo "      The corpora have to be in .txt.gz format."
    echo "      Targets have to be in .txt format. One target word per line."
    echo "      Gold data has to be in .txt, .csv or .tsv format. One target word and the according value (tab-seperated) per line."
    echo "" 
}

if [ $# -ne 5 ] && [ $# -ne 6 ] && [ $# -ne 8 ]
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

mkdir -p data/${id}/corpus1/token
mkdir -p data/${id}/corpus1/lemma

mkdir -p data/${id}/corpus2/token
mkdir -p data/${id}/corpus2/lemma

cp ${corpus1_token} data/${id}/corpus1/token/
cp ${corpus2_token} data/${id}/corpus2/token/

cp ${corpus1_lemma} data/${id}/corpus1/lemma/
cp ${corpus2_lemma} data/${id}/corpus2/lemma/

if [ $# -eq 6 ]
    then 
        cp ${targets} data/${id}/targets.txt 
fi

if [ $# -eq 8 ]
    then 
        cp ${targets} data/${id}/targets.txt
        mkdir -p data/${id}/truth
        cp ${binary_gold} data/${id}/truth/binary_gold.tsv
        cp ${graded_gold} data/${id}/truth/graded_gold.tsv
fi