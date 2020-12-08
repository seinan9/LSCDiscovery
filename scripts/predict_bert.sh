#!/bin/bash
name=$0
language=$1
type=$2
identifier=$3

function usage {
    echo "Create token-based BERT embeddings with fulluses extracted from SemEval data and compute average pairwise distance (APD), cosine similarity (COS) and Spearman correlation afterwards."
    echo ""
    echo "  Usage:" 
    echo "      ${name} <language>"
    echo ""
    echo "      <language>      = eng | ger | swe | lat"
    echo "      <type>          = lemma | token | toklem"
    echo "      <identifier>    = give a good name!"
    echo ""
}

if [ $# -ne 3 ] 
	then 
		usage
		exit 1
fi

if [[ ( $1 == "--help") ||  $1 == "-h" ]] 
	then 
		usage
		exit 0
fi

outdir=output/${language}/bert_predict/${identifier}
resdir=results/${language}/bert_predict/${identifier}

mkdir -p ${outdir}/vectors_corpus1
mkdir -p ${outdir}/vectors_corpus2
mkdir -p ${resdir}

# Compute vectors with bert for target words, compute APD and COS
cat data/${language}/targets.txt | while read line || [ -n "$line" ]
    do  
        echo "${line}"
        python token-based/bert.py -l fulluses/${language}/corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} ${type}
        python token-based/bert.py -l fulluses/${language}/corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} ${type}

        apd=$(python measures/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
        cos=$(python measures/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos.tsv

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd_samples.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos_samples.tsv
    done

# Compute Spearman 
python evaluation/spr.py data/${language}/truth/graded.tsv ${resdir}/apd.tsv 1 1 >> ${resdir}/spr_apd.tsv
python evaluation/spr.py data/${language}/truth/graded.tsv ${resdir}/cos.tsv 1 1 >> ${resdir}/spr_cos.tsv


# # Compute vectors with bert for samples, compute APD and COS
# for i in 1 2 3 4 5
#     do
#         cat data/${language}/samples/samples_area${i}.tsv | while read line || [ -n "$line" ]
#         do  
#             echo "${line}"
#             python token-based/bert.py -l fulluses/${language}/corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} ${type}
#             python token-based/bert.py -l fulluses/${language}/corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} ${type}

#             apd=$(python modules/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
#             cos=$(python modules/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

#             printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd_samples_area${i}.tsv
#             printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos_samples_area${i}.tsv

#             printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd_samples_full.tsv
#             printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos_samples_full.tsv
#         done
#     done

# Create binary scores for separate areas
# for i in 1 2 3 4 5 
#     do 
#         printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class_area${i}_apd.tsv
#         printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class_area${i}_cos.tsv

#         for j in `LANG=en_US seq -2 1 2`
#             do  
#                 python3.8 measures/binary.py ${resdir}/apd_samples_area${i}.tsv data/${language}/targets.txt ${resdir}/binary_t${j}_area${i}_apd.tsv " ${j} "
#                 python3.8 measures/binary.py ${resdir}/cos_samples_area${i}.tsv data/${language}/targets.txt ${resdir}/binary_t${j}_area${i}_cos.tsv " ${j} "

#                 class_apd=$(python evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${j}_area${i}_apd.tsv)
#                 class_cos=$(python evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${j}_area${i}_cos.tsv)

#                 printf "%s\t%s\n" "${j}" "${class_apd}" >> ${resdir}/class_area${i}_apd.tsv
#                 printf "%s\t%s\n" "${j}" "${class_cos}" >> ${resdir}/class_area${i}_cos.tsv
#             done
#     done

# Compute vectors with bert for target words, compute APD and COS
cat data/${language}/samples/samples_full.tsv | while read line || [ -n "$line" ]
    do  
        echo "${line}"
        python token-based/bert.py -l fulluses/${language}/corpus1/${line}.csv ${outdir}/vectors_corpus1/${line} ${language} ${type}
        python token-based/bert.py -l fulluses/${language}/corpus2/${line}.csv ${outdir}/vectors_corpus2/${line} ${language} ${type}

        apd=$(python measures/apd.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})
        cos=$(python measures/cos.py ${outdir}/vectors_corpus1/${line} ${outdir}/vectors_corpus2/${line})

        printf "%s\t%s\n" "${line}" "${apd}" >> ${resdir}/apd_samples.tsv
        printf "%s\t%s\n" "${line}" "${cos}" >> ${resdir}/cos_samples.tsv
    done

# Create binary scores for full samples 
printf "%s\t%s\t%s\t%s\t%s\t%s\n" "factor" "precision" "recall" "bal_acc" "f1" "f0.5" >> ${resdir}/class_apd.tsv
for j in `LANG=en_US seq -2 1 2`
    do  
        python measures/binary.py ${resdir}/apd_samples.tsv data/${language}/targets.txt ${resdir}/binary_t${j}_apd.tsv " ${j} "
        python measures/binary.py ${resdir}/cos_samples.tsv data/${language}/targets.txt ${resdir}/binary_t${j}_cos.tsv " ${j} "

        score_apd=$(python evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${j}_apd.tsv)
        score_cos=$(python evaluation/class_metrics.py data/${language}/truth/binary.txt ${resdir}/binary_t${j}_cos.tsv)

        printf "%s\t%s\n" "${j}" "${class_apd}" >> ${resdir}/class_apd.tsv
        printf "%s\t%s\n" "${j}" "${class_cos}" >> ${resdir}/class_cos.tsv
    done

# Clean up directory 
rm -r output/${language}/bertfull/${identifier}
