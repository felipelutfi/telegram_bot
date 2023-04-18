import telepot
import time
from telethon import TelegramClient
import random
import pandas as pd
import requests
import shutil

from telegram.ext.commandhandler import CommandHandler
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot

token = 'BOT_TOKEN'
receiver_id_group = TELEGRAM_GROUP_ID
receiver_id_me = PERSONAL_TELEGRAM_ID

bot = telepot.Bot(token) 

updater = Updater(token, use_context=True)

dispatcher: Dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext):
    """
    the callback for handling start command
    """
   
    bot: Bot = context.bot


    bot.send_message(chat_id=update.effective_chat.id,
                     text="E aí boca de pelo?")

def facts(update: Update, context: CallbackContext):
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': 'API_KEY'})
    if response.status_code == requests.codes.ok:
        spaces = len(response.text)
        bot: Bot = context.bot
        bot.send_message(chat_id=update.effective_chat.id, text=response.text[11:spaces - 3])
    else:
        print("Error:", response.status_code, response.text)


def image(update: Update, context: CallbackContext):
   category = ''
   api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
   response = requests.get(api_url, headers={'X-Api-Key': 'API_KEY', 'Accept': 'image/jpg'}, stream=True)
   if response.status_code == requests.codes.ok:
     with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        bot.sendPhoto(chat_id=update.effective_chat.id, photo=open('img.jpg', 'rb'))
   else:
        print("Error:", response.status_code, response.text)

dispatcher.add_handler(CommandHandler("start", start))

dispatcher.add_handler(CommandHandler("facts", facts))

dispatcher.add_handler(CommandHandler("image", image))

updater.start_polling()
