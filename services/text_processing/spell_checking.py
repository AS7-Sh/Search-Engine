from spellchecker import SpellChecker

from services.text_processing.data_preprocessing import TextPreprocessor


def correct_data_spelling(query) -> str:
    tokens = TextPreprocessor().tokenize(query)
    spell = SpellChecker()
    misspelled = spell.unknown(tokens)
    for i, token in enumerate(tokens):
        if token in misspelled:
            corrected = spell.correction(token)
            if corrected:
                tokens[i] = corrected

    corrected_query = ' '.join(tokens)

    return corrected_query
