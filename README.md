# LSCDiscovery
Scripts for large-scale prediction of lexical semantic change.

First do:
```
bash get_data.sh
bash scripts/preprocess_data.sh ger
bash scripts/make_samples.sh ger
```

Pipeline to generate SGNS+OP+CD predictions with a threshold of t=1.0:
```
bash scripts/predict_sgns.sh ger 10 300 5 0.001 39 39 5 1.0
```

Pipeline to generate BERT+APD and BERT+COS (toklem, layer 12+1) predictions with a threshold of t=0.1:
```
bash scripts/clean_uses.sh ger
bash scripts/predict_bert.sh ger toklem toklem 0.1
```
