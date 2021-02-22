#!/bin/bash
name=$0
data_set_id=$1
language=$2
type=$3
layers=$4

function usage {
    echo "Create token-based embeddings with BERT and compute average pairwise distance (APD) and cosine similarity (COS) for every target word as well as the Spearman correlation afterwards."
    echo ""
    echo "  Usage:"
    echo "      ${name} <language> <type> <identifier>"
    echo ""
    echo "      <language>      = eng | ger | swe | lat"
    echo "      <type>          = lemma | token | toklem"
    echo "      <identifier>    = give a good name!"
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
mkdir -p ${resdir}

# Create vectors with bert, compute APD and COS
cat data/${language}/targets.tsv | while read line || [ -n "$line" ]
do  
    echo "${line}"
    python token-based/bert.py -l data/${language}/uses/corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} ${type}
    python token-based/bert.py -l data/${language}/uses/corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} ${type}

    apd=$(python modules/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
    cos=$(python modules/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

    printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd.tsv
    printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos.tsv
done

# Compute Spearman 
spr_apd=$(python modules/spr.py data/${language}/truth/graded.tsv ${resdir}/apd.tsv 1 1)
spr_cos=$(python modules/spr.py data/${language}/truth/graded.tsv ${resdir}/cos.tsv 1 1)

printf "%s\t%s\n" "${apd}" "${spr_apd}" >> ${resdir}/spr_apd.tsv
printf "%s\t%s\n" "${cos}" "${spr_cos}" >> ${resdir}/spr_cos.tsv

# # Clean up directory 
# rm -r output/${language}/bert/ranking/${param_id}
