import re

import pandas as pd

FULL_REVIEWS_FILE_PATH = r"C:\Degree\Courses\Research\ICLR review data\reviews_iclr_2018_2024_annotated.csv"
ADJ_ADV_REVIEWS_FILE_PATH = r"C:\Degree\Courses\Research\ICLR review data\reviews_iclr_2018_2024_annotated_adj_adv.csv"


def clean_txt(text):
    text = str(text)  # in case the data in the column is being read as another type
    text = text.replace("\n", " ")
    text = text.replace(".", " ")
    text = text.replace(",", " ")
    text = re.sub(r'[^a-z0-9 -]', '', text.lower())  # lower case, only letters or digits
    return text


def extract_data_from_csv(input_file: str,
                          output_file: str,
                          year_to_filter: int,
                          year_col_id: str = "year",
                          text_col_id: str = "text"):
    """
    Extract all data from `text_col_id` column from `input_file`, and write it to `output_file`
    Args:
        input_file: path to input csv file
        output_file: path to output file
        year_to_filter: the year that we want the data from
        year_col_id: the column name that holds the year in the csv file
        text_col_id: the column name that holds the text in the csv file
    """
    df = pd.read_csv(input_file)
    filtered_df = df[df[year_col_id] == year_to_filter]
    raw_texts = filtered_df[text_col_id].tolist()
    cleaned_texts = [clean_txt(text) for text in raw_texts]
    all_words = []
    for text in cleaned_texts:
        all_words.extend(text.split())
    with open(output_file, "w") as f:
        f.write(" ".join(all_words))


def main():
    extract_data_from_csv(FULL_REVIEWS_FILE_PATH,
                          "processed_output/2022_reviews_all_words.txt",
                          2022,
                          text_col_id="review")
    extract_data_from_csv(FULL_REVIEWS_FILE_PATH,
                          "processed_output/2024_reviews_all_words.txt",
                          2024,
                          text_col_id="review")
    extract_data_from_csv(ADJ_ADV_REVIEWS_FILE_PATH,
                          "processed_output/2022_reviews_adj_adv.txt",
                          2022,
                          year_col_id="author")
    extract_data_from_csv(ADJ_ADV_REVIEWS_FILE_PATH,
                          "processed_output/2024_reviews_adj_adv.txt",
                          2024,
                          year_col_id="author")


if __name__ == '__main__':
    main()
