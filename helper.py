# %conda activate base
import os
import json
import re
from typing import Dict, List
# %pip install -U sentence-transformers
# %pip install scipy
# %pip install joblib
import scipy
import pymongo
import sys
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
from joblib import dump, load
from dotenv import dotenv_values
PASSWORD="PASSWORD"
SECRET="SECRET"
DB_NAME="DB_NAME"
COLLECTION = "COLLECTION"
DOCUMENT = "DOCUMENT"
PASSWORD = "PASSWORD"
SECRET = "SECRET"
DB_NAME = "DB_NAME"
COLLECTION = "COLLECTION"
DOCUMENT = "DOCUMENT"
ROOT_PROJECT_DIR = "ROOT_PROJECT_DIR"
config = dotenv_values("D:/C/py/tez/.env")
print(config)
sys.path.append(config[ROOT_PROJECT_DIR])
from helper import getIds, getTitlesWithReferences
papers_db = config[DB_NAME] 
client = pymongo.MongoClient(papers_db)
db = client[config[COLLECTION]]
citation = db[config[DOCUMENT]]

def saveToDb(path: str):
    collection = []
    offset = citation.count_documents({})
    with open(path, "r") as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            l = json.loads(l)
            l['ser'] = i + offset
            l.pop('indexed_abstract', None)
            collection.append(l)
            if (i % 10_000 == 0 and i > 1):
                citation.insert_many(collection)
                collection = []

        if len(collection) > 0:
            citation.insert_many(collection)


def getIds(path: str):
    Ids = []
    with open(path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line:
                l = json.loads(line)
                Ids.append(l['id'])
        lines.clear()
    return Ids


def getTitles(path: str):
    sentences = []
    with open(path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line:
                l = json.loads(line)
                sentences.append(re.sub("[\n\r]", "", l["title"]))
        lines.clear()
    return sentences


def getTitlesWithAbstract(path: str):
    sentences = []
    with open(path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line:
                l = json.loads(line)
                sentences.append(
                    re.sub("[\n\r]", "", l["title"] + ' ' + l['abs']))
        lines.clear()
    return sentences


def getTitlesWithReferences(path: str):
    sentences = []
    with open(path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line:
                l = json.loads(line)
                names = ' '.join(str(aa['name']) for aa in l['authors'])
                refs = ' '.join(
                    str(rfs) for rfs in l['references']) if 'references' in l else ''
                sentences.append(
                    re.sub("[\n\r]", "", l["title"] + ' ' + names + ' ' + refs))
        lines.clear()
    return sentences
