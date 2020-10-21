#!/bin/bash
language=$1
outdir=output/sgns/$language
resdir=results/sgns/$language

#generate matrices with sgns
mkdir -p ${outdir}
python type-based/sgns.py data/${language}/corpus1/lemma/*.txt.gz ${outdir}/mat1 5 25 1 1 1 1
python type-based/sgns.py data/${language}/corpus2/lemma/*.txt.gz ${outdir}/mat2 5 25 1 1 1 1

#length-normalize and mean-center
python modules/center.py -l ${outdir}/mat1 ${outdir}/mat1c
python modules/center.py -l ${outdir}/mat2 ${outdir}/mat2c

#align with OP
python modules/map_embeddings.py --normalize unit center --init_identical --orthogonal ${outdir}/mat1c ${outdir}/mat2c ${outdir}/mat1ca ${outdir}/mat2ca

#measure CD
mkdir -p ${resdir}
python modules/cd.py -f -d ${outdir}/mat1ca ${outdir}/mat2ca data/${language}/targets.txt ${resdir}/cd.txt

#evaluate with SPR
python modules/spr.py data/${language}/truth/graded.txt ${resdir}/cd.txt 1 1 >> ${resdir}/spr.txt

#clean directory
rm -r output/sgns/${language}
