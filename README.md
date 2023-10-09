#  Codes for Paper "A Closer Look into Automatic Evaluation Using Large Language Models"

- This repo contains the dataset and codes we used in our EMNLP2023 findings paper, A Closer Look into Automatic Evaluation Using Large Language Models.
- Our codes are mostly based on the official implementation of [G-Eval](https://github.com/nlpyang/geval).

## Preparation
We use a venv for all our experiments, and the packages in this enviroment are listed in `requirements.txt`.
Maybe some packages are not required for reproducing our results.

## Datasets and Prompts
The datasets and prompts are already in the `datasets` and `prompts` folders
Note that the files starting with `flu_new` in `prompts/summeval` are the prompts we construct.
The SummEval dataset is from the [the repo of G-eval](https://github.com/nlpyang/geval/tree/main/data), and the dataset of Topical-Chat is from [the repo of UniEval](https://github.com/maszhongming/UniEval/blob/main/reproduce/data/dialogue/topical_chat.json).

### File names of the prompt file

The file names for the prompts in `prompt` are quite clear and speaks for themselves.
For example, here is what you should see when `ls prompts/summeval`:
```
prompts/summeval/rel_analyze_rate_auto_cot.txt  prompts/summeval/rel_geval.txt
prompts/summeval/rel_analyze_rate.txt           prompts/summeval/rel_rate_explain_auto_cot.txt
prompts/summeval/rel_free_text_no_auto_cot.txt  prompts/summeval/rel_rate_explain.txt
prompts/summeval/rel_geval_no_auto_cot.txt
```
You can see that the file name can be represented as `"$attribution"_"$mode".txt`, where '$attribution' corresponds to the initial three letters of the attribution to be evaluated, and `$mode` is the ablations of different prompts (the **Ablations** column in Table 1 and Table 2 in our paper).


## Query GPT3.5-turbo
You need to fill in your OpenAI API key and the organization key in the `run.sh`.
```
bash run.sh
```
The available modes for`$mode` can be found in the file names of the prompts in `prompts/`.


### Results of Querying GPT3.5-turbo
We place all the results of querying ChatGPT in `results`. 



## Meta Evalation
We provide all our results in `results`.
To run the meta evaluation, simply run  `python3 all_eval.py`.
It will generate the latex-like table in our paper.
The current mode for 'all_eval.py' is for calculation Pearson's r using Method 1. If you want to calculate it with method 2, change Line 134 from `results_A = meta(input_fp, attr, 'A')` to `results_A = meta(input_fp, attr, 'B').`
Refer to the Appendix C in our paper about the difference between the two methods.
In short, Method 1 calculates the dataset-level correlation coefficient and Method 2 calculates the document-level correlation coefficent. 
We find that our conclusion holds for method 1 and method 2.


Alternatively, you can use the `meta_eval_summeval.py` to calculate the correlation coefficient for a specific attribution.
Example execution:
```
python3 meta_eval_summeval.py \
  --input results/summeval/gpt3.5_coh_analyze_rate.json \
  --dimension coherence
```

## Contact
If you have any questions, feel free to open an issue.
You can also email Cheng-Han Chiang via `dcml0714 AT gmail DOT com`.

## Citation
If you use our results or find our paper useful, please cite our paper via
```
@inproceedings{
anonymous2023a,
title={A Closer Look into Using Large Language Models for Automatic Evaluation},
author={Anonymous},
booktitle={The 2023 Conference on Empirical Methods in Natural Language Processing},
year={2023},
url={https://openreview.net/forum?id=RsK483IRuO}
}
```

If you use the codes in this repo, please also cite the G-eval paper since our codes are mainly based on thier codes.
```
@misc{liu2023geval,
      title={G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment},
      author={Yang Liu and Dan Iter and Yichong Xu and Shuohang Wang and Ruochen Xu and Chenguang Zhu},
      year={2023},
      eprint={2303.16634},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```
