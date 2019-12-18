from redtoolkit.textanalysis.generators import synonyms


def test_generate_synonyms():
    assert synonyms.generate_from_wordnet("camminare", lang="ita", pos="VERB") == set(
        ["andare_a_piedi", "percorrere_a_piedi"]
    )
