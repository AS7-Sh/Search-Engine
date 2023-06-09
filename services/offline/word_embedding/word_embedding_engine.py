from gensim.models import Word2Vec
from utils.dataset.dataset_loader import DatasetLoader
import numpy as np
from utils.files_handling.files_handler import FilesHandler


class WordEmbeddingEngine:
    def __init__(self, vector_size, sg, workers, epochs, text_processor, text_tokenizer):
        self.vector_size = vector_size
        self.sg = sg
        self.workers = workers
        self.epochs = epochs
        self.text_processor = text_processor
        self.text_tokenizer = text_tokenizer
        self.word_embedding_model = None
        self.documents_vectors = None

    def init_sentences(self):
        sentences = []
        documents = DatasetLoader().load_dataset()
        for document in documents.values():
            sentences.append(
                self.text_tokenizer(self.text_processor(document))
            )

        return sentences

    def train_model(self):
        sentences = self.init_sentences()
        model = Word2Vec(sentences,
                         vector_size=self.vector_size,
                         sg=self.sg,
                         workers=self.workers,
                         epochs=self.epochs)

        self.word_embedding_model = model
        self.documents_vectors = self.vectorize_documents(sentences)
        self.save_model()

    def vectorize_documents(self, sentences):
        documents_vectors = []
        for sentence in sentences:
            zero_vector = np.zeros(self.vector_size)
            vectors = []
            for token in sentence:
                if token in self.word_embedding_model.wv:
                    try:
                        vectors.append(self.word_embedding_model.wv[token])
                    except KeyError:
                        vectors.append(np.random(self.vector_size))
            if vectors:
                vectors = np.asarray(vectors)
                avg_vec = vectors.mean(axis=0)
                documents_vectors.append(avg_vec)
            else:
                documents_vectors.append(zero_vector)
        return documents_vectors

    def save_model(self):
        FilesHandler().save_word_embedding_data(self.documents_vectors, self.word_embedding_model)
