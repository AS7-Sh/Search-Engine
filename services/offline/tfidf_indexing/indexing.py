from tfidf_engine import TfidfEngine
from services.text_processing.data_preprocessing import TextPreprocessor

TfidfEngine(TextPreprocessor().preprocess, TextPreprocessor().tokenize).train_model()
