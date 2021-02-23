#!/bin/bash
name=$0
data_set_id=$1
param_id=$2
sample_id=$2
language=$5
sample_size=$6
max_usages=$7

function usage {
    echo "Extract usages for words in <path_predictions> and apply filter 2."
    echo ""
    echo "  Usage:" 
    echo "      apply_filter2.sh <id> <sample_id> <path_predictions> <path_output> <language>" 
    echo "      apply_filter2.sh <id> <sample_id> <path_predictions> <path_output> <language>" 

    echo ""
    echo "      <id>                = data set id"
    echo "      <path_predictions>  = File containing predictions"
    echo "      <path_output>       = Name and path of output file"
    echo "      <language>          = en | de | it | ru"
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

if [ $# -eq 7 ]
    then
        python modules/sample.py -s ${predictions} data/${id}/samples/${sample_id}/sample.tsv " ${sample_size} " 
        python modules/extract_usages.py data/${id}/corpus1/lemma/*.txt.gz data/${id}/corpus1/token/*.txt.gz data/${id}/samples/${sample_id}/sample.tsv data/${id}/samples/${sample_id}/usages_corpus1/ ${language} " ${max_usages} "
fi

if no sampling needed:
    then
        cat results/${id}/discovery/${param_id}/predictions_f1.tsv | while read line || [ -n "$line" ]
            do
                result=$(python modules/filter2.py data/${id}/samples/${sample_id}/usages_corpus1/${line}.tsv data/${id}/${sample_id}/usages_corpus2/${line}.tsv ${language})
                if [ ${result} == 1 ]
                    then
                        printf "%s\n" "${line}" >> ${output}
                fi
            done
fi


results/${id}/discovery/${param_id}/pred_f1.tsv
results/${id}/discovery/${param_id}/${sampling_id}/pred_f1.tsv


sample ornder in data set id 
usages auch dort 

lade aus results die pred_f1 file 
apply f2 
speichere in data_id/discovery/param_id/sample_id