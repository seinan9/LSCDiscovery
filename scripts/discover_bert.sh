#!/bin/bash
name=$0
data_set_id=$1
sample_id=$2
language=$3
type=$4
layers=$5
t=$6

f2=${7}

max_samples=${8}


function usage {
    echo "Given a corpus pair C1 and C2, decide for the intersection of their vocabularies which words lost or gained sense(s) between C_1 and C_2."
    echo ""
    echo "  Usage:" 
    echo "      discover_bert.sh <data_set_id> <sample_id> <language> <type> <layers> <t>"
    echo "      discover_bert.sh <data_set_id> <sample_id> <language> <type> <layers> <t> <f2>" 
    echo "      discover_bert.sh <data_set_id> <sample_id> <language> <type> <layers> <t> <f2> <max_samples>" 
    echo ""
    echo "      <data_set_id>       = data set identifier"
    echo "      <sample_id>         = sample identifier"
    echo "      <language>          = en | de"
    echo "      <type>              = lemma | token | toklem"
    echo "      <layers>            = which layers to extract embeddings from. All possible combinations including numbers from 1 to 12 seperated by a + (e.g., 1, 1+2, 1+3+12, etc.)"
    echo "      <t>                 = threshold = mean + t * standard deviation"
    echo "      <f2>                = if you want to apply the second filter write f2"
    echo "      <max_samples>       = max. number of samples stored for annotation"
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

outdir=output/${data_set_id}/${param_id}/discovery/${sample_id}/t${t}
resdir=results/${data_set_id}/${param_id}/discovery/${sample_id}/t${t}

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


# Create predictions
python measures/binary.py ${resdir}/APD/distances_sample.tsv ${resdir}/APD/predictions_f1.tsv " ${t} "

python measures/binary.py ${resdir}/COS/distances_sample.tsv ${resdir}/COS/predictions_f1.tsv " ${t} "


# Apply filter2
if [ $# -eq 7 ] || [ $# -eq 8 ]
    then
        cat ${resdir}/APD/predictions_f1.tsv | while read line || [ -n "$line" ]
            do
                result=$(python modules/filter2.py data/${data_set_id}/samples/${sample_id}/usages_corpus1/${line}.tsv data/${data_set_id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${language})
                if [ ${result} == 1 ]
                    then
                        printf "%s\n" "${line}" >> ${resdir}/APD/predictions_f2.tsv
                fi
            done
        cat ${resdir}/COS/predictions_f1.tsv | while read line || [ -n "$line" ]
            do
                result=$(python modules/filter2.py data/${data_set_id}/samples/${sample_id}/usages_corpus1/${line}.tsv data/${data_set_id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${language})
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
            python modules/make_format.py data/${data_set_id}/samples/${sample_id}/usages_corpus1/${line}.tsv data/${data_set_id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${resdir}/APD/DURel/${line}.tsv ${language} " ${max_samples} "
        done
        # COS
        mkdir -p ${resdir}/COS/DURel
        cat ${resdir}/COS/predictions_f2.tsv | while read line || [ -n "$line" ]
        do  
            python modules/make_format.py data/${data_set_id}/samples/${sample_id}/usages_corpus1/${line}.tsv data/${data_set_id}/samples/${sample_id}/usages_corpus2/${line}.tsv ${resdir}/COS/DURel/${line}.tsv ${language} " ${max_samples} "
        done
fi
