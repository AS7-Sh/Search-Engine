## Information Retrieval System
The repository will guide you step by step to create your first basic search engine based on TF-IDF and word embedding techniques

## Used datasets
* Antique
* WikIR EN1K

## Project Services
* Entry point service
* Text preprocessing service
* Query representation service
* Query matching and ranking service

## Flow of control
* The frontend interacts directly with entry point service to get the query results
* The entry point forwards the query to the query representation service
* The representation service requests the text preprocessing service to correct, preprocess and tokenize the query
* The representation service accesses the trained models files to generate the query vector
* The flow returns to the entry point where it forwards the query vector to the matching and ranking service
* The matching service measures the distance between the query vectors and the documents vectors
* The top results are selected as relevant answers for the targeted page
* The matching service queries the indexed MongoDb database to get the documents content
* The documents are sorted based on the Cosine similarity

## How to train the models
By accessing the offline service folder you will find two indexing folders:
* TF-IDF folder to train your model based on TF-IDF technique by using the TfidfVectorizer from Sklearn library
* Word embedding folder to train your model based on Word2Vec from Gensim library
* Change the locations in the FilesLocations class to target your own local files

## Used libraries and packages
* FastApi
* NLTK
* Pandas
* Numpy
* Sklearn
* Gensim
You will find the full list in the requirements file, all you have to do is pip install -r requirements.txt

## Authors
* Abd Alrahman Shebani
* Humam Albazzal
* Marwa Aldaya
* Ghina Sharaf

## Damascus University - IR - 2023 
Graduation Year ..