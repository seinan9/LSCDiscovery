#!/bin/bash

# Download German SemEval data 
wget https://www2.ims.uni-stuttgart.de/data/sem-eval-ulscd/semeval2020_ulscd_ger.zip
unzip semeval2020_ulscd_ger.zip
rm semeval2020_ulscd_ger.zip

# Move Corpora 
mkdir -p data/de_semeval/corpus1
mkdir -p data/de_semeval/corpus2

mv semeval2020_ulscd_ger/corpus1/lemma/*txt.gz data/de_semeval/corpus1/lemma.txt.gz
mv semeval2020_ulscd_ger/corpus2/lemma/*txt.gz data/de_semeval/corpus2/lemma.txt.gz

mv semeval2020_ulscd_ger/corpus1/token/*txt.gz data/de_semeval/corpus1/token.txt.gz
mv semeval2020_ulscd_ger/corpus2/token/*txt.gz data/de_semeval/corpus2/token.txt.gz

# Move targets
mkdir -p data/de_semeval/targets
mv semeval2020_ulscd_ger/targets.txt data/de_semeval/targets/targets.tsv

# Move gold data
mkdir -p data/de_semeval/truth
mv semeval2020_ulscd_ger/truth/binary.txt data/de_semeval/truth/binary.tsv
mv semeval2020_ulscd_ger/truth/graded.txt data/de_semeval/truth/graded.tsv

# Clean up 
rm -r semeval2020_ulscd_ger
