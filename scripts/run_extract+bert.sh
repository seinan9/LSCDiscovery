#!/bin/bash
name=$0
language=$1
identifier=$2

function usage {
    echo ""
    echo "  Usage: ${name} <language>"
    echo ""
    echo "      <language>      = eng | ger | swe | lat"
    echo "      <identifier>    = give a good name!"
    echo ""
}

if [ $# -ne 2 ] 
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

# Generate uses 
mkdir -p ${outdir}/uses_corpus1
mkdir -p ${outdir}/uses_corpus2

python modules/extract_uses.py data/${language}/corpus1/lemma/*.txt.gz data/${language}/corpus1/token/*.txt.gz data/${language}/targets.txt ${outdir}/uses_corpus1/ ${language}
python modules/extract_uses.py data/${language}/corpus2/lemma/*.txt.gz data/${language}/corpus2/token/*.txt.gz data/${language}/targets.txt ${outdir}/uses_corpus2/ ${language}

# Compute vectors with bert, compute APD and COS
mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}

cat data/${language}/targets.txt | while read line || [ -n "$line" ]
do  
    echo "${line}"
    python token-based/bert.py ${outdir}/uses_corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} token
    python token-based/bert.py ${outdir}/uses_corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} token

    apd=$(python modules/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
    cos=$(python modules/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

    printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd.txt
    printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos.txt

done

#Compute Spearman 
python modules/spr.py data/${language}/truth/graded.txt ${resdir}/apd.txt 1 1 >> ${resdir}/spr_apd.txt
python modules/spr.py data/${language}/truth/graded.txt ${resdir}/cos.txt 1 1 >> ${resdir}/spr_cos.txt

# Clean up directory 
rm -r output/${language}/bertfull/${identifier}
