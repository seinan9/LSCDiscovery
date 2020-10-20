#!/bin/bash

#ger
wget https://www2.ims.uni-stuttgart.de/data/sem-eval-ulscd/semeval2020_ulscd_ger.zip
unzip semeval2020_ulscd_ger.zip
rm semeval2020_ulscd_ger.zip

mkdir -p data/ger
mv semeval2020_ulscd_ger/* data/ger/
rm -r semeval2020_ulscd_ger

#eng
wget https://www2.ims.uni-stuttgart.de/data/sem-eval-ulscd/semeval2020_ulscd_eng.zip
unzip semeval2020_ulscd_eng.zip
rm semeval2020_ulscd_eng.zip

mkdir -p data/eng
mv semeval2020_ulscd_eng/* data/eng/
rm -r semeval2020_ulscd_eng

#swe
wget https://zenodo.org/record/3730550/files/semeval2020_ulscd_swe.zip?download=1
mv semeval2020_ulscd_swe.zip?download=1 ./semeval2020_ulscd_swe.zip
unzip semeval2020_ulscd_swe.zip
rm semeval2020_ulscd_swe.zip

mkdir -p data/swe
mv semeval2020_ulscd_swe/* data/swe/
rm -r semeval2020_ulscd_swe

#lat
wget https://zenodo.org/record/3992738/files/semeval2020_ulscd_lat.zip?download=1
mv semeval2020_ulscd_lat.zip?download=1 ./semeval2020_ulscd_lat.zip
unzip semeval2020_ulscd_lat.zip
rm semeval2020_ulscd_lat.zip

mkdir -p data/lat
mv semeval2020_ulscd_lat/* data/lat/
rm -r semeval2020_ulscd_lat
