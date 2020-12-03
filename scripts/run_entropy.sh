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

outdir=output/${language}/entropy/${type}
resdir=results/${language}/entropy/${type}

mkdir -p ${outdir}
mkdir -p ${resdir}

# Create counte-based matrix
python3.8 type-based/count.py data/${language}/corpus1_preprocessed/${type}/*.txt.gz ${outdir}/mat1 ${window_size}
python3.8 type-based/count.py data/${language}/corpus2_preprocessed/${type}/*.txt.gz ${outdir}/mat2 ${window_size}

# Get entropy scores
python3.8 measures/entropy.py -n ${outdir}/mat1 ${outdir}/entropy1_n.tsv
python3.8 measures/entropy.py -n ${outdir}/mat2 ${outdir}/entropy2_n.tsv

python3.8 measures/entropy.py -n -l ${outdir}/mat1 ${outdir}/entropy1_nl.tsv
python3.8 measures/entropy.py -n -l ${outdir}/mat2 ${outdir}/entropy2_nl.tsv

# Compute difference 
python3.8 measures/subtract.py ${outdir}/entropy1_n.tsv ${outdir}/entropy2_n.tsv ${resdir}/entropy_diffs_n.tsv
python3.8 measures/subtract.py ${outdir}/entropy1_nl.tsv ${outdir}/entropy2_nl.tsv ${resdir}/entropy_diffs_nl.tsv

# Create binary scores and evaluate 
printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class_n.tsv
printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class_nl.tsv
for i in `LANG=en_US seq -3 0.5 3`
    do  
        python3.8 measures/binary.py ${resdir}/entropy_diffs_n.tsv data/${language}/targets.txt ${resdir}/binary_t${i}_n.tsv " ${i} "
        python3.8 measures/binary.py ${resdir}/entropy_diffs_nl.tsv data/${language}/targets.txt ${resdir}/binary_t${i}_nl.tsv " ${i} "
        score_n=$(python evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}_n.tsv)
        score_nl=$(python evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}_nl.tsv)
        printf "%s\t%s\n" "${i}" "${score_n}" >> ${resdir}/class_n.tsv
        printf "%s\t%s\n" "${i}" "${score_nl}" >> ${resdir}/class_nl.tsv
    done

# Clean directory
rm -r output/${language}/entropy/${type}
