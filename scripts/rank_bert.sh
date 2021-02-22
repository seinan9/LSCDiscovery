#!/bin/bash
name=$0
data_set_id=$1
language=$2
type=$3
layers=$4


function usage {
    echo "Rank a set of target words according to their degree of LSC between C_1 and C_2."
    echo ""
    echo "  Usage:"
    echo "      rank_bert.sh <data_set_id> <language> <type> <layers>"
    echo ""
    echo "      <data_set_id>   = data set identifier"
    echo "      <language>      = eng | ger | swe | lat"
    echo "      <type>          = lemma | token | toklem"
    echo "      <layers>        = TODO"
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

param_id=BERT_layers${layers}_type${type}

outdir=output/${data_set_id}/${param_id}/ranking
resdir=results/${data_set_id}/${param_id}/ranking

mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}/APD
mkdir -p ${resdir}/COS


# Create vectors with bert, compute APD and COS
cat data/${language}/targets.tsv | while read line || [ -n "$line" ]
do  
    echo "${line}"
    python token-based/bert.py -l data/${language}/uses/corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} ${type} ${layers}
    python token-based/bert.py -l data/${language}/uses/corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} ${type} ${layers}

    apd=$(python modules/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
    cos=$(python modules/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

    printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/APD/distances_targets.tsv
    printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/COS/distances_targets.tsv
done
