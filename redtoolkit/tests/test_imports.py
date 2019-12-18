def test_import_redtoolkit():
    try:
        import redtoolkit

        dir(redtoolkit.scidata)
        dir(redtoolkit.scidata.dataframes)
        dir(redtoolkit.scidata.graphs)
        dir(redtoolkit.scidata.vectors)

        dir(redtoolkit.textanalysis)
        dir(redtoolkit.textanalysis.classifiers)
        dir(redtoolkit.textanalysis.classifiers.bow_classifier)
        dir(redtoolkit.textanalysis.extractors)
        dir(redtoolkit.textanalysis.generators)
        dir(redtoolkit.textanalysis.generators.synonyms)
        dir(redtoolkit.textanalysis.helpers)
        dir(redtoolkit.textanalysis.helpers.converter)
        dir(redtoolkit.textanalysis.helpers.despacy)
        dir(redtoolkit.textanalysis.helpers.splitter)
        dir(redtoolkit.textanalysis.similarities)
        dir(redtoolkit.textanalysis.similarities.embeddings)
        dir(redtoolkit.textanalysis.similarities.wordnet)

        dir(redtoolkit.utils)
        dir(redtoolkit.utils.importers)
        dir(redtoolkit.utils.exporters)
        dir(redtoolkit.utils.parallelism)
        dir(redtoolkit.utils.spacy)

        redtoolkit.visualizers

        dir(redtoolkit.wrappers.mooc.coursera)

    except (AttributeError, ImportError, ModuleNotFoundError):
        assert False

    assert True
