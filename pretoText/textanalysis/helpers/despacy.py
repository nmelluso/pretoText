import re


__all__ = [
    "get_attributes_as_dict",
    "get_clean_text",
    "get_clean_text_filtered_by_pos",
    "get_clean_text_filtered_by_attributions",
    "get_docs_clean_sentences_as_tuples",
]


RE_CLEANER = re.compile(r"[A-Za-z0-9]+$")


def get_attributes_as_dict(spacy_token, attrs):
    """ 
    Turns :class:`spacy.tokens.Token` attributes into a dictionary.
    
    Args:
        token (spacy.tokens.Token): 
            The token to take attributes from.
        attrs (list): 
            Attributes to extract. 
    
    Returns:
        dict: 
            Key-valued attributes.

    
    .. highlight:: python
    .. code-block:: python

        >>> get_attributes_as_dict(doc[3],["dep_","pos_"])
        {'dep_': 'attr', 'pos_': 'NOUN'}


    """
    return {
        attr: getattr(spacy_token, attr) for attr in attrs if hasattr(spacy_token, attr)
    }


def get_clean_text(spacy_doc):
    """ 
    Turns :class:`spacy.tokens.Doc` into clean text where only lowered alphanumeric words are kept.
    
    Args:
        spacy_doc (spacy.tokens.Doc): 
            ``Doc`` where to get clean text from.
    
    Returns:
        str: 
            Clean text.
    """
    return get_clean_text_filtered_by_attributions(spacy_doc, {"text": []})


def get_clean_text_filtered_by_pos(spacy_doc, postags):
    """ 
    Turns a :class:`spacy.tokens.Doc` into clean text where only lowered alphanumeric words are kept,
    and words must be of specific POS tags only.

    Args:
        spacy_doc (spacy.tokens.doc): 
            ``Doc`` where to get filtered text from.
        postags (list): 
            POS tags to keep in text.
    
    Returns:
        str: 
            Clean text filtered by POS tags.
    """
    return get_clean_text_filtered_by_attributions(spacy_doc, {"pos_": postags})


def get_clean_text_filtered_by_attributions(spacy_doc, attributions):
    """
    Turns a :class:`spacy.tokens.Doc` into clean text where only lowered alphanumeric words are kept,
    and tokens must have only allowed values for the attributes specified.
    An attribution can also be set as negative by prefixing a `!` character to the attribute, 
    hence its list of values will be considered as a blacklist.
    If no allowed value is given for an attribute, or its list is empty, all values are allowed.

    Args:
        spacy_doc (spacy.tokens.Doc): 
            ``Doc`` where to get filtered text from.
        attributions (dict): 
            Attributes key-valued to their list of allowed values.
            If an attribute is prefixed with a `!` character, its list turns in not allowed values.

    Returns:
        str: 
            Clean text filtered by tokens having only allowed values for the attribute specified.

    .. highlight:: python
    .. code-block:: python

        >>> doc=nlp("This is the sentence I want to test")
        >>> get_clean_text_filtered_by_attributions(doc,{"pos_":"VERB","!text":"want"})
        'is test'


            
    """
    return " ".join(
        [
            token.text.lower()
            for token in spacy_doc
            if (
                all(
                    [
                        (
                            hasattr(token, attr)
                            and (not values or getattr(token, attr) in values)
                        )
                        or (
                            attr.startswith("!")
                            and hasattr(token, attr[1:])
                            and (not values or getattr(token, attr[1:]) not in values)
                        )
                        for attr, values in attributions.items()
                    ]
                )
                and RE_CLEANER.match(token.text)
            )
        ]
    )


def get_docs_clean_sentences_as_tuples(
    doc_list,
    relevant_tags=["NOUN", "VERB", "ADJ", "ADV"],
    word=" ",
    blacklist=[],
    min_length=10,
):
    """Turns a list of :class:`spacy.token.Doc` into a list of tuples with the sentences
    contained in the documents of doclist and a cleaned version of the same sentence.
    
    Args:
        doc_list (list): 
            List of :class:`spacy.tokens.Doc`.
        relevant_tags (list, optional): 
            List of pos tags to keep when cleaning the sentence. 
            Defaults to ["NOUN", "VERB", "ADJ", "ADV"].
        word (str, optional): 
            If word is in a sentence then that sentence is ignored. 
            Defaults to " ".
        blacklist (list, optional): 
            List of strings which get remove when cleaning the sentence. 
            Defaults to [].
        min_length (int, optional): 
            Minimum length in number of characters a sentence needs to have to not be ignored. 
            Defaults to 50.
    
    Returns:
        list: 
        List of tuples with a sentence of only alpha numeric as first entry and as second entry a cleaned sentence with only words.

    .. highlight:: python
    .. code-block:: python

        >>> test_text_to_show_1 = \"\"\"We can for example examine this small text, composed of long enough sentences. Where some important words are present, even though some word to ignore are present too and we will see how they are not considered. \"\"\"
        >>> test_text_to_show_2 = \"\"\"We can also look at too short sentences. Or at sentences where a forbidden word is present so that they will be ignored even if long enough.\"\"\"
        >>> test_doc_to_show = [nlp(test_text_to_show_one),nlp(test_text_to_show_two)]
        >>> spacy_doclist_to_list_of_tuples_sentence_clean_sentence(test_doc_to_show,relevant_tags=['NOUN','VERB'],word="forbidden",blacklist="ignore",min_length=50)
        [('we can for example examine this small text composed of long enough sentences',
          'can example examine text composed sentences'),
         ('where some important words are present even though some word to ignore are present too and we will see how they are not considered',
          'words are word are will see are considered')]
    """

    output_dict = {}
    for doc in doc_list:
        for sent in doc.sents:
            if word in sent.text.split(" ") or len(sent.text) < min_length:
                continue
            output_dict[
                get_clean_text_filtered_by_attributions(
                    sent, {"pos_": relevant_tags, "!text": blacklist}
                )
            ] = get_clean_text(sent)

    return [(item[1], item[0]) for item in output_dict.items()]
