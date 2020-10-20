#!/bin/bash
language=$1
outdir=output/bert/$language
resdir=results/bert/$language


# Generate uses 
mkdir -p ${outdir}/uses_corpus1
mkdir -p ${outdir}/uses_corpus2

python modules/extract_uses.py data/${language}/corpus1/lemma/*.txt.gz data/${language}/corpus1/token/*.txt.gz data/${language}/targets.txt ${outdir}/uses_corpus1/ ${language}
python modules/extract_uses.py data/${language}/corpus2/lemma/*.txt.gz data/${language}/corpus2/token/*.txt.gz data/${language}/targets.txt ${outdir}/uses_corpus2/ ${language}


# Compute vectors with bert, compute APD and COS
mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}

cat data/${language}/targets.txt | while read line 
do  
    echo "${line}"
    python token-based/bert.py ${outdir}/uses_corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language}
    python token-based/bert.py ${outdir}/uses_corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language}

    apd=$(python modules/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
    cos=$(python modules/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

    printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd.txt
    printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos.txt

done


#Compute Spearman 
python modules/spr.py data/${language}/truth/graded.txt ${resdir}/apd.txt graded apd 1 1 >> ${resdir}/spr_apd.txt
python modules/spr.py data/${language}/truth/graded.txt ${resdir}/cos.txt graded cos 1 1 >> ${resdir}/spr_cos.txt


# Clean up directory 
rm -r output/bert/${language}
