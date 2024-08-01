import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv(r"")
    ndf = df[df["year"] == 2024]
    raw_old_reviews = ndf["review"].tolist()
    old_reviews = []

    for raw_review in raw_old_reviews:
        review = raw_review
        review = review.replace(".", " ")
        review = review.replace(",", " ")
        review = review.replace(r"\n", " ")
        review = review.replace("  ", " ")
        old_reviews.append(review)
    old_reviews_all_words = []
    for review in old_reviews:
        old_reviews_all_words += str(review).split()
    t = "\n".join(old_reviews_all_words)
    with open(r"C:\Degree\Courses\Research\test_2024_reviews_all_words", "wb") as f:
        f.write(t.encode())
