from prettytable import PrettyTable
import numpy as np
from scipy.stats import spearmanr, pearsonr, kendalltau
import json
import re
import string
import argparse


def calculate_correlation(pred_score, human_score, result):
    assert len(pred_score) == len(human_score)

    if (len(result) == 0):
        result = {'pearson': 0, 'spearman': 0, 'kendalltau': 0}
    result['pearson'] += pearsonr(pred_score, human_score)[0]
    result['spearman'] += spearmanr(pred_score, human_score)[0]
    result['kendalltau'] += kendalltau(pred_score, human_score)[0]

    return result


def print_correlations(result, n):
    table = PrettyTable(['Pearson', 'Spearman', 'Kendall'])
    if (n == 0):
        n = 1
    table.add_row(
        [round(result['pearson'] / n, 4), round(result['spearman'] / n, 4), round(result['kendalltau'] / n, 4)])
    print(table)


def parse_output(output):
    ori_output = output
    output = output.lower().replace("\n", " ").replace("1-3", " ")#.replace("yes", '1').replace('no', '0')
    if "rating:" in output:
      output = output.split("rating:")[-1]
    x = re.findall("[a-z]*:?-? ?[0-9]\.?[0-9]?", output)
    if len(x) == 0:
      #print("Cannot match", output)
      pass 
    else:
      x = x[0]
      #print(f"To be replaced: {x}")
      x = re.sub(r"[a-z]*:?-? *", " ", x)
      #print(f"After replace: {x}")
      x = x.replace("rating:", "").strip()
      output = x  
    
    matched = re.search("^ ?([\d\.]+)", output)
    if (matched):
        try:
            score = float(matched.group(1))
        except:
            print("nan", output)
            score = np.nan
    else:
        score = np.nan
        print(f"Original output: {ori_output}\nScore:{score}")
    #print(output)
    #print(ori_output, score)
    if score < 0:
      score = np.nan
    return score


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_fp', type=str, default='results/gpt4_rel_detailed.json')
    parser.add_argument('--dimension', type=str, default='relevance')
    args = parser.parse_args()

    jobj = json.load(open(args.input_fp))
    pred_scores, human_scores = {}, {}

    print("Calculating correlation for G-Eval")


    pred_scores, human_scores = [], []
    for i, item in enumerate(jobj):

        all_responses = item["all_responses"]
        all_scores = [parse_output(x) for x in all_responses]
        score = np.nanmean(all_scores) 

        pred_scores.append(score)
        human_scores.append(item['scores'][args.dimension])
    print('len(pred_scores): {}'.format(len(pred_scores)))
    print('len(human_scores): {}'.format(len(human_scores)))

    results = {'pearson': 0, 'spearman': 0, 'kendalltau': 0}
    results = calculate_correlation(pred_scores, human_scores, results)
    print_correlations(results, n=1)


#    for i, item in enumerate(jobj):
#        #doc_id = item["doc_id"]
#        doc_id = item["source"]
#        if (doc_id not in pred_scores):
#            pred_scores[doc_id] = []
#            human_scores[doc_id] = []
#
#        all_responses = item["all_responses"]
#        all_scores = [parse_output(x) for x in all_responses]
#        score = np.nanmean(all_scores) 
#
#        pred_scores[doc_id].append(score)
#        human_scores[doc_id].append(item['scores'][args.dimension])
#
#    print('len(pred_scores): {}'.format(len(pred_scores)))
#    print('len(human_scores): {}'.format(len(human_scores)))
#
#    results = {'pearson': 0, 'spearman': 0, 'kendalltau': 0}
#    d_ctr = 0
#    for doc_id in pred_scores:
#        pred_scores_doc = pred_scores[doc_id]
#        human_scores_doc = human_scores[doc_id]
#        if (len(set(human_scores_doc)) <= 1) or (len(set(pred_scores_doc)) <= 1):
#            continue
#
#        results = calculate_correlation(pred_scores_doc, human_scores_doc, results)
#        d_ctr += 1
#    print_correlations(results, n=d_ctr)
