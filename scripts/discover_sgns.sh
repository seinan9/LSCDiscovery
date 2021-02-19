#!/bin/bash
name=$0
id=$1
window_size=$2
dim=$3
k=$4
s=$5
min_count1=$6
min_count2=$7
itera=$8
t=$9
language=${10}

function usage {
    echo "Given a corpus pair C_1 and C_2, decide for the intersection of their vocabularies which words lost or gained sense(s) between C_1 and C_2."
    echo ""
    echo "  Usage:" 
    echo "      discover_sgns.sh <id> <window_size> <dim> <k> <s> <min_count> <itera> <t> <language>" 
    echo ""
    echo "      <id>                = data set identifier"
    echo "      <window_size>       = the linear distance of context words to consider in each direction"
    echo "      <dim>               = dimensionality of embeddings"
    echo "      <k>                 = number of negative samples parameter (equivalent to shifting parameter for PPMI)"
    echo "      <s>                 = threshold for subsampling"
    echo "      <min_count1>        = number of occurrences for a word to be included in the vocabulary (corpus1)"
    echo "      <min_count2>        = number of occurrences for a word to be included in the vocabulary (corpus2)"
    echo "      <itera>             = number of iterations"
    echo "      <t>                 = threshold = mean + t * standard deviation"
    echo "      <langauge>          = language for filtering"
    echo ""
    echo "  Options:"
    echo "      -s, --save      Use this flag (at the last position) to save the output matrices."
    echo ""
}

if [ $# -ne 10 ] && [ $# -ne 11 ]
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi


identifier=win${window_size}-dim${dim}-k${k}-s${s}-mc${min_count1}-mc${min_count2}-i${itera}-t${t}

outdir=output/${id}/discovery/${identifier}
resdir=results/${id}/discovery/${identifier}

mkdir -p ${outdir}
mkdir -p ${resdir}

# Generate word embeddins with SGNS
python type-based/sgns.py data/${id}/corpus1/*.txt.gz ${outdir}/mat1 ${window_size} ${dim} ${k} ${s} ${min_count1} ${itera}
python type-based/sgns.py data/${id}/corpus2/*.txt.gz ${outdir}/mat2 ${window_size} ${dim} ${k} ${s} ${min_count2} ${itera}

# Length-normalize, meanc-center and align with OP
python modules/map_embeddings.py --normalize unit center --init_identical --orthogonal ${outdir}/mat1 ${outdir}/mat2 ${outdir}/mat1ca ${outdir}/mat2ca

# Measure CD for every word in the intersection of the vocabularies
python measures/cd.py ${outdir}/mat1ca ${outdir}/mat2ca ${resdir}/cd_intersection.tsv

# Create predictions
python measures/binary.py ${resdir}/cd_intersection.tsv ${resdir}/predictions.tsv " ${deviation_factor} " 

# Filter1: remove words that are not a NOUN, VERB or ADJ
cat ${resdir}/predictions.tsv | while read line || [ -n "$line" ]
    do
        result=$(python modules/filter1.py ${line} ${language})
        if [ ${result} == 1 ]
            then
                printf "%s\n" "${line}" >> ${resdir}/predictions_f1.tsv
        fi
    done

# Clean directory
if [ $# -eq 10 ]
    then 
        rm -r output/${id}/discovery/${identifier}
fi