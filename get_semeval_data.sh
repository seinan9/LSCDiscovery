#!/bin/bash

# #ger
# wget https://www2.ims.uni-stuttgart.de/data/sem-eval-ulscd/semeval2020_ulscd_ger.zip
# unzip semeval2020_ulscd_ger.zip
# rm semeval2020_ulscd_ger.zip

# mkdir -p semeval/ger
# mv semeval2020_ulscd_ger/* semeval/ger/
# rm -r semeval2020_ulscd_ger

#eng
wget https://www2.ims.uni-stuttgart.de/data/sem-eval-ulscd/semeval2020_ulscd_eng.zip
unzip semeval2020_ulscd_eng.zip
rm semeval2020_ulscd_eng.zip

mkdir -p semeval/eng
mv semeval2020_ulscd_eng/* semeval/eng/
rm -r semeval2020_ulscd_eng

# #swe
# wget https://zenodo.org/record/3730550/files/semeval2020_ulscd_swe.zip?download=1
# mv semeval2020_ulscd_swe.zip?download=1 ./semeval2020_ulscd_swe.zip
# unzip semeval2020_ulscd_swe.zip
# rm semeval2020_ulscd_swe.zip

# mkdir -p data/swe
# mv semeval2020_ulscd_swe/* data/swe/
# mv data/swe/targets.txt data/swe/targets.tsv
# mv data/swe/truth/binary.txt data/swe/truth/binary.tsv
# mv data/swe/truth/graded.txt data/swe/truth/graded.tsv
# rm -r semeval2020_ulscd_swe

# #lat
# wget https://zenodo.org/record/3992738/files/semeval2020_ulscd_lat.zip?download=1
# mv semeval2020_ulscd_lat.zip?download=1 ./semeval2020_ulscd_lat.zip
# unzip semeval2020_ulscd_lat.zip
# rm semeval2020_ulscd_lat.zip

# mkdir -p data/lat
# mv semeval2020_ulscd_lat/* data/lat/
# mv data/lat/targets.txt data/lat/targets.tsv
# mv data/lat/truth/binary.txt data/lat/truth/binary.tsv
# mv data/lat/truth/graded.txt data/lat/truth/graded.tsv
# rm -r semeval2020_ulscd_lat
