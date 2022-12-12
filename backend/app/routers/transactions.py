from fastapi import APIRouter
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
import json
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
from app.db.db import db_url
from app.check.checkModel import dict_compare,flatten_dict
from fastapi.templating import Jinja2Templates
from bson.objectid import ObjectId
from unicornException import UnicornException
import bson
import random
import base64
from datetime import date,datetime,timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
templates = Jinja2Templates(directory="dist")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, objectModelId: str):
        for connection in self.active_connections:
            if connection.path_params['objectModelId'] == objectModelId:
                await connection.send_text(message)


manager = ConnectionManager()
loggedInUser = {}
# Setting up connection with MongoDB
client = MongoClient(db_url)
database = client["feedbackLoop"]
inputModel = database["inputObjectModel"] 
inputTransaction = database["inputTransaction"] 

@router.get("/delete/transactions/", tags=["transactions"])
def deleteAll(request: Request):
    inputTransaction.drop()
    return "deleted"

@router.get("/transactions/", tags=["transactions"])
async def read_transactions():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/forms/{objectModelId}/{payload}")
async def launch_app(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/edit/transaction/{objectModelId}/{payload}")
def insertTransactionViaBrowser(objectModelId: str, payload: str, request: Request):
    if bson.objectid.ObjectId.is_valid(objectModelId):
        inputModelQuery = inputModel.find_one({"_id": ObjectId(objectModelId)})
        #inputModelQuery_flattend = flatten_dict(json.loads(json.dumps(inputModelQuery, default=json_util.default)))
        if inputModelQuery is None: 
            raise UnicornException(name=objectModelId,label="ObjectModelId does not exist!")
        else: print(inputModelQuery)
    else: raise UnicornException(name=objectModelId,label="invalid ObjectIdModel, it must be a 12-byte input or a 24-character hex string")
    
    return templates.TemplateResponse("main.html", {"request": request, "objectModelId":objectModelId, "payload":payload, "model":inputModelQuery})

@router.post("/test/api/transaction/{objectModelId}/{payload}")
async def postTransaction(objectModelId: str, payload: str, request: Request):
    inputModelQuery = inputModel.find_one({"_id": ObjectId(objectModelId)})
    payload_base64_decode = base64.b64decode(payload)
    payload_to_dict = json.loads(payload_base64_decode)
    payload = dict_compare(inputModelQuery['object_model'],payload_to_dict)
    return "test"


@router.post("/api/transaction/{objectModelId}/{payload}")
async def postTransaction(objectModelId: str, payload: str, request: Request):
  
    loggedInUser['id']= random.randrange(0, 10)
    loggedInUser['username']=str(loggedInUser['id'])+'_bengi'
    loggedInUser['email']='anemail'
    #get template model but make sure it is a valide object id
    if bson.objectid.ObjectId.is_valid(objectModelId):
        inputModelQuery = inputModel.find_one({"_id": ObjectId(objectModelId)})
        if inputModelQuery is None: raise UnicornException(name=objectModelId,label="ObjectModelId does not exist!")
        else: 
            #The model id exist so we try to decode the payload
            try:    
                payload_base64_decode = base64.b64decode(payload)
                payload_to_dict = json.loads(payload_base64_decode)
            except Exception as e:
                raise UnicornException(name=payload,label="invalid payload, not a b64 string")

            userObj = loggedInUser
            #checking if transaction existing for this object model and user
            transaction = inputTransaction.find_one({"objectModelId":ObjectId(objectModelId),"user.id":loggedInUser['id']})
            if bool(transaction):
                #transaction.pop("_id")
                #transaction.pop("objectModelId")
                #if transaction already exists, the model might allow modification (allow_change) or multiple entries (allow_multiple)
                if inputModelQuery['allow_change']['value']:
                    #check if you are in time for the change
                    if inputModelQuery['allow_change']['before'] > datetime.now():
                        #if we successfully decode the string, we need to make sure it is in the right format
                        print("transaction exists - updating")
                        payload = dict_compare(inputModelQuery['object_model'],payload_to_dict)
                        payload['transaction_modification_date']=datetime.now()
                        #print(payload)
                        #payload = inputTransaction.find_one_and_update({"_id":ObjectId(transaction['_id'])},{"$set":payload},{"returnOriginal": True})
                        payload = inputTransaction.find_one_and_update({"_id":ObjectId(transaction['_id'])},{"$set":payload}, new=True)
                        #print(payload)
                        #print(payload)
                        #print(type(payload))
                        payload_flattend = flatten_dict(json.loads(json.dumps(payload, default=json_util.default)))
                        #print(payload_flattend)

                        #broadcast only to admin users
                        await manager.broadcast(json.dumps(payload_flattend),objectModelId)
                    else: raise UnicornException(name=payload_to_dict,label="transaction was changeable until "+str(inputModelQuery['allow_change']['before']))
                elif inputModelQuery['allow_multiple']['value']:
                    print("we go here")
                    #change might not be allowed but multiple entries might be
                    payload = dict_compare(inputModelQuery['object_model'],payload_to_dict)
                    #add modelId and user info into the payload
                    payload['objectModelId']=inputModelQuery['_id']
                    payload['user']=loggedInUser
                    payload['transaction_creation_date']=datetime.now()
                    payload['transaction_modification_date']=datetime.now()
                    
                    inputTransaction.insert_one(payload)
                    #print(payload)
                    #remove objectIDs after insertion
                    #payload.pop("_id")
                    #payload.pop("objectModelId")
                    payload_flattend = flatten_dict(json.loads(json.dumps(payload, default=json_util.default)))

                    #broadcast only to admin users
                    await manager.broadcast(json.dumps(payload_flattend),objectModelId)
                else:
                    raise UnicornException(name=payload_to_dict,label="transaction already exists and cannot be modified and multiple entries are not allowed: "+str(transaction))
            else:
                #no transaction was ever recorded with the pair modelId/user
                #if we successfully decode the string, we need to make sure it is in the right format
                payload = dict_compare(inputModelQuery['object_model'],payload_to_dict)
                #add modelId and user info into the payload
                payload['objectModelId']=inputModelQuery['_id']
                payload['user']=loggedInUser
                payload['transaction_creation_date']=datetime.now()
                payload['transaction_modification_date']=datetime.now()
                inputTransaction.insert_one(payload)
                #remove objectIDs after insertion
                #payload.pop("_id")
                #payload.pop("objectModelId")
                payload_flattend = flatten_dict(json.loads(json.dumps(payload, default=json_util.default)))

                #broadcast only to admin users
                await manager.broadcast(json.dumps(payload_flattend),objectModelId)
                
    else: raise UnicornException(name=objectModelId,label="invalid ObjectIdModel, it must be a 12-byte input or a 24-character hex string")

    return {"payload": json.dumps(payload, default=json_util.default)}



@router.get("/views/transactions/{objectModelId}")
def getTransactionsList(objectModelId: str, request: Request):
    payload ={}
    data = []
    try:
        query = inputTransaction.find({"objectModelId": ObjectId(objectModelId)})

        for item in list(query):
            #need to dump it to remove non serializible fields
            item_json_dumped = json.dumps(item, default=json_util.default)
            #load it again
            item_json = json.loads(item_json_dumped)
            #flatteb the object
            item_json_flat = flatten_dict(item_json)
            #append to dataset 
            data.append(item_json_flat)

        payload['data']=data
        print(data)
    except Exception as e:
        print("error")
        print(e)    

    return templates.TemplateResponse("transactions.html", {"request": request,"objectModelId":objectModelId, "payload":json.dumps(payload)})

@router.get("/api/transactions/{objectModelId}", tags=["transactions"])
def getTransactions(objectModelId: str, request: Request):
    data = []
    if bson.objectid.ObjectId.is_valid(objectModelId):
        inputTransactionQuery = inputTransaction.find({"objectModelId": ObjectId(objectModelId)})
        for item in list(inputTransactionQuery):
            #need to dump it to remove non serializible fields
            item_json_dumped = json.dumps(item, default=json_util.default)
            #load it again
            item_json = json.loads(item_json_dumped)
            #flatteb the object
            item_json_flat = flatten_dict(item_json)
            #append to dataset 
            data.append(item_json_flat)
        #inputTransactionQuery_flattend = flatten_dict(json.loads(json.dumps(inputTransactionQuery, default=json_util.default)))
        if inputTransactionQuery is None: 
            raise UnicornException(name=objectModelId,label="ObjectModelId does not exist!")
        else: print(inputTransactionQuery)
    else: raise UnicornException(name=objectModelId,label="invalid ObjectIdModel, it must be a 12-byte input or a 24-character hex string")

    return data




#user can get a live feed of the data_stream_id
@router.websocket("/feed/transactions/{objectModelId}")
async def websocket_endpoint(websocket: WebSocket, objectModelId: str):

    payload = {}
    print(websocket)
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            #manager.broadcast(data)
            #print(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        #await manager.broadcast(f"Client #{objectModelId} left the chat")
