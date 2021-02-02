#!/bin/bash
name=$0
language=$1
type=$2
identifier=$3

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

outdir=output/${language}/bert/${identifier}
resdir=results/${language}/bert/${identifier}

# Compute vectors with bert, compute APD and COS
mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}

cat data/${language}/targets.txt | while read line || [ -n "$line" ]
do  
    echo "${line}"
    python token-based/bert.py -l uses/${language}/corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} ${type}
    python token-based/bert.py -l uses/${language}/corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} ${type}

    apd=$(python modules/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
    cos=$(python modules/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

    printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd.txt
    printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos.txt

done

# Compute Spearman 
python modules/spr.py data/${language}/truth/graded.txt ${resdir}/apd.txt 1 1 >> ${resdir}/spr_apd.txt
python modules/spr.py data/${language}/truth/graded.txt ${resdir}/cos.txt 1 1 >> ${resdir}/spr_cos.txt

# Clean up directory 
rm -r output/${language}/bert/${identifier}
