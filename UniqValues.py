from collections import Counter
from typing import List, Tuple

import numpy as np

import TwoSampleHC


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
    pvals = TwoSampleHC.two_sample_pvals(list1, list2)

    hctest = TwoSampleHC.HC(pvals)
    hc, pstar = hctest.HC()

    ##############
    word_pvals = []
    for i, w in enumerate(all_words):
        if pvals[i] < pstar:
            word_pvals.append((w, pvals[i]))
    return word_pvals


if __name__ == '__main__':
    text1 = open('processed_output/2022_reviews_adj_adv.txt', 'r').read()
    text2 = open('processed_output/2024_reviews_adj_adv.txt', 'r').read()
    pvals = get_pvals(text1, text2)

    for pval in pvals:
        print(pval)
