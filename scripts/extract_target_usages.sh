#!/bin/bash
name=$0
data_set_id=$1
language=$2
max_usages=$3


function usage {
	echo "Extract usages for target words and store in appropriate format."
    echo ""
    echo "  Usage:" 
    echo "      extract_target_usages.sh <data_set_id> <language> <max_usages>"
    echo ""
	echo "		<data_set_id>	= data set id"
	echo "		<language>		= en | de"
	echo "		<max_usages>	= max number of usages"
    echo ""
}

if [ $# -ne 3 ] 
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

data_dir=data/${data_set_id}

mkdir -p ${data_dir}/targets/usages_corpus1
mkdir -p ${data_dir}/targets/usages_corpus2

# Extract usages for words in <targets.tsv>
python modules/extract_usages.py ${data_dir}/corpus1/lemma.txt.gz ${data_dir}/corpus1/token.txt.gz ${data_dir}/targets/targets.tsv ${data_dir}/targets/usages_corpus1/ ${language} " ${max_usages} "
python modules/extract_usages.py ${data_dir}/corpus2/lemma.txt.gz ${data_dir}/corpus2/token.txt.gz ${data_dir}/targets/targets.tsv ${data_dir}/targets/usages_corpus2/ ${language} " ${max_usages} "
