# This is a sample Python script.
import csv

from bson import ObjectId
from chatterbot.storage import MongoDatabaseAdapter
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot, comparisons, response_selection, logic
import pymongo
from pydantic import BaseModel

from pymongo import MongoClient
from fastapi import FastAPI
import ir_datasets

dataset = ir_datasets.load("antique/test")
client = MongoClient("localhost:27017")
db = client["IR"]
antique_col = db["antique"]
wikir_col = db["wikir"]
app = FastAPI()
bot = ChatBot('Houmam',
              storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
              read_only=True,
              logic_adapters=[
                  {
                      'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                      'input_text': 'empty',
                      'output_text': ''
                  },
                  {
                      'import_path': 'chatterbot.logic.BestMatch',
                      'default_response': 'i honestly have no idea how to respond to that',
                      "statement_comparison_function": comparisons.SpacySimilarity,
                      "response_selection_method": response_selection.get_most_frequent_response,
                      'maximum_similarity_threshold': 0.85
                  },
              ]
              )


trainer = ListTrainer(bot)

# Press the green button in the gutter to run the script.
conversation = []


class QueryBot(BaseModel):
    msg: str

@router.post("/chat")
async def search(body: QueryBot):

    return {'search_results': test_chat(body.msg)}

def train_antique():
    for query in dataset.queries_iter():
        query_text = query.text
        query_id = query.query_id
        results = []
        conv = []
        for i, qrel in enumerate(dataset.qrels_iter()):
            if qrel[0] == query_id:
                result = antique_col.find_one({'_id': qrel[1]})['content']
                results.append(result)
                conv.append({'q': query_text, 'a': result})
            conversation.append({'q': query_text, 'a': results})
            for c in conv:
                conversation.append(c)


final_list = []


def trainthebot():
    print(len(conversation))
    # print(conversation)
    for i, pair in enumerate(conversation):
        final_list.append(pair['q'])
        if not isinstance(pair['a'],list):
            trainer.train([pair['q'], pair['a']])
        else:
            for i, ans in enumerate(pair['a']):
                final_list.append(ans)
                trainer.train([pair['q'], ans])




def test_chat(question):
    print(bot.get_response(question))


def load_bot():
    trainer.train("export.yml")


def train():
    train_antique()
    train_wikir()
    trainthebot()
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train(
        "chatterbot.corpus.english"
    )
    trainer.export_for_training('./export.yml')


def get_wikir_query(query_id):
    with open('D:/wikir/test/queries.csv', newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            if row[0] == query_id:
                return row[1]

def train_wikir():
    qrels = {}
    with open('D:/wikir/test/qrels', 'r') as f:
        for line in f:
            query_id, _, doc_id, relevance = line.strip().split()
            if query_id not in qrels:
                qrels[query_id] = {}
            qrels[query_id][doc_id] = int(relevance)
    # Create a dataset object from the qrels dictionary
    from collections import defaultdict
    dataset = defaultdict(dict)
    for query_id, doc_dict in qrels.items():
        for doc_id, relevance in doc_dict.items():
            dataset[query_id][doc_id] = relevance

    queries_ids = {}
    last_id = '0'
    results = []
    conv  = []
    for qrel in dataset.items():
        results = []
        for doc in qrel[1]:
            result = wikir_col.find_one({'_id': doc})['content']
            results.append(result)
            conv.append({'q': get_wikir_query(qrel[0]), 'a': result})
        conversation.append({'q': get_wikir_query(qrel[0]), 'a': results})
        for c in conv:
            conversation.append(c)
        conv = []
