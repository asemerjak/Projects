from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.linear_model import LogisticRegression
from typing import List, Set, Dict
import numpy as np
import pickle
import json
import nltk
import os

class ReviewSentimentClassifier:
    def __init__(self):
        """Function downloads necessary nltk components.
        Loads the ML model if it exists or trains and saves it otherwise.
        Loads top 500 positive words."""

        # downloading nltk components
        nltk.download(["names",
                        "stopwords",
                        "averaged_perceptron_tagger",
                        "vader_lexicon",
                        "punkt"], quiet=True);
        # generating list of not meaningful words
        self.unwanted: List[str] = nltk.corpus.stopwords.words("english")
        self.unwanted.extend([w.lower() for w in nltk.corpus.names.words()])

        # open set of top 500 positive words
        with open("projekt/review_sentiment_analysis/top_500_positive.json", 'r') as j:
            self.top_500_positive: Set[str] = set(json.loads(j.read()))

        # checking if saved calssifier exists
        if os.path.isfile('projekt/review_sentiment_analysis/classifier.sav'):
            # loading the classifier
            self.classifier = pickle.load(open('projekt/review_sentiment_analysis/classifier.sav', 'rb'))
        else:
            # trainig and saving the model
            self.classifier = self.train_model()

        # dictionary for formating the main output
        self.is_positive = {"neg": 0, "pos": 1}


    def extract_features(self, text: str)-> Dict[str, float]:
        """Generates dict of features for the whole text.

        Args:
            text (str): Text of the review to be processed.

        Returns:
            Dict[str, float]: Dict of features of the text.
        """
        features: Dict[str, float] = dict()
        wordcount: int = 0
        compound_scores: List[float] = list()
        positive_scores: List[float] = list()

        sia = SentimentIntensityAnalyzer()

        for sentence in nltk.sent_tokenize(text):
            filtered_sentence = [word for word in nltk.word_tokenize(sentence) if word not in self.unwanted]
            filtered_sentence = " ".join(filtered_sentence)
            for word in nltk.word_tokenize(filtered_sentence):
                if word.lower() in self.top_500_positive:
                    wordcount += 1
            
            compound_scores.append(sia.polarity_scores(filtered_sentence)["compound"])
            positive_scores.append(sia.polarity_scores(filtered_sentence)["pos"])

        features["mean_compound"] = np.mean(compound_scores) + 1
        features["mean_positive"] = np.mean(positive_scores)
        features["wordcount"] = wordcount

        return features


    def train_model(self):
        """Trains and saves machine learning model for sentiment analysis in .sav format.

        Returns:
            Trained classifier
        """
        features = [(self.extract_features(nltk.corpus.movie_reviews.raw(review)), "pos")
                    for review in nltk.corpus.movie_reviews.fileids(categories=["pos"])]

        features.extend([(self.extract_features(nltk.corpus.movie_reviews.raw(review)), "neg")
                    for review in nltk.corpus.movie_reviews.fileids(categories=["neg"])])

        classifier = nltk.classify.SklearnClassifier(LogisticRegression())
        classifier.train(features)

        filename = 'projekt/review_sentiment_analysis/classifier.sav'
        pickle.dump(classifier, open(filename, 'wb'))

        return classifier


    def get_sentiment(self, text: str)-> bool:
        """Predicts the text sentiment.

        Args:
            text (str): Text of the review to be processed.

        Returns:
            bool: 0 if sentiment is negative, 1 if positive.
        """
        return self.is_positive[self.classifier.classify(self.extract_features(text))]
 

# sample1 = "Great book! Very interesting! It was a pleasure to read it."
# sample2 = "What a terrible product."
# clf = ReviewSentimentClassifier()
# print(clf.get_sentiment(sample1))
# print(clf.get_sentiment(sample2))