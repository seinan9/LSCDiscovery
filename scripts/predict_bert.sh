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

outdir=output/${language}/bert/prediction/${identifier}
resdir=results/${language}/bert/prediction/${identifier}

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

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos.tsv
    done

# Create predictions
python measures/binary.py ${residr}/apd.tsv data/${language}/targets.tsv ${resdir}/predictions_apd.tsv " ${deviation_factor} " -p 
python measures/binary.py ${residr}/cos.tsv data/${language}/targets.tsv ${resdir}/predictions_cos.tsv " ${deviation_factor} " -p 

# Filter predictions
bash scripts/filter_predictions.sh ${language} ${resdir}/predictions_apd.tsv ${resdir}/filtered_predictions_apd.tsv 
bash scripts/filter_predictions.sh ${language} ${resdir}/predictions_cos.tsv ${resdir}/filtered_predictions_cos.tsv 

# Clean up directory 
rm -r output/${language}/bert/prediction/${identifier}
