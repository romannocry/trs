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
from starlette.middleware.cors import CORSMiddleware

router = APIRouter()
templates = Jinja2Templates(directory="ui")
#the ui router has to mimick the react router components

@router.get("/")
async def ui_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/models")
async def ui_models(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/models/create")
async def ui_models_create(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/links/{objectModelId}")
async def ui_links(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/forms/{objectModelId}")
async def ui_forms(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/forms/{objectModelId}/{payload}")
async def ui_forms_payload(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/forms/{objectModelId}/{payload}/{type}")
async def ui_forms_payload_type(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/transactions/{objectModelId}")
async def ui_transactions(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})