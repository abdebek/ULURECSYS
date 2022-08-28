from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from datetime import timedelta
from fastapi_login import LoginManager
from starlette.responses import Response
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from joblib import load
import scipy
import pymongo
from dotenv import dotenv_values
import timeit

PASSWORD = "PASSWORD"
SECRET = "SECRET"
DB_NAME = "DB_NAME"
COLLECTION = "COLLECTION"
DOCUMENT = "DOCUMENT"
config = dotenv_values(".env")
SECRET = config[PASSWORD]
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# manager = LoginManager(SECRET, token_url='/auth/token', use_cookie=True)
manager = LoginManager(SECRET, token_url='/auth/token')
fake_db = {'ab@cd.ef': {'username': 'ab', 'password': 'abcuiop0'},
           'abc@cd.ef': {'username': 'abc', 'password': 'abcuiop0'}}

papers_db = config[DB_NAME]
client = pymongo.MongoClient(papers_db)
db = client[config[COLLECTION]]
citation = db[config[DOCUMENT]]


def Model():
    ''' # return  SentenceTransformer('paraphrase-MiniLM-L3-v2')'''
    print("reading model")
    return SentenceTransformer('stsb-mpnet-base-v2')


def Embedding():
  '''reads the model embeddings from its source   D:/C/py/tez/ulurecsys_back/Data/sentence_emb_paraphr-MiniLM-L3v2.joblib'''
  src = 'D:/Models/sentence_embeddings_paraphrase-mpnet.joblib'
  return load(src)


def db_search(query_filter):
    answers = citation.find(query_filter)
    resp = []
    for ans in answers:
        if "id" in ans:
            i = str(ans["id"])
            keys = "id", "title", 'abs', 'n_citation', "authors", 'doc_type' 'publisher',  "year", 'topn_sim'
            data = {}
            for key in keys:
                if key in ans:
                    data[key] = i if(key == i) else ans[key]

            if(data):
                resp.append(data)
    return resp


async def save_embeddings(query_embeddings):
    '''Todo: extend the existing embeddiing when a new paper gets accepted.'''
    with open("emd", "w+") as emd:
        emd.writelines(str(query_embeddings))


def Rec(queries, model, embedding, number_top_matches, background_tasks):
    '''
    #  model = Model()
    #  embedding = Embedding()
    '''
    query_embeddings = model.encode(queries)
    background_tasks: BackgroundTasks
    background_tasks.add_task(save_embeddings, query_embeddings)

    for query, query_embedding in zip(queries, query_embeddings):
      '''
        Todo: filtering responses depending on the query filters given as parameters.
      '''
      distances = scipy.spatial.distance.cdist(
          [query_embedding], embedding, "cosine")[0]
      results = zip(range(len(distances)), distances)
      results = sorted(results, key=lambda x: x[1])
      search_filter = {}
      search_filter["$or"] = []
      for idx, distance in results[0:number_top_matches]:
        search_filter["$or"].append({"ser": idx})

      resp = db_search(search_filter)

      return resp


model = Model()
embedding = Embedding()


@manager.user_loader
def load_user(username: str):
    user = fake_db.get(username)
    return user


@app.post('/signup')
def user_signup(email: str, username: str, password: str):
    fake_db.__setitem__(email, {'username': username, "password": password})
    return fake_db


@app.get("/api/test")
def home():
    return {"Hello": "Welcome to ULURESYS!"}


@app.get("/search")
def search(background_tasks: BackgroundTasks, query='A Parallel and Secure Architecture for Asymmetric Cryptography'):
    mdl = model  # Model()
    embd = embedding  # Embedding()
    number_top_matches = 100
    queries = [query]
    recs = Rec(queries, mdl, embd, number_top_matches, background_tasks)
    return recs


@app.post("/search")
def search(background_tasks: BackgroundTasks, query: str = 'A Parallel and Secure Architecture for Asymmetric Cryptography'):
    mdl = model  # Model()
    embd = embedding  # Embedding()
    number_top_matches = 100
    queries = [query]
    recs = Rec(queries, mdl, embd, number_top_matches, background_tasks)
    return recs


# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    # we are using the same function to retrieve the user
    user = load_user(email)
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    # expires after 15 min
    token = manager.create_access_token(
        data=dict(sub=email)
    )

    # expires after 12 hours
    long_token = manager.create_access_token(
        data=dict(sub=email), expires=timedelta(hours=12)
    )

    return {'access_token': long_token, 'token_type': 'bearer', "user": user['username']}


@app.get('/auth')
def auth(response: Response, user=Depends(manager)):
    token = manager.create_access_token(data=dict(sub=user['username']))
    manager.set_cookie(response, token)

    # return response
    return {"Hi": user['username']}  # "Hi"


class NotAuthenticatedException(Exception):
    pass

# the two mandatory arguments


def exc_handler(request, exc):
    return RedirectResponse(url='/')


manager.not_authenticated_exception = NotAuthenticatedException
#  exception handler for the app instance
app.add_exception_handler(NotAuthenticatedException, exc_handler)
