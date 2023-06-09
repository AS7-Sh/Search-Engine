from word_embedding_engine import WordEmbeddingEngine
from services.text_processing.data_preprocessing import TextPreprocessor

WordEmbeddingEngine(500, 1, 4, 35, TextPreprocessor().preprocess, TextPreprocessor().tokenize).train_model()
