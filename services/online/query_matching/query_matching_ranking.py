from sklearn.metrics.pairwise import cosine_similarity
from utils.db.db_init import get_mongo_client
from utils.files_handling.files_locations import FilesLocations
from utils.files_handling.files_handler import FilesHandler


class QueryMatchingRanking:
    def __init__(self, page, items_per_page, threshold):
        self.page = page
        self.items_per_page = items_per_page
        self.threshold = threshold
        self.start_index = (page - 1) * self.items_per_page
        self.end_index = self.start_index + self.items_per_page

    def get_tfidf_results(self, dataset, query_vector):
        if dataset == "antique":
            tfidf_matrix_location = FilesLocations.ANTIQUE_TFIDF_MATRIX.value
        elif dataset == "antique_queries":
            tfidf_matrix_location = FilesLocations.ANTIQUE_TFIDF_QUERIES.value
        elif dataset == "wikir_queries":
            tfidf_matrix_location = FilesLocations.WIKIR_TFIDF_QUERIES.value
        else:
            tfidf_matrix_location = FilesLocations.WIKIR_TFIDF_MATRIX.value

        tfidf_matrix = FilesHandler.load_file(tfidf_matrix_location)
        similarities = cosine_similarity(tfidf_matrix, query_vector)
        sorted_indices = similarities.argsort(axis=0)[::-1][self.start_index:self.end_index].flatten()

        top_indices = []
        for i in sorted_indices:
            if similarities[i] >= self.threshold:
                top_indices.append(i.item())

        col = get_mongo_client()["IR"][dataset]
        unordered_results = list(col.find({'index': {'$in': top_indices}}))
        return sorted(unordered_results, key=lambda x: top_indices.index(x['index']))

    def get_word_embedding_results(self, dataset, query_vector):
        if dataset == "antique":
            documents_vectors = FilesHandler.load_file(FilesLocations.ANTIQUE_VECTORS.value)
        else:
            documents_vectors = FilesHandler.load_file(FilesLocations.WIKIR_VECTORS.value)
        similarities = cosine_similarity(documents_vectors, query_vector)
        sorted_indices = similarities.argsort(axis=0)[::-1][self.start_index:self.end_index].flatten()
        top_indices = []
        for i in sorted_indices:
            if similarities[i] >= self.threshold:
                top_indices.append(i.item())

        col = get_mongo_client()["IR"][dataset]
        unordered_results = list(col.find({'index': {'$in': top_indices}}))
        return sorted(unordered_results, key=lambda x: top_indices.index(x['index']))
