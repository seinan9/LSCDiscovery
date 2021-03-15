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

function usage {
    echo "For a set of target words, decide which words lost or gained sense(s) between C1 and C2."
    echo ""
    echo "  Usage:" 
    echo "      classify_sgns.sh <data_set_id> <window_size> <dim> <k> <s> <min_count1> <min_count2> <itera> <t>" 
    echo ""
    echo "      <data_set_id>       = data set identifier"
    echo "      <window_size>       = the linear distance of context words to consider in each direction"
    echo "      <dim>               = dimensionality of embeddings"
    echo "      <k>                 = number of negative samples parameter (equivalent to shifting parameter for PPMI)"
    echo "      <s>                 = threshold for subsampling"
    echo "      <min_count1>        = number of occurrences for a word to be included in the vocabulary (corpus1)"
    echo "      <min_count2>        = number of occurrences for a word to be included in the vocabulary (corpus2)"
    echo "      <itera>             = number of iterations"
    echo "      <t>                 = threshold = mean + t * standard deviation"
    echo ""
}

if [ $# -ne 9 ]
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

outdir=output/${data_set_id}/${param_id}/classification/t${t}
resdir=results/${data_set_id}/${param_id}/classification/t${t}

mkdir -p ${outdir}
mkdir -p ${resdir}


# Generate word embeddins with SGNS
python static/sgns.py data/${data_set_id}/corpus1/lemma.txt.gz ${outdir}/mat1 ${window_size} ${dim} ${k} ${s} ${min_count1} ${itera}
python static/sgns.py data/${data_set_id}/corpus2/lemma.txt.gz ${outdir}/mat2 ${window_size} ${dim} ${k} ${s} ${min_count2} ${itera}


# Length-normalize, meanc-center and align with OP
python modules/map_embeddings.py --normalize unit center --init_identical --orthogonal ${outdir}/mat1 ${outdir}/mat2 ${outdir}/mat1ca ${outdir}/mat2ca


# Measure CD for every word in the intersection
python measures/cd.py ${outdir}/mat1ca ${outdir}/mat2ca ${resdir}/distances_intersection.tsv


# Measure CD for every target word
python measures/cd.py ${outdir}/mat1ca ${outdir}/mat2ca data/${data_set_id}/targets/targets.tsv ${resdir}/distances_targets.tsv


# Compute binary scores for targets
python measures/binary.py ${resdir}/distances_intersection.tsv ${resdir}/distances_targets.tsv ${resdir}/scores_targets.tsv " ${t} "
