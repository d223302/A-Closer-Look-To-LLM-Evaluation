
for attr in coh flu flu_new rel con; do
  mv "$attr"_analyze.txt "$attr"_analyze_rate.txt
  mv "$attr"_analyze_w_cot.txt "$attr"_analyze_rate_auto_cot.txt
  mv "$attr"_detailed_no_cot.txt "$attr"_geval_no_auto_cot.txt
  mv "$attr"_detailed.txt "$attr"_geval.txt
  mv "$attr"_explain.txt "$attr"_rate_explain_auto_cot.txt
  mv "$attr"_explain_no_cot.txt "$attr"_rate_explain.txt
  rm *explain_first*
  mv "$attr"_llm_eval.txt "$attr"_free_text_no_auto_cot.txt
done
