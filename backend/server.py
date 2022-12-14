from asyncio.windows_events import NULL
import multiprocessing
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
from pymongo import MongoClient
from bson.objectid import ObjectId
import uvicorn
import base64
import json
import random
import logging, platform
import time
import io
from starlette.responses import StreamingResponse
import socket
from starlette.middleware.cors import CORSMiddleware
from enum import Enum
from datetime import date,datetime,timedelta
from enum import Enum
from fastapi.responses import JSONResponse
import bson
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response
from unicornException import UnicornException
from bson import json_util
from collections.abc import MutableMapping
from multiprocessing import cpu_count, freeze_support
from app.routers import models
from app.routers import transactions
from app.routers import ui
from app.check.checkModel import dict_compare,flatten_dict
from app.db.db import db_url
from fastapi.security import OAuth2PasswordBearer




app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    
    start_time = time.time()
    #time.sleep(5)
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.include_router(ui.router)
app.include_router(models.router)
app.include_router(transactions.router)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    uvicorn.run("server:app", host="0.0.0.0", port=8000, log_level="info",reload="true")
    
#def start_server(host="127.0.0.1",port=8000):
#    uvicorn.run("server:app",
#                host=host,
#                port=port
#                )

#if __name__ == "__main__":
#    freeze_support()  # Needed for pyinstaller for multiprocessing on WindowsOS
    #num_workers = int(cpu_count() * 0.75)
    #start_server()
#    uvicorn.run("server:app", host="127.0.0.1", port=8000, log_level="info")


app.mount("/", StaticFiles(directory="ui", html=True), name="static")

templates = Jinja2Templates(directory="ui")

# Setting up connection with MongoDB
client = MongoClient(db_url)
database = client["feedbackLoop"]
inputModel = database["inputObjectModel"] 
inputTransaction = database["inputTransaction"] 

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=500,
        content={"message": f"Oops! {exc.name} did something: {exc.label}"},
    )

