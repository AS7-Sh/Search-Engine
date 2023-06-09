import re
import string
from typing import List
import numpy as np
from nltk import tokenize, pos_tag
from nltk.corpus import stopwords
from services.text_processing.lemmatizer import LemmatizerWithPOSTagger
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet


class TextPreprocessor:
    def __init__(self) -> None:
        self.tokenizer = tokenize.word_tokenize
        self.stopwords_tokens = stopwords.words('english')
        self.stemmer = PorterStemmer()
        self.lemmatizer = LemmatizerWithPOSTagger()

    def tokenize(self, text: str) -> List[str]:
        tokens = self.tokenizer(text)
        return tokens

    @staticmethod
    def to_lower(tokens: List[str]) -> List[str]:
        lower_tokens = []
        for token in tokens:
            lower_token = str(np.char.lower(token))
            lower_tokens.append(lower_token)
        return lower_tokens

    @staticmethod
    def remove_markers(tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(re.sub(r'\u00AE', '', token))
        return new_tokens

    @staticmethod
    def remove_punctuation(tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(token.translate(str.maketrans('', '', string.punctuation)))
        return new_tokens

    @staticmethod
    def replace_under_score_with_space(tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(re.sub(r'_', ' ', token))
        return new_tokens

    def remove_stop_words(self, tokens: List[str]) -> list[str]:
        new_tokens = []
        for token in tokens:
            if token not in self.stopwords_tokens and len(token) > 1:
                new_tokens.append(token)
        return new_tokens

    @staticmethod
    def remove_apostrophe(tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(str(np.char.replace(token, "'", " ")))
        return new_tokens

    def stemming(self, tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(self.stemmer.stem(token))
        return new_tokens

    @staticmethod
    def normalize_abbreviations(tokens: List[str]) -> List[str]:
        resolved_terms = {}
        for token in tokens:

            if len(token) >= 2:
                synsets = wordnet.synsets(token)
                if synsets:
                    resolved_term = synsets[0].lemmas()[0].name()
                    resolved_terms[token] = resolved_term

        for abbreviation, resolved_term in resolved_terms.items():
            for i in range(len(tokens)):
                if tokens[i] == abbreviation:
                    tokens[i] = resolved_term
                    break

        return tokens

    def lemmatizing(self, tokens: List[str]) -> List[str]:
        tagged_tokens = pos_tag(tokens)
        lemmatized_tokens = [self.lemmatizer.lemmatize(token, pos) for token, pos in tagged_tokens]
        return lemmatized_tokens

    def preprocess(self, text: str) -> str:
        operations = [
            self.to_lower,
            self.remove_punctuation,
            self.remove_apostrophe,
            self.remove_stop_words,
            self.remove_markers,
            self.stemming,
            self.lemmatizing,
            self.normalize_abbreviations,
            self.to_lower,
            self.replace_under_score_with_space
        ]
        text_tokens = self.tokenize(text)
        for op in operations:
            text_tokens = op(text_tokens)

        new_text = ' '.join(text_tokens)

        return new_text
