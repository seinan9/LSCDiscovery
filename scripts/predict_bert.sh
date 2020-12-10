#!/bin/bash
name=$0
language=$1
type=$2
identifier=$3

function usage {
    echo "Create token-based BERT embeddings for 500 samples + target words. Compute binary classification for SemEval Subtask 1 and Spearman correlation for Subtask 2." 
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

outdir=output/${language}/predict_bert/${identifier}
resdir=results/${language}/predict_bert/${identifier}

mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}

# Compute vectors with bert for target words, compute APD and COS
cat data/${language}/samples/samples.tsv | while read line || [ -n "$line" ]
    do  
        echo "${line}"
        python3.8 token-based/bert.py -l sample_uses/${language}/corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} ${type}
        python3.8 token-based/bert.py -l sample_uses/${language}/corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} ${type}

        apd=$(python3.8 measures/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
        cos=$(python3.8 measures/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd_samples.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos_samples.tsv
    done

cat data/${language}/target.txt | while read line || [ -n "$line" ]
    do
        echo "${line}"
        apd=$(python3.8 measures/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
        cos=$(python3.8 measures/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos.tsv 

# Compute Spearman 
python3.8 evaluation/spr.py data/${language}/truth/graded.tsv ${resdir}/apd.tsv 1 1 >> ${resdir}/spr_apd.tsv
python3.8 evaluation/spr.py data/${language}/truth/graded.tsv ${resdir}/cos.tsv 1 1 >> ${resdir}/spr_cos.tsv

# Create binary scores using full samples
printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class_apd.tsv
for j in `LANG=en_US seq 0.5 0.5 2`
    do  
        python3.8 measures/binary.py ${resdir}/apd_samples.tsv data/${language}/targets.txt ${resdir}/binary_t${j}_apd.tsv " ${j} "
        python3.8 measures/binary.py ${resdir}/cos_samples.tsv data/${language}/targets.txt ${resdir}/binary_t${j}_cos.tsv " ${j} "

        score_apd=$(python3.8 evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${j}_apd.tsv)
        score_cos=$(python3.8 evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${j}_cos.tsv)

        printf "%s\t%s\n" "${j}" "${class_apd}" >> ${resdir}/class_apd.tsv
        printf "%s\t%s\n" "${j}" "${class_cos}" >> ${resdir}/class_cos.tsv

        python3.8 measures/binary.py -a ${resdir}/apd_samples.tsv data/${language}/targets.txt ${resdir}/binary_t${j}_apd-a.tsv " ${j} " data/${language}/samples/areas.tsv 
        python3.8 measures/binary.py -a ${resdir}/cos_samples.tsv data/${language}/targets.txt ${resdir}/binary_t${j}_cos-a.tsv " ${j} " data/${language}/samples/areas.tsv 

        score_apd_a=$(python3.8 evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${j}_apd-a.tsv)
        score_cos_a=$(python3.8 evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${j}_cos-a.tsv)

        printf "%s\t%s\n" "${j}" "${class_apd-a}" >> ${resdir}/class_apd-a.tsv
        printf "%s\t%s\n" "${j}" "${class_cos-a}" >> ${resdir}/class_cos-a.tsv
    done

# Clean up directory 
rm -r output/${language}/predict_bert/${identifier}
