#!/bin/bash
name=$0
id=$1
predictions=$2
output=$3
language=$4
max_usages=$5

function usage {
    echo "Extract usages for words in <path_predictions> and apply filter 2."
    echo ""
    echo "  Usage:" 
    echo "      apply_filter2.sh <id> <path_predictions> <path_output> <language> <max_usages>" 
    echo ""
    echo "      <id>                = data set id"
    echo "      <path_predictions>  = File containing predictions"
    echo "      <path_output>       = Name and path of output file"
    echo "      <language>          = en | de | it | ru"
    echo "      <max_usages>        = maximal number of usages to extract"
    echo ""
}

if [ $# -ne 5 ] 
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

mkdir -p data/${id}/usages/corpus1
mkdir -p data/${id}/usages/corpus2

python modules/extract_usages.py data/${id}/corpus1/lemma/*.txt.gz data/${id}/corpus1/token/*.txt.gz ${predictions} data/${id}/usages/corpus1/ ${language} " ${5} "
python modules/extract_usages.py data/${id}/corpus2/lemma/*.txt.gz data/${id}/corpus2/token/*.txt.gz ${predictions} data/${id}/usages/corpus2/ ${language} " ${5} "

cat ${predictions} | while read line || [ -n "$line" ]
    do
        result=$(python modules/filter2.py data/${id}/usages/corpus1/${line}.tsv data/${id}/usages/corpus2/${line}.tsv ${language})
        if [ ${result} == 1 ]
            then
                printf "%s\n" "${line}" >> ${output}
        fi
    done
