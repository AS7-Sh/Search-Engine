import pymongo

from pymongo import MongoClient

client = MongoClient("localhost:27017")

db = client["IR"]
col = db["wikir"]

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from typing import List


class LemmatizerWithPOSTagger(WordNetLemmatizer):
    def __init__(self):
        pass

    def _get_wordnet_pos(self, tag: str) -> str:
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def lemmatize(self, word: str, pos: str = "n") -> str:
        return super().lemmatize(word, self._get_wordnet_pos(pos))


import re
import string
from typing import Callable

import numpy as np
from nltk import tokenize, pos_tag
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from dateutil import parser
import nltk


class TextPreprocessor():

    def __init__(self, tokenizer: Callable = None) -> None:
        self.tokenizer = tokenizer

        if self.tokenizer is None:
            self.tokenizer = tokenize.word_tokenize

        self.stopwords_tokens = stopwords.words('english')
        self.stemmer = PorterStemmer()
        self.lemmatizer = LemmatizerWithPOSTagger()

    def tokenize(self, text: str) -> List[str]:
        tokens = self.tokenizer(text)
        return tokens

    def to_lower(self, tokens: List[str]) -> List[str]:
        lower_tokens = []
        for token in tokens:
            lower_token = str(np.char.lower(token))
            lower_tokens.append(lower_token)
        return lower_tokens

    # Remove the trademark symbol using regular expressions
    def remove_markers(self, tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(re.sub(r'\u00AE', '', token))
        return new_tokens

    def remove_punctuation(self, tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(token.translate(str.maketrans('', '', string.punctuation)))
        return new_tokens

    def correct_sentence_spelling(self, tokens: List[str]) -> List[str]:
        spell = SpellChecker()
        misspelled = spell.unknown(tokens)
        for i, token in enumerate(tokens):
            if token in misspelled:
                corrected = spell.correction(token)
                if (corrected != None):
                    tokens[i] = corrected
        return tokens

    def rplace_under_score_with_space(self, tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(re.sub(r'_', ' ', token))
        return new_tokens

    def remove_stop_words(self, tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            if token not in self.stopwords_tokens and len(token) > 1:
                new_tokens.append(token)
        return new_tokens

    def remove_apostrophe(self, tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(str(np.char.replace(token, "'", " ")))
        return new_tokens

    def stemming(self, tokens: List[str]) -> List[str]:
        new_tokens = []
        for token in tokens:
            new_tokens.append(self.stemmer.stem(token))
        return new_tokens

    def normalize_appreviations(self, tokens: List[str]) -> List[str]:
        new_tokens = []
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
            # self.normalize_date,
            self.to_lower,
            self.remove_punctuation,
            self.remove_apostrophe,
            self.remove_stop_words,
            self.remove_markers,
            # self.correct_sentence_spelling,
            self.stemming,
            self.lemmatizing,
            self.normalize_appreviations,
            self.to_lower,
            self.rplace_under_score_with_space
        ]
        text_tokens = self.tokenize(text)
        for op in operations:
            text_tokens = op(text_tokens)

        new_text = ""
        new_text = ' '.join(text_tokens)

        return new_text


def process_text(document: str):
    return TextPreprocessor().preprocess(document)


process_text('Hello is 12 sxi helllo')

import numpy as np
from nltk.tokenize import word_tokenize


def vectorize(documents):
    documents_vectors = []
    i = 0
    for document in documents:
        zero_vector = np.zeros(500)
        vectors = []
        for token in document:
            if token in model.wv:
                try:
                    vectors.append(model.wv[token])
                except KeyError:
                    vectors.append(np.random(500))
        if vectors:
            vectors = np.asarray(vectors)
            avg_vec = vectors.mean(axis=0)
            documents_vectors.append(avg_vec)
        else:
            documents_vectors.append(zero_vector)
    return documents_vectors


import pickle

# query=vectorize([word_tokenize(process_text('how can we get concentration onsomething?'))])[0]
with open('D:/wikir/word2vec/documents_vectors.pickle', 'rb') as handle:
    documents_vectors = pickle.load(handle)

from gensim.models import Word2Vec

model = Word2Vec.load("D:/wikir/word2vec/model")

from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def vectorize_query(query: str):
    tfidf_model = None
    with open('D:/wikir/tfidf/tfidf_model.pickle', 'rb') as handle:
        tfidf_model = pickle.load(handle)
    return tfidf_model.transform([query]).toarray()[0];


with open('D:/wikir/tfidf/tfidf_matrix.pickle', 'rb') as handle:
    tfidf_matrix = pickle.load(handle)


def get_results(query_fin):
    similarities = cosine_similarity(tfidf_matrix,
                                     vectorize_query(query_fin).reshape(1, -1))

    sorted_indices = similarities.argsort(axis=0)[-10:][::-1].flatten()
    result_ids = []

    for i in sorted_indices:
        if (similarities[i][0] >= 0.35):
            result_ids.append(int(i))

    unordered_results = list(col.find({'index': {'$in': result_ids}}))

    return sorted(unordered_results, key=lambda x: result_ids.index(x['index']))


qrels = {}
with open('D:/wikir/test/qrels', 'r') as f:
    for line in f:
        query_id, _, doc_id, relevance = line.strip().split()
        if query_id not in qrels:
            qrels[query_id] = {}
        qrels[query_id][doc_id] = int(relevance)
# Create a dataset object from the qrels dictionary
from collections import defaultdict

dataset = defaultdict(dict)
for query_id, doc_dict in qrels.items():
    for doc_id, relevance in doc_dict.items():
        dataset[query_id][doc_id] = relevance

print(len(dataset))

import csv


def get_query(query_id):
    with open('D:/wikir/test/queries.csv', newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            if row[0] == query_id:
                return row[1]


def calculate_MAP(query_id):
    relevant_docs = []
    for qrel in dataset.items():
        if qrel[0] == query_id:
            for key, value in qrel[1].items():
                relevant_docs.append(key)

    ordered_results = []
    for query in dataset.items():
        if query[0] == query_id:
            ordered_results = get_results(get_query(query_id))
            break

    pk_sum = 0
    total_relevant = 0
    for i in range(1, 11):
        relevant_ret = 0
        for j in range(i):
            if (j < len(ordered_results) and ordered_results[j]['_id'] in relevant_docs):
                relevant_ret += 1
        p_at_k = (relevant_ret / (i)) * (
            1 if i - 1 < len(ordered_results) and ordered_results[i - 1]['_id'] in relevant_docs else 0)
        pk_sum += p_at_k
        if (i - 1 < len(ordered_results) and ordered_results[i - 1]['_id'] in relevant_docs):
            total_relevant += 1

    return 0 if total_relevant == 0 else pk_sum / total_relevant


# queries_ids = {}
# for qrel in dataset.items():
#     queries_ids.update({qrel[0]: ''})
#
# print(len(queries_ids))
#
# map_sum = 0
# for query_id in list(queries_ids.keys()):
#     map_sum += calculate_MAP(query_id)

# print(len(dataset))
# print(map_sum)
# print(map_sum / len(queries_ids))


def calculate_MRR(query_id):
    relevant_docs = []
    for qrel in dataset.items():
        if qrel[0] == query_id:
            for key, value in qrel[1].items():
                relevant_docs.append(key)

    ordered_results = []
    for query in dataset.items():
        if query[0] == query_id:
            ordered_results = get_results(get_query(query_id))
            break

    for i, result in enumerate(ordered_results):
        if result['_id'] in relevant_docs:
            return 1 / (i + 1)

    return 0


queries_ids = {}
for qrel in dataset.items():
    queries_ids.update({qrel[0]: ''})

mrr_sum = 0
for query_id in list(queries_ids.keys()):
    mrr_sum += calculate_MRR(query_id)

print(mrr_sum / len(dataset))
