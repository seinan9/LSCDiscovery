# LSCDiscovery
Scripts for large-scale prediction of lexical semantic change.

First do:
```
bash scripts/prepare_data.sh corpus1_token corpus2_token corpus1_lemma corpus2_lemma [targets] [binary_gold] [graded_gold]
```
For SGNS
```
bash scripts/discover_sgns.sh data_set_id window_size dim k s min_count1 min_count2 itera t language
(O) bash scripts/f2.sh (optional parameter to extract usages if needed) 
(O) bash scripts/make_format.sh (optional parameter to extract usages if needed)
```
For BERT
```
bash scripts/make_sample.sh id sample_id sample_size usage_size language
bash scripts/discover_bert.sh id sample_id layers type t language
(O) bash scripts/f2.sh 
(O) bash scripts/make_format.sh
```

- implement fortschritt in bash scripts (current_line/number_of_lines)
