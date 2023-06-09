from utils.files_handling.files_handler import FilesHandler
from utils.files_handling.files_locations import FilesLocations
import numpy as np


class QueryRepresentation:
    @staticmethod
    def tfidf_vectorize_query(query, dataset):
        if dataset == "antique":
            tfidf_model_location = FilesLocations.ANTIQUE_TFIDF_MODEL.value
        elif dataset == "antique_queries":
            tfidf_model_location = FilesLocations.ANTIQUE_QUERIES_MODEL.value
        elif dataset == "wikir_queries":
            tfidf_model_location = FilesLocations.WIKIR_QUERIES_MODEL.value
        else:
            tfidf_model_location = FilesLocations.WIKIR_TFIDF_MODEL.value

        model = FilesHandler.load_file(tfidf_model_location)
        return model.transform([query]).toarray()[0]

    @staticmethod
    def word_embedding_vectorize_query(query, dataset):
        if dataset == "antique":
            word_embedding_model_location = FilesLocations.ANTIQUE_WORD_EMBEDDING_MODEL.value
        else:
            word_embedding_model_location = FilesLocations.WIKIR_WORD_EMBEDDING_MODEL.value

        model = FilesHandler.load_word_embedding_model(word_embedding_model_location)

        vectors = []
        zero_vector = np.zeros(500)
        for token in query:
            if token in model.wv:
                try:
                    vectors.append(model.wv[token])
                except KeyError:
                    vectors.append(np.random(500))
        if vectors:
            vectors = np.asarray(vectors)
            query_vector = vectors.mean(axis=0)
        else:
            query_vector = zero_vector

        return query_vector
