import csv
from utils.files_handling.files_locations import FilesLocations
from utils.db.db_init import get_mongo_client


class DatasetLoader:

    def load_dataset(self):
        if FilesLocations.DATASET_NAME.value == "antique":
            return self.load_antique()

        elif FilesLocations.DATASET_NAME.value == "antique_queries":
            return self.load_queries("antique_queries")

        elif FilesLocations.DATASET_NAME.value == "wikir_queries":
            return self.load_queries("wikir_queries")

        return self.load_wikir()

    @staticmethod
    def load_antique():
        documents = {}

        with open(FilesLocations.ANTIQUE_DOCUMENTS.value, encoding="utf-8") as documents_file:
            documents_reader = csv.reader(documents_file, delimiter="\t")
            for doc_id, doc_content in documents_reader:
                documents.update({doc_id: doc_content})

        return documents

    @staticmethod
    def load_wikir():
        documents = {}
        i = 0
        with open(FilesLocations.WIKIR_DOCUMENTS.value, encoding="utf-8") as documents_file:
            documents_reader = csv.reader(documents_file)
            for doc_id, doc_content in documents_reader:
                if i == 0:
                    i += 1
                    continue
                documents.update({doc_id: doc_content})

        return documents

    @staticmethod
    def load_queries(collection):
        col = get_mongo_client()["IR"][collection]
        documents = {}

        for query in list(col.find({})):
            documents.update({query['_id']: query['content']})

        return documents
