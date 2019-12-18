def test_import_pretoText():
    try:
        import pretoText

        dir(pretoText.scidata)
        dir(pretoText.scidata.dataframes)
        dir(pretoText.scidata.graphs)
        dir(pretoText.scidata.vectors)

        dir(pretoText.textanalysis)
        dir(pretoText.textanalysis.classifiers)
        dir(pretoText.textanalysis.classifiers.bow_classifier)
        dir(pretoText.textanalysis.extractors)
        dir(pretoText.textanalysis.generators)
        dir(pretoText.textanalysis.generators.synonyms)
        dir(pretoText.textanalysis.helpers)
        dir(pretoText.textanalysis.helpers.converter)
        dir(pretoText.textanalysis.helpers.despacy)
        dir(pretoText.textanalysis.helpers.splitter)
        dir(pretoText.textanalysis.similarities)
        dir(pretoText.textanalysis.similarities.embeddings)
        dir(pretoText.textanalysis.similarities.wordnet)

        dir(pretoText.utils)
        dir(pretoText.utils.importers)
        dir(pretoText.utils.exporters)
        dir(pretoText.utils.parallelism)
        dir(pretoText.utils.spacy)

        pretoText.visualizers

        dir(pretoText.wrappers.mooc.coursera)

    except (AttributeError, ImportError, ModuleNotFoundError):
        assert False

    assert True
