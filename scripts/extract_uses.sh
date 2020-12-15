#!/bin/bash
name=$0
language=$1

function usage {
	echo "Extract uses from given corpus and save in appropriate format."
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


# Generate uses 
mkdir -p data/${language}/uses/corpus1
mkdir -p data/${language}/uses/corpus2

python3.8 modules/extract_uses.py data/${language}/corpus1/lemma/*.txt.gz data/${language}/corpus1/token/*.txt.gz data/${language}/targets.tsv data/${language}/uses/corpus1/ ${language}
python3.8 modules/extract_uses.py data/${language}/corpus2/lemma/*.txt.gz data/${language}/corpus2/token/*.txt.gz data/${language}/targets.tsv data/${language}/uses/corpus2/ ${language}


