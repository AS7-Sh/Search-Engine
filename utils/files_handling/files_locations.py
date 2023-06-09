from enum import Enum


class FilesLocations(Enum):
    DATASET_NAME = "wikir_queries"

    ANTIQUE_DOCUMENTS = 'D:/antique/collection.tsv'
    ANTIQUE_TFIDF_MATRIX = 'D:/antique/tfidf/tfidf_matrix.pickle'
    ANTIQUE_TFIDF_MODEL = 'D:/antique/tfidf/tfidf_model.pickle'
    ANTIQUE_VECTORS = "D:/antique/word2vec/documents_vectors.pickle"
    ANTIQUE_WORD_EMBEDDING_MODEL = "D:/antique/word2vec/model"
    ANTIQUE_TFIDF_QUERIES = "D:/antique/queries/tfidf_matrix.pickle"
    ANTIQUE_QUERIES_MODEL = "D:/antique/queries/tfidf_model.pickle"

    WIKIR_DOCUMENTS = 'D:/wikir/documents.csv'
    WIKIR_TFIDF_MATRIX = 'D:/wikir/tfidf/tfidf_matrix.pickle'
    WIKIR_TFIDF_MODEL = 'D:/wikir/tfidf/tfidf_model.pickle'
    WIKIR_VECTORS = "D:/wikir/word2vec/documents_vectors.pickle"
    WIKIR_WORD_EMBEDDING_MODEL = "D:/wikir/word2vec/model"
    WIKIR_TFIDF_QUERIES = "D:/wikir/queries/tfidf_matrix.pickle"
    WIKIR_QUERIES_MODEL = "D:/wikir/queries/tfidf_model.pickle"
