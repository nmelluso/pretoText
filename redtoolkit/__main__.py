if __name__ == "__main__":
    from os.path import dirname
    import sys

    # fix root module importing
    sys.path.append(dirname("."))

    from redtoolkit.textanalysis import embeddings
    from redtoolkit.textanalysis import wordnet
    from redtoolkit.textanalysis import synonyms
    from redtoolkit.utils import spacy
    from redtoolkit.wrappers import mooc
    from redtoolkit.wrappers import wikipedia
    import fire

    # Commands exposed to CLI

    fire.Fire(
        {
            "ranking_by_embeddings_from_gsheet": embeddings.ranking_by_embeddings_from_gsheet,
            "ranking_by_wordnet_from_gsheet": wordnet.ranking_by_wordnet_from_gsheet,
            "spacy_download": spacy.download_model,
            "dump_coursera_all": mooc.coursera.dump_all,
            "dump_coursera_search": mooc.coursera.dump_from_search,
            "wikipedia_linking_graph": wikipedia.extractors.linking_graph_as_df,
            "wordnet_synonyms": synonyms.generate_from_wordnet,
        }
    )
