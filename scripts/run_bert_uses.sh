#!/bin/bash
name=$0
language=$1

function usage {
    echo ""
    echo "  Usage: ${name} <language>"
    echo ""
    echo "      <language>   = eng | ger | swe | lat"
    echo ""
}

if [ $# -ne 1 ] 
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

outdir=output/bert/$language
resdir=results/bert/$language

# Compute vectors with bert, compute APD and COS
mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}

for entry in ${dir}/*
do
    line=${entry##*/}
    echo "${line}"

    python token-based/bert.py data/${language}/corpus1/uses/${line}.csv ${outdir}/vectors_corpus1/${line} ${language}
    python token-based/bert.py data/${language}/corpus2/uses/${line}.csv ${outdir}/vectors_corpus2/${line} ${language}

    apd=$(python modules/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
    cos=$(python modules/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

    printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd.txt
    printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos.txt

done

#Compute Spearman 
python modules/spr.py data/${language}/truth/graded.txt ${resdir}/apd.txt 1 1 >> ${resdir}/spr_apd.txt
python modules/spr.py data/${language}/truth/graded.txt ${resdir}/cos.txt 1 1 >> ${resdir}/spr_cos.txt

# Clean up directory 
rm -r output/bert/${language}
