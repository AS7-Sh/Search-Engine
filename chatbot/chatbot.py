# This is a sample Python script.
import csv

from bson import ObjectId
from chatterbot.storage import MongoDatabaseAdapter
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot, comparisons, response_selection, logic
import pymongo

from pymongo import MongoClient
from fastapi import FastAPI
import ir_datasets

dataset = ir_datasets.load("antique/test")
client = MongoClient("localhost:27017")
db = client["IR"]
col = db["antique"]
app = FastAPI()
bot = ChatBot('Houmam')

# Press the green button in the gutter to run the script.
conversation = []

trainer = ListTrainer(bot)


def train_antique():
    for query in dataset.queries_iter():
        query_text = query.text
        query_id = query.query_id
        results = []
        for qrel in dataset.qrels_iter():
            if qrel[0] == query_id:
                result = col.find_one({'_id': qrel[1]})['content']
                results.append(result)
        conversation.append({'q': query_text, 'a': results})


final_list = []


def trainthebot():
    print(len(conversation))
    # print(conversation)
    for i, pair in enumerate(conversation):
        final_list.append(pair['q'])
        for ans in pair['a']:
            final_list.append(ans)
            trainer.train([pair['q'], ans])
        print(">>>>>>>>>>>")


# def trainthebotcorpus():
#     with open('C:/Users/msi/.ir_datasets/antique/collection.tsv', 'r') as tsvfile:
#         reader = csv.reader(tsvfile, delimiter='\t')
#         documents = [row[1] for row in reader]
#     trainer = ListTrainer(bot)
#     trainer.train(documents)

def test_chat(question):
    print(bot.get_response(question))


def load_bot():
    trainer.train("export.yml")


# train_antique()
# trainthebot()

# trainer.train(
#     "chatterbot.corpus.english"
# )
# trainthebotcorpus()


#
#
# load_bot()
trainer = ChatterBotCorpusTrainer(bot)


test_chat("why people go church on Easter")
# trainer.export_for_training('./export.yml')
