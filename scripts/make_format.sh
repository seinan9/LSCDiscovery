#!/bin/bash
name=$0
id=$1
predictions=$2
language=$3
max_samples=$4

function usage {
    echo "Save usages in an appropriate format for the DURel system."
    echo ""
    echo "  Usage:" 
    echo "      make_format.sh <id> <path_predictions> <language> <max_samples>"
    echo ""
    echo "      <id>                = data set id"
    echo "      <path_predictions>  = file containing the predictions"
    echo "      <language>          = en | de | it | ru"
    echo "      <max_samples>       = maximal number of samples"
    echo ""
}

if [ $# -ne 4 ] 
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

mkdir -p data/${id}/DURel

cat ${predictions} | while read line || [ -n "$line" ]
do  
    python modules/make_format.py data/${id}/usages/corpus1/${line}.tsv data/${id}/usages/corpus2/${line}.tsv data/${id}/DURel/ ${language} " ${max_samples} "
done
