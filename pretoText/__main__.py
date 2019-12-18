if __name__ == "__main__":
    from os.path import dirname
    import sys

    # fix root module importing
    sys.path.append(dirname("."))

    from pretoText.textanalysis import embeddings
    from pretoText.textanalysis import wordnet
    from pretoText.textanalysis import synonyms
    from pretoText.utils import spacy
    from pretoText.wrappers import mooc
    from pretoText.wrappers import wikipedia
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
