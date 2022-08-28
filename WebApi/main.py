from typing import Optional, List
from dataclasses import dataclass
from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from datetime import timedelta
from fastapi_login import LoginManager
from starlette.responses import Response  # type: ignore
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer # type: ignore
from dataclasses_serialization.json import JSONSerializer  # type: ignore
from dataclasses import dataclass
from dataclasses_json import dataclass_json # type: ignore
import json
from joblib import load  # type: ignore
import scipy  # type: ignore
import pymongo  # type: ignore
from dotenv import dotenv_values
import timeit
import typing

PASSWORD="PASSWORD"
SECRET="SECRET"
DB_NAME="DB_NAME"
COLLECTION="COLLECTION"
DOCUMENT="DOCUMENT"
config = dotenv_values(".env")
SECRET = config[PASSWORD]  # type: ignore
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:4200",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# manager = LoginManager(SECRET, token_url='/api/auth/token', use_cookie=True)
manager = LoginManager(SECRET, token_url='/api/auth/token')
fake_db = {'ab@cd.ef': {'username':'ab', 'password': 'abcuiop0'}, 'abc@cd.ef': {'username':'abc', 'password': 'abcuiop0'}}

papers_db = config[DB_NAME] 
client = pymongo.MongoClient(papers_db)
db = client[config[COLLECTION]]
citation = db[config[DOCUMENT]]
search_text = "Lecture Notes in Machine Learning"


@dataclass_json
@dataclass
class Author:
    name: Optional[str] = None
    id: Optional[str] = None
    org: Optional[str] = None


@dataclass_json
@dataclass
class Paper:
    id: Optional[int] = None
    title: Optional[str] = None
    abs: Optional[str] = None
    n_citation: Optional[int] = None
    authors: Optional[List[Author]] = None
    year: Optional[int] = None
    topn_sim: Optional[List[List[float]]] = None
    score: float = 0


@dataclass_json
@dataclass
class Recommendations:
    papers: Optional[List[Paper]]
    
    
def Model():
    ''' # return  SentenceTransformer('paraphrase-MiniLM-L3-v2')
        # return  SentenceTransformer('stsb-mpnet-base-v2')
    '''
    print("reading model")
    return SentenceTransformer('paraphrase-mpnet-base-v2')

def Embedding():
  '''reads the model embeddings from its source'''
  src = 'D:/Models/sentence_embeddings_paraphrase-mpnet.joblib'
  return load(src) 

def db_search(query_filter, scores):
    answers = citation.find(query_filter)
    resp:Recommendations = []
    for index, ans in enumerate(answers):
        if "id" in ans:
            id = str(ans["id"])
            keys = "id", "title", 'abs', 'n_citation', "authors", 'doc_type' 'publisher',  "year", 'topn'
            score = scores[index] if index < len(scores) else 0
            data = {}
            data['score'] = score
            for key in keys:
                if key in ans:
                    data[key] = id if(key == id) else ans[key]

            if(data):
                resp.append(Paper.from_dict(data))
    return resp

async def save_embeddings(query_embeddings):
    '''Todo: extend the existing embeddiing when a new paper gets accepted.'''
    with open("emd", "w+") as emd:
        emd.writelines(str(query_embeddings))


def Rec(queries, model, embedding, offset: int, pageSize: int, background_tasks: BackgroundTasks) -> Recommendations:
    '''
    #  model = Model()
    #  embedding = Embedding()
    '''
    query_embeddings = model.encode(queries)
    background_tasks.add_task(save_embeddings, query_embeddings);
    
    for query, query_embedding in zip(queries, query_embeddings):
      '''
        Todo: filtering responses depending on the query filters given as parameters.
      '''
      distances = scipy.spatial.distance.cdist([query_embedding], embedding, "cosine")[0]
      results = zip(range(len(distances)), distances)
      results = sorted(results, key=lambda x: x[1])  # type: ignore
      search_filter = {}  # type: ignore
      search_filter["$or"] = []
      scores = []
      limit = int(pageSize) if int(pageSize) < len(
          results) else len(results) + 1  # type: ignore
      for idx, distance in results[offset:offset+limit]:  # type: ignore
        scores.append(1 - distance)
        search_filter["$or"].append({"ser":idx})       
     
      resp = db_search(search_filter, scores)
      
      return resp
  

model =  Model()
embedding = Embedding()

@manager.user_loader
def load_user(username: str):
    user = fake_db.get(username)
    return user


@app.post('/api/signup')
def user_signup(email: str, username: str, password: str): 
    fake_db.__setitem__(email, {'username': username, "password": password})
    return fake_db


@app.get("/api/test")
def home():
    return {"Hello": "Welcome to ULURESYS!"}


@app.get("/api/search")
@app.post("/api/search")  # type: ignore
def search(background_tasks: BackgroundTasks, query: str = search_text, offset=0, pageSize=100) -> Recommendations:
    mdl= model # Model()
    embd=  embedding #Embedding()
    queries = [query]
    recs = Rec(queries, mdl, embd, int(offset), int(pageSize), background_tasks) 
    return recs


# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post('/api/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    user = load_user(email) # type: ignore  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    # expires after 15 min
    token = manager.create_access_token(
        data = dict(sub = email)
    )
    
    # expires after 12 hours
    long_token = manager.create_access_token(
        data = dict(sub = email), expires=timedelta(hours=12)
    )
       
    return {'access_token': long_token, 'token_type': 'bearer', "user": user['username']}


@app.get('/api/auth')
def auth(response: Response, user=Depends(manager)):
    token = manager.create_access_token( data=dict(sub=user['username']) )
    manager.set_cookie(response, token)
    
    # return response
    return  {"Hi": user['username']}    #   "Hi" 

class NotAuthenticatedException(Exception):
    pass

# the two mandatory arguments
def exc_handler(request, exc):
    return RedirectResponse(url='/')

manager.not_authenticated_exception = NotAuthenticatedException
#  exception handler for the app instance
app.add_exception_handler(NotAuthenticatedException, exc_handler)
