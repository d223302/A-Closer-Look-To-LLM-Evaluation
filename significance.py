from prettytable import PrettyTable
from scipy import stats
import numpy as np
import sys
from scipy.stats import spearmanr, pearsonr, kendalltau
import json
import re
import string
import argparse


def williams_test(r12, r13, r23, n):
    """The Williams test (Evan J. Williams. 1959. Regression Analysis, volume 14. Wiley, New York, USA)
    
    A test of whether the population correlation r12 equals the population correlation r13.
    Significant: p < 0.05
    
    Arguments:
        r12 (float): correlation between x1, x2
        r13 (float): correlation between x1, x3
        r23 (float): correlation between x2, x3
        n (int): size of the population
        
    Returns:
        t (float): Williams test result
        p (float): p-value of t-dist
    """
    if r12 < r13:
        print('r12 should be larger than r13')
        sys.exit()
    elif n <= 3:
        print('n should be larger than 3')
        sys.exit()
    else:
        K = 1 - r12**2 - r13**2 - r23**2 + 2*r12*r13*r23
        denominator = np.sqrt(2*K*(n-1)/(n-3) + (((r12+r13)**2)/4)*((1-r23)**3))
        numerator = (r12-r13) * np.sqrt((n-1)*(1+r23))
        t = numerator / denominator
        p = 1 - stats.t.cdf(t, df=n-3) # changed to n-3 on 30/11/14
        return t, p

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
    #output = output.split("Rationale")[0].strip().strip("Rating:").strip().strip("-").strip().strip("Rating").strip().strip(":").strip()
    
    output = output.lower().replace("\n", " ").replace("1-3", " ")#.replace("yes", '1').replace('no', '0')
    if "rating:" in output:
      output = output.split("rating")[-1]
    x = re.findall("[a-z]*:?-? *[0-9]\.?[0-9]?", output)
    if len(x) == 0:
      #print("Cannot match", output)
      pass 
    else:
      x = x[0]
      x = re.sub(r"[a-z]*:?-? *", "", x)
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
        print(ori_output, output, score)
    #print(output)
    #print(ori_output, score)
    if score < 0:
      score = np.nan
    return score

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_fp_1', type=str, default='results/gpt4_rel_detailed.json')
    parser.add_argument('--input_fp_2', type=str, default='results/gpt4_rel_detailed.json')
    parser.add_argument('--dimension', type=str, default='relevance')
    args = parser.parse_args()

    jobj = json.load(open(args.input_fp_1))
    jobj_2 = json.load(open(args.input_fp_2))

    print("Calculating correlation for G-Eval")



    def get_result(jobj):
        pred_scores, human_scores = {}, {}
        for i, item in enumerate(jobj):
            #doc_id = item["doc_id"]
            doc_id = item["source"]
            system_id = item["system_id"]
            if (doc_id not in pred_scores):
                pred_scores[doc_id] = {}
                human_scores[doc_id] = {}
    
            all_responses = item["all_responses"]
            all_scores = [parse_output(x) for x in all_responses]
            score = np.nanmean(all_scores) 
    
            pred_scores[doc_id][system_id] = score
            human_scores[doc_id][system_id] = item['scores'][args.dimension]

        return pred_scores, human_scores

    pred_scores_1, human_scores_1 = get_result(jobj)
    pred_scores_2, human_scores_2 = get_result(jobj_2)

    key_0 = [k for k in pred_scores_1][0]

    new_pred_scores_1, new_pred_scores_2, new_human_scores = [], [], []

    for doc_id in pred_scores_1:
      if doc_id not in pred_scores_2:
        continue
      for system_id in pred_scores_1[doc_id]:
        if system_id not in pred_scores_2[doc_id]:
          continue
        new_pred_scores_1.append(pred_scores_1[doc_id][system_id])
        new_pred_scores_2.append(pred_scores_2[doc_id][system_id])
        new_human_scores.append(human_scores_1[doc_id][system_id])
    
    print(len(new_pred_scores_1))
    corr_1 = pearsonr(new_pred_scores_1, new_human_scores)[0]
    corr_2 = pearsonr(new_pred_scores_2, new_human_scores)[0]
    inter_corr = pearsonr(new_pred_scores_1, new_pred_scores_2)[0]

    print(f"Corr 1: {corr_1}, corr 2: {corr_2}, inter corr: {inter_corr}")
    t, p = williams_test(corr_1, corr_2, inter_corr, len(new_pred_scores_1))
    print(t, p)
