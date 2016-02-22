# -*- coding: utf-8 -*-
from telegram import Updater
import json
import urllib2
import random

def getMedia():
	while True:
		number = random.randint(1, 3000)
		data = json.load(urllib2.urlopen('http://api.oboobs.ru/boobs/%s/1/rank/' % number))
		if len(data) > 0:
			preview = data[0]["preview"]
			media = 'http://media.oboobs.ru/%s' % preview
			print(media)
			return media

def echo(bot, update):
	media = getMedia()
	bot.sendMessage(chat_id=update.message.chat_id, text='Лови, бро!')
	bot.sendPhoto(chat_id=update.message.chat_id, photo=media)

def main():
	random.seed(None)
	updater = Updater(token='<YOUR_TOKEN>')
	dispatcher = updater.dispatcher
	dispatcher.addTelegramMessageHandler(echo)
	dispatcher.addTelegramCommandHandler('boobs', echo)
	updater.start_polling()

if __name__ == "__main__":
	main()
	