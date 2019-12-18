def split_sentence_attaching_id(text, starting_id="", splitter="\n\n"):
    r"""
    This function split a sentence according to a splitter element (default set as \\n\\n) and assign an id to the
    sentences created. It starts indexing by enumerating the sentences from 00001.
    
    Args:
        text (str): 
            the string to be splitted in sentences
        starting_id (str, optional): 
            The first part of the index assigned to the sentence. 
            Defaults to ``emptystring``.
        splitter (str, optional): 
            The delimiter of splitting the text into sentences. 
            Defaults to "\\n\\n".
    
    Returns:
        dict: 
            a dictionary containing as key the id of the sentence and as value the sentence splitted
    """

    splitted_list = text.split(splitter)

    output = {}

    for id, sent in enumerate(splitted_list):
        output[str(starting_id) + "%05d" % (id + 1,)] = sent

    return output
