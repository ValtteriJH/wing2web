import os
import telebot as tele
import requests
#from asyncio import sleep
from  time import sleep

import pycurl
from io import StringIO

from secAlg import getSecret

Bot_Token = os.environ.get('BOT_TOKEN')

bot = tele.TeleBot(Bot_Token)

number = 0

orderList = {}

from telebot import types

readyToOrder = {}

markup = types.ReplyKeyboardRemove(selective=False)


@bot.message_handler(commands=['start','hello'])
def send_welcome(message):

    bot.reply_to(message,"Howdy, how are you doing?",reply_markup=markup)


@bot.message_handler(commands=['queue', 'Queue', 'que', 'Que'])
def send_queue_status(message):
    response = requests.get('https://api.swider.dev')

    body = response.text
    body = body[1:-2]
    body = body.replace("\"", "")
    body = body.split(" ")

    bot.reply_to(message,f"Order number: {body[0]}, Wait time: {body[1]}")


@bot.message_handler(commands=['cancel','Cancel'])
def send_queue_status(message):

    chatId = message.from_user.id
    if " " not in message.text:
        readyToOrder[chatId] = False
        bot.reply_to(message,f"Placing order cancelled")


@bot.message_handler(commands=['myWings','mywings'])
def send_queue_status(message):

    chatId = message.from_user.id
    if " " not in message.text:
        readyToOrder[chatId] = True
        bot.reply_to(message,f"What's your order number?")




def handle_messages(messages):
    for message in messages:
        chatId = message.from_user.id
        msg = message.text

        if chatId in readyToOrder:
            if readyToOrder[chatId]:
                if msg.strip().isnumeric():
                    order = int(msg)
                    if order > 100:
                        bot.reply_to(message,f"invalid que number")
                        return

                else:
                    bot.reply_to(message,f"invalid queue number (/cancel to not change queue number)")
                    return

                readyToOrder[chatId] = False
                orderList[chatId] = order
                
                a = str(chatId)
                b = str(order)
                
                secret = getSecret([a,b])
                
                response = requests.post(
                    url=f'https://api.swider.dev/queueNotification',
                    json={'order': f'{chatId} {order}',
                          'crypt': secret
                    }
                )
                bot.reply_to(message,f"🔥 I have received your order: {message.from_user.username} = {order} 🔥 You will receice a DM after your order is done 😎")

    

bot.set_update_listener(handle_messages)

bot.infinity_polling()
