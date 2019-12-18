from nltk.corpus import wordnet as wn
from redtoolkit.textanalysis.helpers.converter import any2wnpos

import nltk

nltk.download("omw")


__all__ = ["generate_from_wordnet"]


def generate_from_wordnet(word, lang="eng", pos=None):
    """
    Generate all the synonyms from WordNet in the given language. 
    
    Args:
        word (str): 
            The word to search.
        lang (str, optional): 
            The language of the word and the language of the synonyms to find out. 
            Defaults to ``eng``.
        pos (str, optional): 
            The part-of-speech of the word to find out. 
            Defaults to None.
    
    Returns:
        list: 
            All synonyms found.

    .. highlight:: python
    .. code-block:: python

        >>> generate_from_wordnet('camminare',lang='it')
        {'andare_a_piedi', 'percorrere_a_piedi'}
    """
    norm_word = word.replace(" ", "_")

    if pos is not None:
        wn_pos = any2wnpos(pos)
    else:
        wn_pos = pos

    return set(
        [
            l.name()
            for syn in wn.synsets(norm_word, lang=lang, pos=wn_pos)
            for l in syn.lemmas(lang=lang)
            if l.name() != word
        ]
    )
