from redtoolkit.textanalysis.classifiers import bow_classifier
import numpy as np
import spacy


nlp = spacy.load("en_core_web_sm")


def test_bow_classifier():

    test_training_doclist = [
        "sentence 1 has the word target and it has to have more than 50 characters just because",
        "sentence 2 has the word target we really care that there are enough letters everywhere",
        "sentence 3 has the word target unless you don't believe this couls ever possibily be done",
        "sentence 4 has the word target and it has to have more than 50 characters just because",
        "these 3 don't have the word we look for which is completely irrelevant in everyone's opinion",
        "so this one does not, hey hey hey, missing some words aren't we?? maybe a little bit more",
        " also some random signs \n @ and again here it comes the trick needs to be done on purpose",
        "and some more.. otherwise we have no clue as to what we're here for which is interesting enough",
        "then again target unless you look at it from the wrong perspective all over the place without sentence",
    ]

    test_predicting_doclist = [
        "this sentence has the word target and needs more than 50 characters",
        "but it is not here as you can see from this long phrase",
    ]

    np.random.seed(13)
    extractor = bow_classifier.BowClassifier(
        test_training_doclist, test_predicting_doclist, ["target"], nlp
    )

    extractor.struct_classifier()

    extractor.train_classifier()

    predicted = extractor.predict_new(10)

    assert predicted == [
        "this sentence has the word target and needs more than 50 characters"
    ]
