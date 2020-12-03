#!/bin/bash
name=$0
language=$1
identifier=$2

function usage {
    echo "Compute frequency baseline."
    echo ""
    echo "  Usage1:" 
    echo "      ${name} <language> <window_size> <dim> <k> <t> <min_count> <itera>" 
    echo ""
    echo "      <language>      = eng | ger | swe | lat"
    echo "      <identifier>    = blalba"
    echo ""

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

outdir=output/${language}/freq/${identifier}
resdir=results/$language/freq/${identifier}

mkdir -p ${outdir}
mkdir -p ${resdir}

python3.8 modules/get_freqs.py data/${language}/corpus1_preprocessed/${identifier}/*.txt.gz ${outdir}/freqs1.csv
python3.8 modules/get_freqs.py data/${language}/corpus2_preprocessed/${identifier}/*.txt.gz ${outdir}/freqs2.csv

python3.8 modules/subtract_freqs.py ${outdir}/freqs1.csv ${outdir}/freqs2.csv ${resdir}/freq_diffs.csv

printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class.csv
for i in `LANG=en_US seq -3 0.5 3`
    do  
        python3.8 modules/get_binary.py ${resdir}/freq_diffs.csv data/${language}/targets.txt ${resdir}/binary_t${i}.csv " ${i} "
        score=$(python modules/classification_measure.py data/${language}/truth/binary.txt ${resdir}/binary_t${i}.csv)
        printf "%s\t%s\n" "${i}" "${score}" >> ${resdir}/class.csv
    done

# clean directory
rm -r output/${language}/freq/${identifier}
