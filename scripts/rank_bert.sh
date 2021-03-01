#!/bin/bash
name=$0
data_set_id=$1
language=$2
type=$3
layers=$4


function usage {
    echo "Rank a set of target words according to their degree of LSC between C1 and C2."
    echo ""
    echo "  Usage:"
    echo "      rank_bert.sh <data_set_id> <language> <type> <layers>"
    echo ""
    echo "      <data_set_id>   = data set identifier"
    echo "      <language>      = en | de | sw | la"
    echo "      <type>          = lemma | token | toklem"
    echo "      <layers>        = which layers to extract embeddings from. All possible combinations including numbers from 1 to 12 seperated by a + (e.g., 1, 1+2, 1+3+12, etc.)"
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
cat data/${data_set_id}//targets/targets.tsv | while read line || [ -n "$line" ]
do  
    echo "${line}"
    python token-based/bert.py -l data/${data_set_id}/targets/usages_corpus1/${line}.tsv ${outdir}/vectors_corpus1/${line} ${language} ${type} ${layers}
    python token-based/bert.py -l data/${data_set_id}/targets/usages_corpus2/${line}.tsv ${outdir}/vectors_corpus2/${line} ${language} ${type} ${layers}

    apd=$(python measures/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
    cos=$(python measures/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

    printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/APD/distances_targets.tsv
    printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/COS/distances_targets.tsv
done
