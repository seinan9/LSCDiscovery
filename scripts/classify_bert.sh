#!/bin/bash
name=$0
data_set_id=$1
sample_id=$2
language=$3
type=$4
layers=$5
t=$6


function usage {
    echo "For a set of target words, decide which words lost or gained sense(s) between C1 and C2." 
    echo ""
    echo "  Usage:" 
    echo "      classify_bert.sh <data_set_id> <sample_id> <language> <type> <layers> <t>"
    echo ""
    echo "      <data_set_id>   = data set identifsier"
    echo "      <sample_id>     = sample identifier"
    echo "      <language>      = en | de | sw"
    echo "      <type>          = lemma | token | toklem"
    echo "      <layers>        = which layers to extract embeddings from. All possible combinations including numbers from 1 to 12 seperated by a + (e.g., 1, 1+2, 1+3+12, etc.)"
    echo "      <t>             = threshold = mean + t * standard deviation"
    echo ""
}

if [ $# -ne 6 ] 
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

outdir=output/${data_set_id}/${param_id}/classification/${sample_id}/t${t}
resdir=results/${data_set_id}/${param_id}/classification/${sample_id}/t${t}

mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}/APD
mkdir -p ${resdir}/COS


# Generate contextualized word embeddings with BERT for words in <sample.tsv> 
cat data/${data_set_id}/samples/${sample_id}/sample.tsv | while read line || [ -n "$line" ]
    do  
        echo "${line}"
        python contextualized/bert.py -l data/${data_set_id}/samples/${sample_id}/usages_corpus1/${line}.tsv ${outdir}/vectors_corpus1/${line} ${language} ${type} ${layers}
        python contextualized/bert.py -l data/${data_set_id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${outdir}/vectors_corpus2/${line} ${language} ${type} ${layers}

        # Measure APD and COS for every word in <sample.tsv>
        apd=$(python measures/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
        cos=$(python measures/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/APD/distances_sample.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/COS/distances_sample.tsv
    done

# Generate contextualized word embeddings with BERT for words in <targets.tsv> 
cat data/${data_set_id}/targets.tsv | while read line || [ -n "$line" ]
    do  
        echo "${line}"
        python contextualized/bert.py -l data/${data_set_id}/samples/${sample_id}/usages_corpus1/${line}.tsv ${outdir}/vectors_corpus1/${line} ${language} ${type} ${layers}
        python contextualized/bert.py -l data/${data_set_id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${outdir}/vectors_corpus2/${line} ${language} ${type} ${layers}

        # Measure APD and COS for every word in <sample.tsv>
        apd=$(python measures/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
        cos=$(python measures/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/APD/distances_targets.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/COS/distances_targets.tsv
    done


# Create predictions
python measures/binary.py ${resdir}/APD/distances_sample.tsv ${resdir}/APD/distances_targets.tsv ${resdir}/APD/scores_targets.tsv " ${t} "
python measures/binary.py ${resdir}/COS/distances_sample.tsv ${resdir}/COS/distances_targets.tsv ${resdir}/COS/scores_targets.tsv " ${t} "
