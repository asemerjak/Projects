import nltk
import json

def generate_top_500_pos()-> None:
    """Generates top 500 positive words from movie reviews dataset.
    The file is later saved to .json format. If the file already exists,
    there's no need to run it."""

    unwanted = nltk.corpus.stopwords.words("english")
    unwanted.extend([w.lower() for w in nltk.corpus.names.words()])

    def skip_unwanted(pos_tuple):
        word, tag = pos_tuple
        if not word.isalpha() or word in unwanted:
            return False
        if tag.startswith("NN"):
            return False
        return True

    positive_words = [word for word, _ in filter(
        skip_unwanted,
        nltk.pos_tag(nltk.corpus.movie_reviews.words(categories=["pos"])))]

    negative_words = [word for word, _ in filter(
        skip_unwanted,
        nltk.pos_tag(nltk.corpus.movie_reviews.words(categories=["neg"])))]

    positive_fd = nltk.FreqDist(positive_words)
    negative_fd = nltk.FreqDist(negative_words)

    common_set = set(positive_fd).intersection(negative_fd)

    for word in common_set:
        del positive_fd[word]
        del negative_fd[word]

    top_500_positive = {word for word, _ in positive_fd.most_common(500)}

    with open("projekt/review_sentiment_analysis/top_500_positive.json", "w") as outfile:
        json.dump(list(top_500_positive), outfile)