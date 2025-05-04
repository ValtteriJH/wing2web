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

orderList = {}



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

@bot.message_handler(commands=['myWings', 'munSiibs', 'kerroSikku', 'sayWhen'])
def send_queue_status(message):

    order = message.text.split(" ")

    if len(order) == 2:
        order = order[1]
        chatId = message.from_user.id
#        if chatId not in orderList:
#            orderList[chatId] = order

    secret = "123"
    response = requests.post(
        url=f'https://api.swider.dev/queNotification?text={chatId} {order}',
        json={'crypt': secret
        }
    )
    print(response.content)
    bot.reply_to(message,f"{order}")
#    else:
#        bot.reply_to(message,f"Invalid command")


#@bot.fwdCombo(message)
#def echo_all(message):
#    bot.reply_to(message, f'Order ready!')


@bot.message_handler(func=lambda msg: True)
def echo_all(message):

    logUser(message)
    
    response = requests.get('https://api.swider.dev')

    body = response.text
    body = body[1:-2]
    body = body.replace("\"", "")
    body = body.split(" ")

    #bot.reply_to(message,f"Order number: {body[0]}, Wait time: {body[1]}")
    bot.reply_to(message, message.text)


bot.infinity_polling()
