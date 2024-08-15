from collections import Counter
import json
import numpy as np
import two_sample_hc


def get_pvals(text1: str, text2: str):
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

    # Assign pvals to year #

    word_pvals = {}
    pvals_2022 = {}
    pvals_2024 = {}

    for i, w in enumerate(all_words):
        if pvals[i] < pstar:
            word_pvals[w] = pvals[i]
            if word_freq1.get(w, 0) >= word_freq2.get(w, 0):
                pvals_2022[w] = pvals[i]
            else:
                pvals_2024[w] = pvals[i]

    return word_pvals, pvals_2022, pvals_2024


def extrac_text_to_json_format():
    """

    Extract the words with small pvals from the two text files and stores it in a json format
    The code generates the formats by the year of the paper.

    """
    text1 = open('processed_output/2022_submissions_adj_adv.txt', 'r').read()
    text2 = open('processed_output/2024_submissions_adj_adv.txt', 'r').read()
    pvals, pvals_2022, pvals_2024 = get_pvals(text1, text2)

    json.dump(pvals, open("processed_output/pvals_submiossions.json", "w"))
    json.dump(pvals_2022, open("processed_output/pvals_2022.json", "w"))
    json.dump(pvals_2024, open("processed_output/pvals_2024.json", "w"))


def get_submissions_and_reviews_diff():
    """

    Returns: List of the difference between the pvals of the submissions and the reviews.

    """
    submissions_text = json.load(open("processed_output/pvals_submiossions.json", 'r'))
    reviews_text = json.load(open("processed_output/pvals_reviews.json", 'r'))
    list1 = submissions_text.keys()
    list2 = reviews_text.keys()
    list3 = list(set(list2) - set(list1))
    return list3


def get_common_cgpt_in_difference(difference):
    """

    Args:
        difference: List of the difference between the pvals of the submissions and the reviews

    Returns: List of the mutual words between the difference and the common ChatGPT words.

    """
    mutual_words = []
    with open("inputs/chat_gpt_generated_words_long.txt", "r") as f:
        chat_gpt_words = f.readlines()
        for word in chat_gpt_words:
            word = word.lower()[:-1]
            if word in difference:
                mutual_words.append(word)
    return mutual_words


if __name__ == '__main__':

    difference = get_submissions_and_reviews_diff()
    mutual_words = get_common_cgpt_in_difference(difference)
