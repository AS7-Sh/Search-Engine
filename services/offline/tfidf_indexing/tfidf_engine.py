from sklearn.feature_extraction.text import TfidfVectorizer
from utils.files_handling.files_handler import FilesHandler
from utils.dataset.dataset_loader import DatasetLoader


class TfidfEngine:
    def __init__(self, text_processor, text_tokenizer):
        self.text_processor = text_processor
        self.text_tokenizer = text_tokenizer
        self.tfidf_matrix = None
        self.tfidf_model = None

    def train_model(self):
        corpus = DatasetLoader().load_dataset()
        documents = list(corpus.values())
        vectorizer = TfidfVectorizer(preprocessor=self.text_processor, tokenizer=self.text_tokenizer)
        tfidf_matrix = vectorizer.fit_transform(documents)
        self.tfidf_matrix = tfidf_matrix
        self.tfidf_model = vectorizer
        self.save_model()

    def save_model(self):
        FilesHandler().save_tfidf_data(self.tfidf_matrix, self.tfidf_model)
