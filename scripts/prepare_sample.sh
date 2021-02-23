#!/bin/bash
name=$0
data_set_id=$1
sample_id=$2
sample_size=$3
usage_size=$4
language=$5

function usage {
	echo "Generate a sample of size <sample_size> and extract <usage_size> usages for every word from C_1 and C_2."
    echo ""
    echo "  Usage:" 
    echo "      make_samples.sh <data_set_id> <sample_id> <sample_size> <usage_size> <language>"
    echo ""
	echo "		<data_set_id>	= data set id"
	echo "		<sample_id>	= identifier for the sample"
	echo "		<sample_size>	= size of the sample"
	echo "		<usage_size>	= max number of usages"
	echo "		<language>	= en | de"
    echo ""
}

if [ $# -ne 5 ] 
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

sample_dir=data/${data_set_id}/samples/${sample_id}

mkdir -p ${sample_dir}
mkdir -p ${sample_dir}/usages_corpus1/
mkdir -p ${sample_dir}/usages_corpus2/
mkdir -p data/${data_set_id}/tmp

# Generate frequency list of intersection
python measures/freqs.py data/${data_set_id}/corpus1/lemma.txt.gz data/${data_set_id}/corpus2/lemma.txt.gz data/${data_set_id}/tmp/freqs_inter.tsv

# Apply Filter1
python modules/filter1.py data/${data_set_id}/tmp/freqs_inter.tsv data/${data_set_id}/tmp/freqs_inter_f1.tsv en -t

# Generate sample
python modules/sample.py data/${data_set_id}/tmp/freqs_inter_f1.tsv ${sample_dir}/sample.tsv " ${sample_size} " 

# Extract usages for sample
python modules/extract_usages.py data/${data_set_id}/corpus1/lemma.txt.gz data/${data_set_id}/corpus1/token.txt.gz ${sample_dir}/sample.tsv ${sample_dir}/usages_corpus1/ ${language} " ${usage_size} "
python modules/extract_usages.py data/${data_set_id}/corpus2/lemma.txt.gz data/${data_set_id}/corpus2/token.txt.gz ${sample_dir}/sample.tsv ${sample_dir}/usages_corpus2/ ${language} " ${usage_size} "

# Clean
rm -rf data/${data_set_id}/tmp