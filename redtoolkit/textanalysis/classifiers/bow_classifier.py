from redtoolkit.textanalysis.helpers import despacy
from redtoolkit.scidata import dataframes
from redtoolkit.textanalysis.classifiers.base_classifier import BaseClassifier

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import numpy as np


class BowClassifier(BaseClassifier):
    r"""Class to perform a support vector machine on a bag of word representation of text.
    
    Returns:
        class: A class where all the steps of a classification process are joined together.

    .. highlight:: python
    .. code-block:: python

        >>> test_training_doclist = [
              "sentence 1 has the word target and it has to have more than 50 characters just because",
              "sentence 2 has the word target we really care that there are enough letters everywhere",
              "sentence 3 has the word target unless you don't believe this could ever possibily be done",
              "sentence 4 has the word target and it has to have more than 50 characters just because",
              "these 3 don't have the word we look for which is completely irrelevant in everyone's opinion",
              "so this one does not, hey hey hey, missing some words aren't we?? maybe a little bit more",
              " also some random signs \n @ and again here it comes the trick needs to be done on purpose",
              "and some more.. otherwise we have no clue as to what we're here for which is interesting enough",
              "then again target unless you look at it from the wrong perspective all over the place without sentence"
            ]
        >>> test_predicting_doclist = [
                "this sentence has the word target and needs more than 50 characters",
                "but it is not here as you can see from this long phrase"
                ]
        >>> extractor = bow_classifier.AutomaticSentenceRecover(
                test_training_doclist, test_predicting_doclist, ["target"], nlp
            )
        >>> extractor.struct_data()
        >>> extractor.train_classifier()
        >>> predicted = extractor.predict_new(10)
        ["this sentence has the word target and needs more than 50 characters"]

    """

    def __init__(self, training_doclist, predicting_doclist, target_words, nlp):

        super().__init__(training_doclist, predicting_doclist, target_words, nlp)

        self.score = {"accuracy": 0, "precision": 0, "recall": 0, "F1_score": 0}

        self.vectorizer = CountVectorizer()

        self.classifier = LinearSVC()

        self.X = None

        self.y = None

    def struct_classifier(self):
        """ Structures the data into a sparse matrix and a target vector for the training.
        """

        is_target = lambda x: len(set(self.target_words).intersection(x.split(" "))) > 0

        positive_examples = [
            item for item in self.training_doclist if is_target(item[0])
        ]

        negative_examples = [
            item for item in self.training_doclist if not is_target(item[0])
        ]

        examples = positive_examples + negative_examples[: len(positive_examples)]

        self.X = self.vectorizer.fit_transform([item[1] for item in examples])

        self.y = dataframes.target_values_vec(
            [item[0] for item in examples], self.target_words
        )

    def train_classifier(self):
        """ After splitting the dataset into train and test 
            train a linear support vector machine on the dataset
            also writes accuracy, precision, recall, F1 in their respective 
            instance variables.
        """
        train, test, train_labels, test_labels = train_test_split(
            self.X, self.y, test_size=0.1
        )
        self.classifier.fit(train, train_labels)
        self.score["accuracy"] = (
            accuracy_score(self.classifier.predict(test), test_labels),
        )
        self.score["precision"] = (
            precision_score(self.classifier.predict(test), test_labels),
        )
        self.score["recall"] = (
            recall_score(self.classifier.predict(test), test_labels),
        )
        self.score["F1"] = f1_score(self.classifier.predict(test), test_labels)

    def predict_new(self, num_sentences):
        """ Predicts which sentences respect the patterns from the given predicting_doclist.
        
        Args:
            num_sentences (int): Number of sentences to return
        
        Returns:
            (list): list of predicted sentences from the predicting_doclist.
        """
        sentences_data = self.vectorizer.transform(
            [item[1] for item in self.predicting_doclist]
        )

        sentences_vec = np.array([item[0] for item in self.predicting_doclist])

        predicted_sentences = list(
            sentences_vec[self.classifier.predict(sentences_data).astype(bool)]
        )

        return predicted_sentences[:num_sentences]
