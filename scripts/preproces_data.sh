#!/bin/bash
name=$0
language=$1

function usage {
    echo "Preprocess corpus (remove low-frequency words, etc.)."
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

if [ $1 == 'eng' ]
    then
        min_count1=4
        min_count2=4
elif [ $1 == 'ger' ]
    then 
        min_count1=39
        min_count2=39
elif [ $1 == 'swe' ]
    then  
        min_count1=42
        min_count2=65
elif [ $1 == 'lat' ]
    then
        min_count1=1
        min_count2=6
fi

mkdir -p data/${language}/corpus1_preprocessed/lemma
mkdir -p data/${language}/corpus1_preprocessed/token
mkdir -p data/${language}/corpus2_preprocessed/lemma
mkdir -p data/${language}/corpus2_preprocessed/token

python3.8 modules/preprocess.py data/${language}/corpus1/lemma/*txt.gz data/${language}/corpus1_preprocessed/lemma/preprocessed.txt.gz ${min_count1}
python3.8 modules/preprocess.py data/${language}/corpus1/token/*txt.gz data/${language}/corpus1_preprocessed/token/preprocessed.txt.gz ${min_count1}
python3.8 modules/preprocess.py data/${language}/corpus2/lemma/*txt.gz data/${language}/corpus2_preprocessed/lemma/preprocessed.txt.gz ${min_count2}
python3.8 modules/preprocess.py data/${language}/corpus2/token/*txt.gz data/${language}/corpus2_preprocessed/token/preprocessed.txt.gz ${min_count2}
