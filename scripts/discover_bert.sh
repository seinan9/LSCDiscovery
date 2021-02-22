#!/bin/bash
name=$0
id=$1
sample_id=$2
language=$3
layers=$4
type=$5
t=$6

f2=${7}
max_samples=${8}

function usage {
    echo "Given a corpus pair C_1 and C_2, decide for the intersection of their vocabularies which words lost or gained sense(s) between C_1 and C_2."
    echo ""
    echo "  Usage:" 
    echo "      discover_bert.sh <id> <sample_id> <layers> <type> <t> <language>"
    echo ""
    echo "      <id>                = data set identifier"
    echo "      <sample_id>         = sample identifier"
    echo "      <layers>            = TODO"
    echo "      <type>              = lemma | token | toklem"
    echo "      <t>                 = threshold = mean + t * standard deviation"
    echo "      <langauge>          = en | de"
    echo ""
}

if [ $# -ne 6 ] && [ $# -ne 7 ] && [ $# -ne 8 ]
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

outdir=output/${id}/${param_id}/discovery/${sample_id}/t${t}
resdir=results/${id}/${param_id}/discovery/${sample_id}/t${t}

mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}/APD
mkdir -p ${resdir}/COS

# Generate contextualized word embeddings with BERT for words in <sample.tsv> 
cat data/${id}/samples/${sample_id}/sample.tsv | while read line || [ -n "$line" ]
    do  
        echo "${line}"
        python token-based/bert.py -l data/${id}/samples/${sample_id}/usages_corpus1/${line}.tsv ${outdir}/vectors_corpus1/${line} ${language} ${type} ${layers}
        python token-based/bert.py -l data/${id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${outdir}/vectors_corpus2/${line} ${language} ${type} ${layers}

        # Measure APD and COS for every word in <sample.tsv>
        apd=$(python measures/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
        cos=$(python measures/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/APD/distances_sample.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/COS/distances_sample.tsv
    done

# Create predictions
python measures/binary.py ${resdir}/APD/distances_sample.tsv ${resdir}/APD/predictions_f1.tsv " ${t} "

python measures/binary.py ${resdir}/COS/distances_sample.tsv ${resdir}/COS/predictions_f1.tsv " ${t} "


# Apply filter2
if [ $# -eq 7 ] || [ $# -eq 8 ]
    then
        cat ${resdir}/APD/predictions_f1.tsv | while read line || [ -n "$line" ]
            do
                result=$(python modules/filter2.py data/${id}/samples/${sample_id}/usages_corpus1/${line}.tsv data/${id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${language})
                if [ ${result} == 1 ]
                    then
                        printf "%s\n" "${line}" >> ${resdir}/APD/predictions_f2.tsv
                fi
            done
        cat ${resdir}/COS/predictions_f1.tsv | while read line || [ -n "$line" ]
            do
                result=$(python modules/filter2.py data/${id}/samples/${sample_id}/usages_corpus1/${line}.tsv data/${id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${language})
                if [ ${result} == 1 ]
                    then
                        printf "%s\n" "${line}" >> ${resdir}/COS/predictions_f2.tsv
                fi
            done
fi

# Store in DURel format
if [ $# -eq 8 ]
    then
        # APD
        mkdir -p ${resdir}/APD/DURel
        cat ${resdir}/APD/predictions_f2.tsv | while read line || [ -n "$line" ]
        do  
            python modules/make_format.py data/${id}/samples/${sample_id}/usages_corpus1/${line}.tsv data/${id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${resdir}/APD/DURel/${line}.tsv ${language} " ${max_samples} "
        done
        # COS
        mkdir -p ${resdir}/COS/DURel
        cat ${resdir}/COS/predictions_f2.tsv | while read line || [ -n "$line" ]
        do  
            python modules/make_format.py data/${id}/samples/${sample_id}/usages_corpus1/${line}.tsv data/${id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${resdir}/COS/DURel/${line}.tsv ${language} " ${max_samples} "
        done
fi


# # Clean directory
# rm -r output/${id}/${param_id}/discovery/${sample_id}/t${t}

