from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import uvicorn

from asyncio import sleep

import copy
import json
import requests
import hashlib

from secAlg import getSecret 


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

@app.post("/add")
async def update_values(request: Request, text: str):

    body = await get_secret(request)
    secret = body['crypt']
    global initial_values
    if len(text)> 0:
        text = "".join(char for char in text if char.isalnum() or char == " ")
        if len(text) < 1000000000000:
            targets = text.split(' ')

            if len(targets) == 2:
                key = targets[0] + targets[1] + 2*targets[0] + 2*targets[1]
                msg_secret = getSecret(targets)

                if secret == msg_secret:
                    initial_values = text
                    with open("curState.txt", "wt") as f:
                        f.write(f"{initial_values}")

                    #giveNumber()
                    return {"message": "Numbers updated", "current_values": initial_values}
                else:
                    return {f"Invalid request"}

@app.get("/get-numbers")
async def root():
    return StreamingResponse(giveNumber(), media_type="text/event-stream")

async def giveNumber():
#    myCurrentState = copy.copy(initial_values) Add data to a heartbeat. 
    while True:
        yield f"event: locationUpdate\ndata: {initial_values}\n\n"
        await sleep(2)
#        if (myCurrentState != initial_values):
        #myCurrentState = copy.copy(initial_values)

@app.get("/")
async def read_root(request: Request):
   return {initial_values}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


