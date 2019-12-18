from redtoolkit.textanalysis.helpers import despacy
from redtoolkit.scidata import dataframes

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import numpy as np


class BaseClassifier:
    """Basic classifier structure to help build proper ones, not supposed to be called.
    """

    def __init__(
        self,
        training_doclist,
        predicting_doclist,
        target_words,
        nlp,
        relevant_tags=["NOUN", "VERB", "ADJ"],
        min_length=10,
    ):
        self.target_words = target_words
        self.nlp = nlp
        self.min_length = min_length
        self.relevant_tags = relevant_tags
        self.training_doclist = despacy.get_docs_clean_sentences_as_tuples(
            [self.nlp(doc) for doc in training_doclist],
            self.relevant_tags,
            min_length=self.min_length,
        )

        self.predicting_doclist = despacy.get_docs_clean_sentences_as_tuples(
            [self.nlp(doc) for doc in predicting_doclist],
            self.relevant_tags,
            min_length=self.min_length,
        )
