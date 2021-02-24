#!/bin/bash

# Download English SemEval data 
wget https://www2.ims.uni-stuttgart.de/data/sem-eval-ulscd/semeval2020_ulscd_eng.zip
unzip semeval2020_ulscd_eng.zip
rm semeval2020_ulscd_eng.zip

# Move Corpora 
mkdir -p data/en_semeval/corpus1
mkdir -p data/en_semeval/corpus2

mv semeval2020_ulscd_eng/corpus1/lemma/*txt.gz data/en_semeval/corpus1/lemma.txt.gz
mv semeval2020_ulscd_eng/corpus2/lemma/*txt.gz data/en_semeval/corpus2/lemma.txt.gz

mv semeval2020_ulscd_eng/corpus1/token/*txt.gz data/en_semeval/corpus1/token.txt.gz
mv semeval2020_ulscd_eng/corpus2/token/*txt.gz data/en_semeval/corpus2/token.txt.gz

# Move targets
mkdir -p data/en_semeval/targets
mv semeval2020_ulscd_eng/targets.txt data/en_semeval/targets/targets.tsv

# Move gold data
mkdir -p data/en_semeval/truth
mv semeval2020_ulscd_eng/truth/binary.txt data/en_semeval/truth/binary.tsv
mv semeval2020_ulscd_eng/truth/graded.txt data/en_semeval/truth/graded.tsv

# Clean up 
rm -r semeval2020_ulscd_eng

