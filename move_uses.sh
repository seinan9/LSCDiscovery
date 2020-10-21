#!/bin/bash

mkdir -p data/eng/corpus1/uses
mkdir -p data/eng/corpus2/uses

mv uses/eng/corpus1/* data/eng/corpus1/uses/
mv uses/eng/corpus1/* data/eng/corpus2/uses/

mkdir -p data/ger/corpus1/uses
mkdir -p data/ger/corpus2/uses

mv uses/ger/corpus1/* data/ger/corpus1/uses/
mv uses/ger/corpus1/* data/ger/corpus2/uses/

mkdir -p data/swe/corpus1/uses
mkdir -p data/swe/corpus2/uses

mv uses/swe/corpus1/* data/swe/corpus1/uses/
mv uses/swe/corpus1/* data/swe/corpus2/uses/