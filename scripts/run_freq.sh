#!/bin/bash
name=$0
language=$1
type=$2

function usage {
    echo "Compute frequency baseline."
    echo ""
    echo "  Usage1:" 
    echo "      ${name} <language> <window_size> <dim> <k> <t> <min_count> <itera>" 
    echo ""
    echo "      <language>      = eng | ger | swe | lat"
    echo "      <type>          = lemma | token"
    echo ""
}

if [ $# -ne 2 ] 
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

outdir=output/${language}/freq/${type}
resdir=results/${language}/freq/${type}

mkdir -p ${outdir}
mkdir -p ${resdir}

# Get frequencies
python3.8 measures/freqs.py -n -l data/${language}/corpus1_preprocessed/${type}/*.txt.gz ${outdir}/freqs1_nl.tsv
python3.8 measures/freqs.py -n -l data/${language}/corpus2_preprocessed/${type}/*.txt.gz ${outdir}/freqs2_nl.tsv

# Compute difference 
python3.8 measures/subtract.py ${outdir}/freqs1_nl.tsv ${outdir}/freqs2_nl.tsv ${resdir}/freq_diffs_nl.tsv

# Create binary scores and evaluate 
printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class_nl.tsv
for i in `LANG=en_US seq -3 0.5 3`
    do  
        python3.8 measures/binary.py ${resdir}/freq_diffs_nl.tsv data/${language}/targets.txt ${resdir}/binary_t${i}_nl.tsv " ${i} "
        score_nl=$(python evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}_nl.tsv)
        printf "%s\t%s\n" "${i}" "${score_nl}" >> ${resdir}/class_nl.tsv
    done

# Clean directory
rm -r output/${language}/freq/${type}
