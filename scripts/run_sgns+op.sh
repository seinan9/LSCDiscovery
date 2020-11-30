#!/bin/bash
name=$0
language=$1
window_size=$2
dim=$3
k=$4
t=$5
min_count1=$6
min_count2=$7
itera=$8

function usage {
    echo "Create type-based embeddings with SGNS. Measure the cosine distance (CD) for every word and compute the Spearman correlation."
    echo ""
    echo "  Usage1:" 
    echo "      ${name} <language> <window_size> <dim> <k> <t> <min_count> <itera>" 
    echo ""
    echo "      <language>      = eng | ger | swe | lat"
    echo "      <window_size>   = the linear distance of context words to consider in each direction"
    echo "      <dim>           = dimensionality of embeddings"
    echo "      <k>             = number of negative samples parameter (equivalent to shifting parameter for PPMI)"
    echo "      <t>             = threshold for subsampling"
    echo "      <min_count1>    = number of occurrences for a word to be included in the vocabulary (corpus1)"
    echo "      <min_count2>    = number of occurrences for a word to be included in the vocabulary (corpus2)"
    echo "      <itera>         = number of iterations"
    echo ""
    echo "  Usage2: ${name} <language>"
    echo ""
    echo "      <language>      = eng | ger | swe | lat"
    echo ""
    echo "  Note: Usage2 chooses the paramters according to the best personal performance so far."
    echo ""
}

if [ $# -ne 8 ] && [ $# -ne 1 ]
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

if [ $# -eq 2 ]
    then 
        if [ $1 == "eng" ]
            then 
                window_size=10
                dim=350
                k=5
                t=None
                min_count1=4
                min_count2=4
                itera=30
        elif [ $1 == "ger" ]
            then
                window_size=10
                dim=300
                k=1
                t=0.025
                min_count1=39
                min_count2=39
                itera=5
        elif [ $1 == "swe" ]
            then
                window_size=10
                dim=500
                k=5
                t=None
                min_count1=42
                min_count2=65
                itera=5
        elif [ $1 == "lat" ]
            then
                window_size=10
                dim=10
                k=5
                t=None
                min_count1=1
                min_count2=6
                itera=30
        fi
fi

identifier=w${window_size}-dim${dim}-k${k}-t${t}-mc${min_count1}-mc${min_count2}-i${itera}

outdir=output/${language}/sgns/${identifier}
resdir=results/$language/sgns/${identifier}

#generate matrices with sgns
mkdir -p ${outdir}

python3.8 type-based/sgns.py data/${language}/corpus1/lemma/*.txt.gz ${outdir}/mat1 ${window_size} ${dim} ${k} ${t} ${min_count1} ${itera}
python3.8 type-based/sgns.py data/${language}/corpus2/lemma/*.txt.gz ${outdir}/mat2 ${window_size} ${dim} ${k} ${t} ${min_count2} ${itera}

#length-normalize and mean-center
python3.8 modules/center.py -l ${outdir}/mat1 ${outdir}/mat1c
python3.8 modules/center.py -l ${outdir}/mat2 ${outdir}/mat2c

#align with OP
python3.8 modules/map_embeddings.py --normalize unit center --init_identical --orthogonal ${outdir}/mat1c ${outdir}/mat2c ${outdir}/mat1ca ${outdir}/mat2ca

#measure CD
mkdir -p ${resdir}
python3.8 modules/cd.py ${outdir}/mat1ca ${outdir}/mat2ca data/${language}/targets.txt ${resdir}/cd.txt

#evaluate with SPR
python3.8 modules/spr.py data/${language}/truth/graded.txt ${resdir}/cd.txt 1 1 >> ${resdir}/spr.txt

#clean directory
rm -r output/${language}/sgns/${identifier}
