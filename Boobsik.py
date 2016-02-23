# -*- coding: utf-8 -*-
from telegram import Updater
import json
import urllib2
import random
from string import Template

def parseMedia(data):
	preview = data["preview"]
	result = {}
	result["preview"] = 'http://media.oboobs.ru/%s' % preview
	result["model"] = data["model"]
	if result["model"] is None:
		result["model"] = 'Неизвестно'
	result["rank"] = data["rank"]
	return result


def getMedia():
	while True:
		number = random.randint(1, 9000)
		data = json.load(urllib2.urlopen('http://api.oboobs.ru/boobs/get/%s' % number))
		if len(data) > 0:
			result = parseMedia(data[0])
			if result is not None:
				return result

def doSearch(request):
	print(request)
	data = json.load(urllib2.urlopen('http://api.oboobs.ru/boobs/model/%s' % request))
	l = len(data)
	if l > 0:
		number = random.randint(0, l)
		result = parseMedia(data[number])
		return result
	return None

def send(bot, update, media):
	model = media["model"]
	rank = media["rank"]
	message = Template(u'Лови, бро!\nИмя красавицы: $name\nРейтинг: $rank').substitute( name=model, rank=rank )
	bot.sendMessage(chat_id=update.message.chat_id, text=message)
	bot.sendPhoto(chat_id=update.message.chat_id, photo=media["preview"])

def boobs(bot, update):
	media = getMedia()
	print(media)
	send(bot, update, media)

def help(bot, update):
	message = "Документация:\n/boobs - Поднять настроение\n/search - Найти по имени модели"
	bot.sendMessage(chat_id=update.message.chat_id, text=message)

def search(bot, update, args):
	args = ' '.join(args)
	result = doSearch(args)
	print(result)
	if result is None:
		bot.sendMessage(chat_id=update.message.chat_id, text=u'Сорян, бро')
		return
	send(bot, update, result)

def main():
	random.seed(None)
	updater = Updater(token='<YOUR_TOKEN>')
	dispatcher = updater.dispatcher
	dispatcher.addTelegramCommandHandler('boobs', boobs)
	dispatcher.addTelegramCommandHandler('help', help)
	dispatcher.addTelegramCommandHandler('search', search)
	updater.start_polling()

if __name__ == "__main__":
	main()
	