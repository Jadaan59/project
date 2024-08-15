from collections import Counter
from typing import List, Tuple
import json
import numpy as np

import two_sample_hc


def get_pvals(text1: str, text2: str) -> List[Tuple[str, np.float64]]:
    """
    Gets two texts, compares them and extracts the smallest p-values

    Returns: A list of tuples containing the string and its p-value
    """
    word_freq1 = Counter(text1.split())
    word_freq2 = Counter(text2.split())
    all_words = set(word_freq1.keys() | word_freq2.keys())

    all_word_counts = {}
    for word in all_words:
        all_word_counts[word] = [word_freq1.get(word, 0), word_freq2.get(word, 0)]

    list1 = np.array([all_word_counts[k][0] for k in all_word_counts])
    list2 = np.array([all_word_counts[k][1] for k in all_word_counts])
    pvals = two_sample_hc.two_sample_pvals(list1, list2)
    two_sample_hc.visualize_HCT(pvals)

    hctest = two_sample_hc.HC(pvals)

    hc, pstar = hctest.HC()

    ##############
    word_pvals = {}
    #pvals_2022 = {}
    #pvals_2024 = {}
    for i, w in enumerate(all_words):
        if pvals[i] < pstar:
            word_pvals[w] = pvals[i]
            #attribution = ""
#            if word_freq1.get(w, 0) >= word_freq2.get(w, 0):
 #               attribution = "2022"
                #pvals_2022[w] = pvals[i]
#            else:
                #attribution = "2024"
                #pvals_2024[w] = pvals[i]
    json.dump(word_pvals, open("processed_output/pvals_submiossions.json", "w"))


    #json.dump(pvals_2022, open("processed_output/pvals_2022.json", "w"))
    #json.dump(pvals_2024, open("processed_output/pvals_2024.json", "w"))


    with open("inputs/chat_gpt_generated_words_long.txt", "r") as f:
        common_words = f.readlines()
        counter_2022 = 0
        counter_2024 = 0
        print("****************************************************\n               2024")
        for common_word in common_words:
            common_word = common_word.lower()[:-1]
       #     if common_word in pvals_2024.keys():
       #         counter_2024 += 1
       #         print(common_word)
        print(counter_2024)

        print("****************************************************\n               2022")
        for common_word in common_words:
            common_word = common_word.lower()[:-1]
        #    if common_word in pvals_2022.keys():
        #        counter_2022 += 1
        #        print(common_word)
        print(counter_2022)
        print("****************************************************")



    return word_pvals


if __name__ == '__main__':
 #   text1 = open('processed_output/2022_submissions_adj_adv.txt', 'r').read()
 #  text2 = open('processed_output/2024_submissions_adj_adv.txt', 'r').read()
 #  pvals = get_pvals(text1, text2)
    sub_text = json.load(open("processed_output/pvals_submiossions.json",'r'))
    reviews_text = json.load(open("processed_output/pvals_reviews.json", 'r'))
    list1 = sub_text.keys()
    list2 = reviews_text.keys()
    list3 = list(set(list2) - set(list1))

    with open("inputs/chat_gpt_generated_words_long.txt", "r") as f:
        common_words = f.readlines()
        counter = 0
        for common_word in common_words:
            common_word = common_word.lower()[:-1]
            if common_word in list3:
                print(common_word)
                counter += 1
        print(counter)

'''
    for pval in pvals:
        print(pval)
        new_pvals.append(pval[0])
'''

