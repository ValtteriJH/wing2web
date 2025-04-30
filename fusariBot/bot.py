import os
import telebot
import requests
#from asyncio import sleep
from  time import sleep

import pycurl
from io import StringIO

Bot_Token = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(Bot_Token)

number = 0

#bot.setBotMenuButton(True)

@bot.message_handler(commands=['start','hello'])
def send_welcome(message):
    bot.reply_to(message,"Howdy, how are you doing?")

@bot.message_handler(commands=['queue', 'Queue', 'que', 'Que'])
def send_queue_status(message):
    response = requests.get('https://api.swider.dev')

    body = response.text
    body = body[1:-2]
    body = body.replace("\"", "")
    body = body.split(" ")

    bot.reply_to(message,f"Order number: {body[0]}, Wait time: {body[1]}")
@bot.message_handler(commands=['queue', 'Queue', 'que', 'Que'])
def send_queue_status(message):
    response = requests.get('https://api.swider.dev')

    body = response.text
    body = body[1:-2]
    body = body.replace("\"", "")
    body = body.split(" ")

    bot.reply_to(message,f"Order number: {body[0]}, Wait time: {body[1]}")

@bot.message_handler(commands=['test'])
def send_queue_status(message):

    sleep(5)
    bot.reply_to(message,f"Number is {2}")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# This approach didnt work
#@bot.message_handler(commands=['test'])
#async def send_queue_status(message):
#    rounds = 0
#    while True:
#        response = requests.get('https://api.swider.dev')
#
#        body = response.text
#        body = body[1:-2]
#        body = body.replace("\"", "")
#        body = body.split(" ")
#
#        bot.reply_to(message,f"Order number: {body[0]}, Wait time: {body[1]}")
#
#        await sleep(3)  # Send heartbeat every 3 seconds
#        rounds += 1
#        if rounds > 5:
#            break


#@bot.message_handler(commands=['queue', 'Queue', 'que', 'Que'])
#def send_welcome(message):
#    # Create a Curl object
#    # Perform the request
#    # Retrieve the response
#
#    storage = StringIO()
#    url = 'https://api.swider.dev'
#
#    c = pycurl.Curl()
#    c.setopt(c.URL, url)
#    c.setopt(c.WRITEFUNCTION, storage.write)
#    c.perform()
#
##    response = c.getinfo(pycurl.RESPONSE_CODE)
#
#    c.close()
#    content = storage.getvalue()
#
#    bot.reply_to(message,f"Queue status: {content}")

# This approach didnt work
# async def event_generator(message):
#     rounds = 0
#     print('works')
#     while True:
#         response = requests.get('https://api.swider.dev')
# 
#         body = response.text
#         body = body[1:-2]
#         body = body.replace("\"", "")
#         body = body.split(" ")
# 
#         bot.reply_to(message,f"Order number: {body[0]}, Wait time: {body[1]}")
#         #yield 'data: {"type": "heartbeat"}\n\n'
#         await sleep(3)  # Send heartbeat every 3 seconds
#         rounds += 1
#         print(rounds)
#         if rounds > 3:
#             break
# 
# #@app.get('/stream')
# @bot.message_handler(commands=['test'])
# def message_stream(message):
#     await event_generator(message)

bot.infinity_polling()
