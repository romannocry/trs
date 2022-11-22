from datetime import datetime
from fastapi import APIRouter
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
import json
from bson import json_util
import bson
from datetime import date,datetime,timedelta
from bson.objectid import ObjectId
from pymongo import MongoClient
from app.db.db import db_url
from app.check.checkModel import dict_compare,flatten_dict
from fastapi.templating import Jinja2Templates
from bson.objectid import ObjectId
from unicornException import UnicornException


router = APIRouter()
templates = Jinja2Templates(directory="static")

# Setting up connection with MongoDB
client = MongoClient(db_url)
database = client["feedbackLoop"]
inputModel = database["inputObjectModel"] 
inputTransaction = database["inputTransaction"] 

@router.get("/api/models", tags=["models"])
async def read_models():
    #if bson.objectid.ObjectId.is_valid():
    data = []
    inputModelQuery = inputModel.find({})
    for item in list(inputModelQuery):
        #need to dump it to remove non serializible fields
        item_json_dumped = json.dumps(item, default=json_util.default)
        #load it again
        item_json = json.loads(item_json_dumped)
        #flatteb the object
        item_json_flat = flatten_dict(item_json)
        #append to dataset 
        data.append(item_json_flat)
    return data

@router.get("/models/{objectModelId}", tags=["models"])
async def read_model(objectModelId: str, request: Request):
    if bson.objectid.ObjectId.is_valid(objectModelId):
        inputModelQuery = inputModel.find_one({"_id": ObjectId(objectModelId)})
        inputModelQuery_flattend = flatten_dict(json.loads(json.dumps(inputModelQuery, default=json_util.default)))
        if inputModelQuery is None: 
            raise UnicornException(name=objectModelId,label="ObjectModelId does not exist!")
        else: print(inputModelQuery)
    else: raise UnicornException(name=objectModelId,label="invalid ObjectIdModel, it must be a 12-byte input or a 24-character hex string")

    return inputModelQuery_flattend


@router.get("/models/{objectModelId}", tags=["models"])
async def read_model(objectModelId: str, request: Request):
    if bson.objectid.ObjectId.is_valid(objectModelId):
        inputModelQuery = inputModel.find_one({"_id": ObjectId(objectModelId)})
        inputModelQuery_flattend = flatten_dict(json.loads(json.dumps(inputModelQuery, default=json_util.default)))
        if inputModelQuery is None: 
            raise UnicornException(name=objectModelId,label="ObjectModelId does not exist!")
        else: print(inputModelQuery)
    else: raise UnicornException(name=objectModelId,label="invalid ObjectIdModel, it must be a 12-byte input or a 24-character hex string")

    return inputModelQuery_flattend


@router.get("/init/models/", tags=["models"])
def insertObjectModelViaGet(request: Request):
    _id = inputModel.insert_one({
        'object_creation_date': datetime.now(),
        'object_modification_date': datetime.now(),
        'object_created_by': "Roman",
        'object_modified_by': "Roman",
        'object_name':'test',
        'object_model':{
            'Roman':{'label':'SMC','values':['IDX','FSI']},
            'price':{'label':'price','values':'int'},
            'rating':{'label':'rating','values':[1,2,3,4,5]},
        },
        'allow_change':{
            'value':True,
            'before':datetime.now()+timedelta(days=1)
        },
        'allow_multiple':{
            'value':False,
            'frequency':'daily'
        }
        
        
        }).inserted_id
    return f"Model persisted via get under id: {_id}"