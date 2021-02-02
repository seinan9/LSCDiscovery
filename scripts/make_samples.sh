#!/bin/bash
name=$0
language=$1

function usage {
	echo "Generate samples and extract 100 uses from both time periods for every sample."
    echo ""
    echo "  Usage:" 
    echo "      ${name} <language>"
    echo ""
    echo "      <language>  = eng | ger | swe"
    echo ""
}

if [ $# -ne 1 ] 
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi


mkdir -p data/${language}/samples
mkdir -p data/${language}/uses/corpus1
mkdir -p data/${language}/uses/corpus2

# Generate frequency lists
python measures/freqs.py data/${language}/corpus1_preprocessed/lemma/*txt.gz data/${language}/samples/freqs1.tsv
python measures/freqs.py data/${language}/corpus2_preprocessed/lemma/*txt.gz data/${language}/samples/freqs2.tsv

# Generate samples
python modules/sample.py data/${language}/samples/freqs1.tsv data/${language}/samples/freqs2.tsv data/${language}/targets.tsv data/${language}/samples/

# Extract uses for samples
python modules/extract_uses.py data/${language}/corpus1/lemma/*.txt.gz data/${language}/corpus1/token/*.txt.gz data/${language}/samples/samples.tsv data/${language}/uses/corpus1/ ${language}
python modules/extract_uses.py data/${language}/corpus2/lemma/*.txt.gz data/${language}/corpus2/token/*.txt.gz data/${language}/samples/samples.tsv data/${language}/uses/corpus2/ ${language}


