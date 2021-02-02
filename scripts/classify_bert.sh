#!/bin/bash
name=$0
language=$1
type=$2
identifier=$3
deviation_factor=$4

function usage {
    echo "Create token-based BERT embeddings for 500 samples + target words. Compute binary classification for SemEval Subtask 1 and Spearman correlation for Subtask 2." 
    echo ""
    echo "  Usage:" 
    echo "      ${name} <language>"
    echo ""
    echo "      <language>          = eng | ger | swe | lat"
    echo "      <type>              = lemma | token | toklem"
    echo "      <identifier>        = give a good name!"
    echo "      <deviation_factor>  = threshold = mean + deviation_factor * std"
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

outdir=output/${language}/bert/classification/${identifier}
resdir=results/${language}/bert/classification/${identifier}

mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}

# Compute vectors with bert for target words, compute APD and COS
cat data/${language}/samples/samples.tsv | while read line || [ -n "$line" ]
    do  
        echo "${line}"
        python token-based/bert.py -l data/${language}/uses/corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} ${type}
        python token-based/bert.py -l data/${language}/uses/corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} ${type}

        apd=$(python measures/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
        cos=$(python measures/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd_samples.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos_samples.tsv
    done

# Classify targets
python measures/binary.py ${resdir}/apd_samples.tsv data/${language}/targets.tsv ${resdir}/binary_apd.tsv " ${deviation_factor} " 
python measures/binary.py ${resdir}/cos_samples.tsv data/${language}/targets.tsv ${resdir}/binary_cos.tsv " ${deviation_factor} "  

# Evaluate classification
score_apd=$(python evaluation/class_metrics.py data/${language}/truth/binary.tsv ${resdir}/binary_apd.tsv)
score_cos=$(python evaluation/class_metrics.py data/${language}/truth/binary.tsv ${resdir}/binary_cos.tsv)

printf "%s\n" "${score_apd}" >> ${resdir}/class_apd.tsv
printf "%s\n" "${score_cos}" >> ${resdir}/class_cos.tsv

# Clean up directory 
rm -r output/${language}/bert/classification/${identifier}
