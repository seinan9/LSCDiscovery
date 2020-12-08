#!/bin/bash
name=$0
language=$1
type=$2
identifier=$3

function usage {
    echo "Create token-based BERT embeddings with fulluses extracted from SemEval data and compute average pairwise distance (APD), cosine similarity (COS) and Spearman correlation afterwards."
    echo ""
    echo "  Usage:" 
    echo "      ${name} <language>"
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

outdir=output/${language}/bertfull/${identifier}
resdir=results/${language}/bertfull/${identifier}

# Compute vectors with bert, compute APD and COS
mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}

cat data/${language}/targets.txt | while read line || [ -n "$line" ]
do  
    echo "${line}"
    python3.8 token-based/bert.py -l fulluses/${language}/corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} ${type}
    python3.8 token-based/bert.py -l fulluses/${language}/corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} ${type}

    apd=$(python3.8 modules/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
    cos=$(python3.8 modules/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

    printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd.txt
    printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos.txt

done

# Compute Spearman 
python3.8 modules/spr.py data/${language}/truth/graded.txt ${resdir}/apd.txt 1 1 >> ${resdir}/spr_apd.txt
python3.8 modules/spr.py data/${language}/truth/graded.txt ${resdir}/cos.txt 1 1 >> ${resdir}/spr_cos.txt

# Clean up directory 
rm -r output/${language}/bertfull/${identifier}
