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

outdir=output/${language}/predict_freq/${type}
resdir=results/${language}/predict_freq/${type}

mkdir -p ${outdir}
mkdir -p ${resdir}

# Get frequencies
python measures/freqs.py -n -l data/${language}/corpus1_preprocessed/${type}/*.txt.gz ${outdir}/freqs1-nl.tsv
python measures/freqs.py -n -l data/${language}/corpus2_preprocessed/${type}/*.txt.gz ${outdir}/freqs2-nl.tsv

# Compute difference 
python measures/subtract.py ${outdir}/freqs1-nl.tsv ${outdir}/freqs2-nl.tsv data/${language}/samples/samples.tsv ${resdir}/freq_diffs-nl.tsv

# Create binary scores and evaluate 
for i in `LANG=en_US seq 0 0.5 2`
    do  
        python measures/binary.py ${resdir}/freq_diffs-nl.tsv data/${language}/targets.txt ${resdir}/binary_t${i}-nl.tsv " ${i} "
        score_nl=$(python evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}-nl.tsv)
        printf "%s\t%s\n" "${i}" "${score_nl}" >> ${resdir}/class-nl.tsv

        python measures/binary.py -a ${resdir}/freq_diffs-nl.tsv data/${language}/targets.txt ${resdir}/binary_t${i}-nl-a.tsv " ${i} " data/${language}/samples/areas.tsv 
        score_nl_a=$(python evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}-nl-a.tsv)
        printf "%s\t%s\n" "${i}" "${score_nl_a}" >> ${resdir}/class-nl-a.tsv
    done

# Clean directory
rm -r output/${language}/predict_freq/${type}
