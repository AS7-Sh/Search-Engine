import pickle
import os
from utils.files_handling.files_locations import FilesLocations
from gensim.models import Word2Vec


class FilesHandler:

    @staticmethod
    def save_file(file_location: str, content):
        if os.path.exists(file_location):
            os.remove(file_location)
        with open(file_location, 'wb') as handle:
            pickle.dump(content, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_file(file_location: str):
        with open(file_location, 'rb') as handle:
            content = pickle.load(handle)
        return content

    def save_tfidf_data(self, tfidf_matrix, tfidf_model):
        if FilesLocations.DATASET_NAME.value == "antique":
            self.save_file(FilesLocations.ANTIQUE_TFIDF_MATRIX.value, tfidf_matrix)
            self.save_file(FilesLocations.ANTIQUE_TFIDF_MODEL.value, tfidf_model)

        elif FilesLocations.DATASET_NAME.value == "antique_queries":
            self.save_file(FilesLocations.ANTIQUE_TFIDF_QUERIES.value, tfidf_matrix)
            self.save_file(FilesLocations.ANTIQUE_QUERIES_MODEL.value, tfidf_model)

        elif FilesLocations.DATASET_NAME.value == "wikir_queries":
            self.save_file(FilesLocations.WIKIR_TFIDF_QUERIES.value, tfidf_matrix)
            self.save_file(FilesLocations.WIKIR_QUERIES_MODEL.value, tfidf_model)

        else:
            self.save_file(FilesLocations.WIKIR_TFIDF_MATRIX.value, tfidf_matrix)
            self.save_file(FilesLocations.WIKIR_TFIDF_MODEL.value, tfidf_model)

    def save_word_embedding_data(self, documents_vectors, word_embedding_mode):
        if FilesLocations.DATASET_NAME.value == "antique":
            self.save_file(FilesLocations.ANTIQUE_VECTORS.value, documents_vectors)
            word_embedding_mode.save(FilesLocations.ANTIQUE_WORD_EMBEDDING_MODEL.value)

        else:
            self.save_file(FilesLocations.WIKIR_VECTORS.value, documents_vectors)
            word_embedding_mode.save(FilesLocations.WIKIR_WORD_EMBEDDING_MODEL.value)

    @staticmethod
    def load_word_embedding_model(file_location: str):
        return Word2Vec.load(file_location)
