#!/usr/bin/env bash
API_KEY="YOUR_KEY"
ORG_KEY="YOUR_KEY"
dataset="summeval"
for attr in flu_new rel coh con; do
  for mode in geval analyze_rate rate_explain geval_no_auto_cot; do
    echo "$attr"_"$mode"
    python3 gpt4_eval_"$dataset".py \
      --prompt prompts/"$dataset"/"$attr"_"$mode".txt \
      --save_fp results/"$dataset"/gpt3.5_"$attr"_"$mode".json \
      --summeval_fp data/"$dataset".json \
      --key $API_KEY \
      --org_key $ORG_KEY \
      --max_len 128 \
      --model gpt-3.5-turbo-0613
  done 
done
