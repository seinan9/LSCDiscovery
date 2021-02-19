#!/bin/bash
name=$0
id=$1
corpus1=$2
corpus2=$3
targets=$4
binary_gold=$5
graded_gold=$6

function usage {
    echo "Bring the data in the appropriate format."
    echo ""
    echo "  Usage:"
    echo "      prepare_data.sh <id> <path_corpus1> <path_corpus2>" 
    echo "      prepare_data.sh <id> <path_corpus1> <path_corpus2> <path_targets>" 
    echo "      prepare_data.sh <id> <path_corpus1> <path_corpus2> <path_targets> <path_binary_gold> <path_graded_gold>" 
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

if [ $# -ne 3 ] && [ $# -ne 4 ] && [ $# -ne 6 ]
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

mkdir -p data/${id}/corpus1
mkdir -p data/${id}/corpus2

cp ${corpus1} data/${id}/corpus1/
cp ${corpus2} data/${id}/corpus2/

if [ $# -eq 4 ]
    then 
        cp ${targets} data/${id}/targets.txt 
fi

if [ $# -eq 6 ]
    then 
    mkdir -p data/${id}/truth
        cp ${binary_gold} data/${id}/truth/binary_gold.tsv
        cp ${graded_gold} data/${id}/truth/graded_gold.tsv
fi