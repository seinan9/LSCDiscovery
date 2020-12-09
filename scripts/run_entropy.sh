#!/bin/bash
name=$0
language=$1
type=$2
window_size=$3

function usage {
    echo "Compute entropy baseline."
    echo ""
    echo "  Usage:" 
    echo "      ${name} <language> <type> <window_size>"
    echo ""
    echo "      <language>      = eng | ger | swe | lat"
    echo "      <type>          = lemma | token"
    echo "      <window_size>   = window size"
    echo ""
    echo "  Short usage:"
    echo "      ${name} <language> <type>"
    echo ""
    echo "      Window_size is set to 10"
    echo ""
}
if [ $# -ne 2 ] && [ $# -ne 3 ]
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
        window_size=10
fi

outdir=output/${language}/entropy_predict/${type}
resdir=results/${language}/entropy_predict/${type}

mkdir -p ${outdir}
mkdir -p ${resdir}

# Create counte-based matrix
python3.8 type-based/count.py data/${language}/corpus1_preprocessed/${type}/*.txt.gz ${outdir}/mat1 ${window_size}
python3.8 type-based/count.py data/${language}/corpus2_preprocessed/${type}/*.txt.gz ${outdir}/mat2 ${window_size}

# Get entropy scores
python3.8 measures/entropy.py -n ${outdir}/mat1 ${outdir}/entropy1-n.tsv
python3.8 measures/entropy.py -n ${outdir}/mat2 ${outdir}/entropy2-n.tsv

python3.8 measures/entropy.py -n -l ${outdir}/mat1 ${outdir}/entropy1-nl.tsv
python3.8 measures/entropy.py -n -l ${outdir}/mat2 ${outdir}/entropy2-nl.tsv

# Compute difference 
python3.8 measures/subtract.py ${outdir}/entropy1-n.tsv ${outdir}/entropy2-n.tsv data/${language}/samples/samples.tsv ${resdir}/entropy_diffs-n.tsv
python3.8 measures/subtract.py ${outdir}/entropy1-nl.tsv ${outdir}/entropy2-nl.tsv data/${language}/samples/samples.tsv ${resdir}/entropy_diffs-nl.tsv

# Create binary scores and evaluate 
printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class-n.tsv
printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class-nl.tsv
for i in `LANG=en_US seq 0.5 0.5 2`
    do  
        python3.8 measures/binary.py ${resdir}/entropy_diffs-n.tsv data/${language}/targets.txt ${resdir}/binary_t${i}-n.tsv " ${i} "
        python3.8 measures/binary.py ${resdir}/entropy_diffs-nl.tsv data/${language}/targets.txt ${resdir}/binary_t${i}-nl.tsv " ${i} "
        score-n=$(python3.8 evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}-n.tsv)
        score-nl=$(python3.8 evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}-nl.tsv)
        printf "%s\t%s\n" "${i}" "${score-n}" >> ${resdir}/class-n.tsv
        printf "%s\t%s\n" "${i}" "${score-nl}" >> ${resdir}/class-nl.tsv

        python3.8 measures/binary.py -a ${resdir}/entropy_diffs-n.tsv data/${language}/targets.txt ${resdir}/binary_t${i}-n-a.tsv " ${i} " data/${language}/samples/areas.tsv 
        python3.8 measures/binary.py -a ${resdir}/entropy_diffs-nl.tsv data/${language}/targets.txt ${resdir}/binary_t${i}-nl-a.tsv " ${i} " data/${language}/samples/areas.tsv 
        score-n-a=$(python3.8 evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}-n-a.tsv)
        score-nl-a=$(python3.8 evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}-nl-a.tsv)
        printf "%s\t%s\n" "${i}" "${score-n-a}" >> ${resdir}/class-n-a.tsv
        printf "%s\t%s\n" "${i}" "${score-nl-a}" >> ${resdir}/class-nl-a.tsv
    done

# Clean directory
rm -r output/${language}/entropy/${type}
