#!/bin/bash
name=$0
data_set_id=$1
window_size=$2
dim=$3
k=$4
s=$5
min_count1=$6
min_count2=$7
itera=$8
t=$9
language=${10}

sample_id=${11}
sample_size=${12}
max_usages=${13}

max_samples=${14}

function usage {
    echo "Given a corpus pair C1 and C2, decide for the intersection of their vocabularies which words lost or gained sense(s) between C1 and C2."
    echo ""
    echo "  Usage:" 
    echo "      discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count> <itera> <t> <language>" 
    echo "      discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count> <itera> <t> <language> <sample_id> <sample_size> max_usages>" 
    echo "      discover_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count> <itera> <t> <language> <sample_id> <sample_size> <max_usages> <max_samples>" 
    echo ""
    echo "      <data_set_id>       = data set param_id"
    echo "      <window_size>       = the linear distance of context words to consider in each direction"
    echo "      <dim>               = dimensionality of embeddings"
    echo "      <k>                 = number of negative samples parameter (equivalent to shifting parameter for PPMI)"
    echo "      <s>                 = threshold for subsampling"
    echo "      <min_count1>        = number of occurrences for a word to be included in the vocabulary (corpus1)"
    echo "      <min_count2>        = number of occurrences for a word to be included in the vocabulary (corpus2)"
    echo "      <itera>             = number of iterations"
    echo "      <t>                 = threshold = mean + t * standard deviation"
    echo "      <language>          = en | de"
    echo "      <sample_id>         = sample identifier"    
    echo "      <sample_size>       = Number of words to be sampled from filtered words (after filter1)"
    echo "      <max_usages>        = max. number of usages to be extracted from each corpus"
    echo "      <max_samples>       = max. number of samples stored for annotation"
    echo ""
}

if [ $# -ne 10 ] && [ $# -ne 13 ] && [ $# -ne 14 ]
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi


param_id=SGNS_win${window_size}_dim${dim}_k${k}_s${s}_mc${min_count1}_mc${min_count2}_i${itera}

outdir=output/${data_set_id}/${param_id}/discovery/t${t}
resdir=results/${data_set_id}/${param_id}/discovery/t${t}

mkdir -p ${outdir}
mkdir -p ${resdir}

# Generate static word embeddings with SGNS
python type-based/sgns.py data/${data_set_id}/corpus1/lemma.txt.gz ${outdir}/mat1 ${window_size} ${dim} ${k} ${s} ${min_count1} ${itera}
python type-based/sgns.py data/${data_set_id}/corpus2/lemma.txt.gz ${outdir}/mat2 ${window_size} ${dim} ${k} ${s} ${min_count2} ${itera}


# Length-normalize, meanc-center and align with OP
python modules/map_embeddings.py --normalize unit center --init_identical --orthogonal ${outdir}/mat1 ${outdir}/mat2 ${outdir}/mat1ca ${outdir}/mat2ca


# Measure CD for every word in the intersection of the vocabularies
python measures/cd.py ${outdir}/mat1ca ${outdir}/mat2ca ${resdir}/distances_intersection.tsv


# Create predictions
python measures/binary.py ${resdir}/distances_intersection.tsv ${resdir}/predictions.tsv " ${t} " 


# Apply filter1
python modules/filter1.py ${resdir}/predictions.tsv ${resdir}/predictions_f1.tsv ${language}


# Sample from <predictions_f1.tsv> 
if [ $# -eq 13 ] || [ $# -eq 14 ]
    then
        sample=${resdir}/predictions_f1.tsv
        
        mkdir -p ${outdir}/${sample_id}/usages_corpus1
        mkdir -p ${outdir}/${sample_id}/usages_corpus2
        mkdir -p ${resdir}/${sample_id}

        number_lines=$(wc -l ${resdir}/predictions_f1.tsv | awk '{print $1 }')
        if [ ${sample_size} -lt ${number_lines} ]
            then
                python modules/sample.py -s ${resdir}/predictions_f1.tsv ${resdir}/${sample_id}/sample.tsv " ${sample_size} "
                sample=${resdir}/${sample_id}/sample.tsv
        fi

        python modules/extract_usages.py data/${data_set_id}/corpus1/lemma.txt.gz data/${data_set_id}/corpus1/token.txt.gz ${sample} ${outdir}/${sample_id}/usages_corpus1/ ${language} " ${max_usages} "
        python modules/extract_usages.py data/${data_set_id}/corpus2/lemma.txt.gz data/${data_set_id}/corpus2/token.txt.gz ${sample} ${outdir}/${sample_id}/usages_corpus2/ ${language} " ${max_usages} "

        # Apply filter2
        number_lines=$(wc -l ${sample} | awk '{print $1 }')
        progress_counter=0
        cat ${sample} | while read line || [ -n "$line" ]
            do
                result=$(python modules/filter2.py ${outdir}/${sample_id}/usages_corpus1/${line}.tsv ${outdir}/${sample_id}/usages_corpus2/${line}.tsv ${language})
                if [ ${result} == 1 ]
                    then
                        printf "%s\n" "${line}" >> ${resdir}/${sample_id}/predictions_f2.tsv
                fi
                ((progress_counter=progress_counter+1))
                echo "PROGRESS: ${progress_counter}/${number_lines}"
            done
fi


# Store in DURel format
if [ $# -eq 14 ]
    then
        mkdir -p ${resdir}/${sample_id}/DURel
        number_lines=$(wc -l ${resdir}/${sample_id}/predictions_f2.tsv | awk '{print $1 }')
        progress_counter=0
        cat ${resdir}/${sample_id}/predictions_f2.tsv | while read line || [ -n "$line" ]
        do  
            python modules/make_format.py ${outdir}/${sample_id}/usages_corpus1/${line}.tsv ${outdir}/${sample_id}/usages_corpus2/${line}.tsv ${resdir}/${sample_id}/DURel/${line}.tsv ${language} " ${max_samples} "
            ((progress_counter=progress_counter+1))
            echo "PROGRESS: ${progress_counter}/${number_lines}"
        done
fi
