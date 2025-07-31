import os
from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import StreamingResponse

from fastapi.middleware.cors import CORSMiddleware
from asyncio import sleep
import copy

import json
import requests

import hashlib

from secAlg import getSecret

import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

global wingRequests
wingRequests = {}

def get_hash(string:str):
    return hashlib.sha256(string.encode("utf-8")).hexdigest()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def event_generator():
    while True:
        yield 'data: {"type": "heartbeat"}\n\n'
        await sleep(3)  # Send heartbeat every 3 seconds

@app.get('/stream')
async def message_stream():
    return EventSourceResponse(event_generator())

async def check_ip(request: Request):
    client_host = request.client.host
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        client_ip = forwarded_for.split(',')[0].strip()
    else:
        client_ip = client_host
    return client_ip


initial_values = "0 0"
with open('curState.txt', 'r') as file:
    content = file.read()
    initial_values = content
#
#
async def get_secret(request: Request):
    return await request.json()#


@app.post("/queueNotification")
async def update_values(request: Request):

    body = await request.json()
    orderString = body['order']
    parts = orderString.split(' ')

    if len(parts) != 2:
        return
    chatID, orderNumber = parts


    body = await get_secret(request)
    secret = body['crypt']

    msg_secret = getSecret([str(chatID),str(orderNumber)])


    if secret != msg_secret:
        print("Incorrect secret")
        return {"message": "Incorrect secret"}
  
    orderNumber = orderNumber.strip()
    if not orderNumber.isnumeric():
        return

    orderNumber = int(orderNumber)
    if orderNumber >= 100:
        return {"message": "Faulty number", "order_value": orderNumber}

    if orderNumber not in wingRequests:
        wingRequests[orderNumber]=[]

    wingRequests[orderNumber].append(chatID)

    return {"message": "Chat Id received", "order_value": orderNumber}

@app.post("/add")
async def update_values(request: Request, text: str):

    body = await get_secret(request)
    secret = body['crypt']
    global initial_values
    if len(text)> 0:
        text = "".join(char for char in text if char.isalnum() or char == " ")
        if len(text) < 1000000000000:
            test = text.split(' ')
            if len(test) == 2:
                msg_secret = getSecret([test[0],test[1]])
                if secret == msg_secret:

                    new = test[0]
                    curVals = initial_values.split(' ')
                    old = curVals[0]

                    processQue(old,new)

                    initial_values = text
                    with open("curState.txt", "wt") as f:
                        f.write(f"{initial_values}")
                    return {"message": "Numbers updated", "current_values": initial_values}
                else:
                    return {f"Invalid request"}

def processQue(old, new):
    Bot_Token = os.environ.get('BOT_TOKEN')
    token = Bot_Token
    old = int(old)
    new = int(new)
    if old > new:
        new = 100 + new

    logger.debug(f'Processing the thing from {old} to {new}')
    logger.debug(f'all orders in system: {wingRequests.keys()}')
    for curNum in range(old,new+1):
        queNum = curNum % 100

        if queNum in wingRequests.keys():
            for chatterID in wingRequests[queNum]:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                text = f'Your order ({queNum}) is ready for pickup!'
                params = {"chat_id": chatterID, "text": text}
                response = requests.post(url, data=params)
            wingRequests[queNum] = []


@app.get("/")
async def read_root(request: Request):
   return {initial_values}
