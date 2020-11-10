name=$0
language=$1

function usage {
    echo ""
    echo "  Usage: ${name} <language>"
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

mkdir -p cleanuses/${language}/corpus1
mkdir -p cleanuses/${language}/corpus2

cat data/${language}/targets.txt | while read line || [ -n "$line" ]
do  
    echo "${line}"
    python modules/clean_uses.py uses/${language}/corpus1/${line}.csv cleanuses/${language}/corpus1/${line} ${language} 
    python modules/clean_uses.py uses/${language}/corpus2/${line}.csv cleanuses/${language}/corpus2/${line} ${language} 

done
