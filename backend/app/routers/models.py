from datetime import datetime
from fastapi import APIRouter
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

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
from pydantic import BaseModel
from typing import Union


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

router = APIRouter()
templates = Jinja2Templates(directory="dist")

# Setting up connection with MongoDB
client = MongoClient(db_url)
database = client["feedbackLoop"]
inputModel = database["inputObjectModel"] 
inputTransaction = database["inputTransaction"] 
def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/app", tags=["models"])
async def launch_app(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/api/models", tags=["models"])
#async def read_models(token: str = Depends(oauth2_scheme)):
async def read_models():
    #if bson.objectid.ObjectId.is_valid():
    data = []
    inputModelQuery = inputModel.find({})
    for item in list(inputModelQuery):
        #need to dump it to remove non serializible fields
        item_json_dumped = json.dumps(item, default=json_util.default)
        #load it again
        item_json = json.loads(item_json_dumped)
        #flatteb the object - no need for models
        #item_json_flat = flatten_dict(item_json)
        #append to dataset 
        data.append(item_json)
    return data


@router.get("/api/models/{objectModelId}", tags=["models"])
async def read_model(objectModelId: str, request: Request):
    data = []
    if bson.objectid.ObjectId.is_valid(objectModelId):
        inputModelQuery = inputModel.find_one({"_id": ObjectId(objectModelId)})
        #inputModelQuery_flattend = flatten_dict(json.loads(json.dumps(inputModelQuery, default=json_util.default)))
        if inputModelQuery is None: 
            raise UnicornException(name=objectModelId,label="ObjectModelId does not exist!")
        else: print(inputModelQuery)
    else: raise UnicornException(name=objectModelId,label="invalid ObjectIdModel, it must be a 12-byte input or a 24-character hex string")

    return json.loads(json.dumps(inputModelQuery, default=json_util.default))
    #return inputModelQuery_flattend

class Trs_model(BaseModel):
    object_name: str = None
    object_description: str = None
    object_model: object = None
    allow_change: bool = False
    allow_change_until_date: datetime = None # ISO 8601 format
    allow_multiple: bool = False

@router.post("/api/models", tags=["models"])
def create_model(trs_model: Trs_model):
    print(trs_model)
    _id = inputModel.insert_one({
        'object_creation_date': datetime.now(),
        'object_modification_date': datetime.now(),
        'object_created_by': "Roman",
        'object_modified_by': "Roman",
        'object_name':trs_model.object_name,
        'object_description':trs_model.object_description,
        'object_model':trs_model.object_model,
        'allow_change':{
            'value':trs_model.allow_change,
            'before':trs_model.allow_change_until_date
        },
        'allow_multiple':{
            'value':trs_model.allow_multiple,
       #     'frequency':'daily'
       }
        
        
        }).inserted_id



    return f"Model persisted via get under id: {_id}"
    #return f"Model persisted via get under id: {request}"
    #return f"Model persisted via get under id: {_id}"