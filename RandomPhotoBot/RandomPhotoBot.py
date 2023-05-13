import requests
import random
import telebot
from telebot import types
from aiogram.types.message import ContentTypes
import time
from datetime import datetime

token="5704107941:AAFiD8e97KhWdZD5d4SwCsPzyuygqY6SV8E"
https="https://api.telegram.org/bot{0}".format(token)
bot = telebot.TeleBot(token)

print("Запуск")

global posts, videoPosts, canSendFoto, canSendVideo
file = open("countPostsVideo.txt","r")
videoPosts = int(file.read())
file.close()
file = open("countPosts.txt","r")
posts = file.read()
file.close()
canSendFoto = False
canSendVideo = False

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Случайное фото")
btn2 = types.KeyboardButton("Загрузить фото")
btn3 = types.KeyboardButton("Случайное видео")
btn4 = types.KeyboardButton("Загрузить видео")
markup.add(btn1,btn2,btn3,btn4)

def sendPayment(userId):
    bot.send_message(userId, "Поддержи бота! Сделай вклад в его улучшение! https://my.qiwi.com/Enryke-VIHiGDGElf")

def waitPay(userId, billid, sekretKey, message):
    zaprosURL = "https://api.qiwi.com/partner/bill/v1/bills/" + billid
    count = 0
    while True:
        time.sleep(10)
        count += 1
        if(count == 50):
            break
        zapros = requests.get(zaprosURL,headers = {"Authorization":"Bearer " + sekretKey,"Accept":"application/json"}).json()
        if(zapros['status']['value'] == "WAITING"):
            print(str(userId) + " оплачивает подписку, ждем...")
        elif(zapros['status']['value'] == "PAID"):
            print(str(userId) + " оплатил счет!")
            PayResult(message)
      	

def CheckSubscriber(id):
    file = open("Subscribers.txt","r")
    count = 0
    otherUsername = []
    for line in file:
        line = line.replace("\n","")
        line = line.split(" ")
        if(line[0] == id):
            count += 1
            date = int(line[1])
        elif(line[0] != id):
            otherUsername.append(line)
        elif(line[0] == "446111281"):
            return True
    file.close()
    CurrentTime = round(time.time())
    if(count != 0 and CurrentTime >= date):
        file = open("Subscribers.txt","w")
        for line in otherUsername:
            file.write(line[0] + " " + line[1] + "\n")
        file.close()
        return False
    elif(count != 0 and CurrentTime < date):
        return True
    elif(count == 0):
        return False

def CheckBlackList(username):
    file = open("BlackList.txt","r")
    count = 0
    for line in file:
        line = line.replace("\n","")
        if(line == username):
            count += 1
        else:
            None
    file.close()
    if(count != 0):
        return True
    else:
        return False

def sendPhoto(message,posts,canSendFoto):
    try:
        PostId = int(random.randint(12,int(posts)))
        curTime = time.time()
        curTime = time.gmtime(curTime + (60*60*3))
        curTime = time.strftime("%H:%M:%S",curTime)
        print(str(message.from_user.username) + " (" + str(message.from_user.id) + ")-"+str(curTime)+"//ID фото-поста - " + str(PostId) + ", последний ID - " + str(posts))
        bot.copy_message(userId, "@RandomFotoChannel", PostId, "")
        canSendFoto = False
    except:
        sendPhoto(message,posts,canSendFoto)

def sendVideo(message,videoPosts,canSendVideo):
    try:
        PostId = random.randint(2,videoPosts)
        curTime = time.time()
        curTime = time.gmtime(curTime + (60*60*3))
        curTime = time.strftime("%H:%M:%S",curTime)
        print(str(message.from_user.username) + " (" + str(message.from_user.id) + ")-"+str(curTime)+"//ID видео-поста - " + str(PostId) + ", последний ID - " + str(videoPosts))
        bot.copy_message(userId, "@RandomniyVidoeChannel", PostId, "")
        canSendVideo = False
    except:
        sendVideo(message,videoPosts,canSendVideo)

@bot.message_handler(commands=["start"])
def HelloMess(message):
    global userId,UserName,canSendFoto, canSendVideo
    canSendFoto = False
    canSendVideo = False
    UserName = "@" + str(message.from_user.username)
    file = open("UsersNames.txt","r")
    count = 0
    for line in file:
        line = line.replace("\n","")
        if(line == UserName):
            count += 1
    file.close()
    if(count == 0):
        file = open("UsersNames.txt","a")
        file.write(UserName+"\n")
    file.close()
    userId = message.from_user.id
    bot.send_message(userId,"Привет, " + message.from_user.first_name)
    bot.send_message(message.chat.id,text = "Жми на кнопку чтобы увидеть рандомную фотку или загрузить свою!", reply_markup=markup)

@bot.message_handler()
def Listen(message):
    global userId,canSendFoto, canSendVideo
    userId = message.from_user.id
    resultBlacklistCheck = CheckBlackList(message.from_user.username)
    if(resultBlacklistCheck == True):
        bot.send_message(userId,"вы забанены(")
    elif(resultBlacklistCheck == False):
        if(message.text == "Случайное фото"):
            chanceToAdd = int(random.randint(0,10))
            if (chanceToAdd >= 8) :
                sendPayment(userId)
            sendPhoto(message,posts,canSendFoto)
        elif(message.text == "Загрузить фото"):
            canSendFoto = True
            bot.send_message(userId,"Тогда отправь мне фото")
        elif(message.text == "Случайное видео"):
            sub = CheckSubscriber(str(message.from_user.id))
            sub = True #удалить если введу подписку
            if(sub == True):
                chanceToAdd = int(random.randint(0,10))
                if (chanceToAdd >= 8) :
                    sendPayment(userId)
                sendVideo(message,videoPosts,canSendVideo)
            else:
                bot.send_message(userId,"Время вашей подписки вышло или вы не были подписаны ранее")
                Submarkup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton("Да")
                btn2 = types.KeyboardButton("Нет")
                Submarkup.add(btn1,btn2)
                bot.send_message(userId,message.from_user.first_name+", для просмотра видео тебе необходимо оформить подписку.\nПодписка стоит 70 рублей в месяц, после чего ее снова потребуется продлить. Возврат средств за оформление подписки не проводится.\nНу так что, хочешь?", reply_markup=Submarkup)
        elif(message.text == "Загрузить видео"):
            canSendVideo = True
            bot.send_message(userId,"Тогда отправь мне видео")
        elif(message.text == "Да"):
            Submarkup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton("Qiwi")
            btn3 = types.KeyboardButton("Я передумал")
            Submarkup2.add(btn2,btn3)
            bot.send_message(userId,"Оплата через Qiwi дослупна со всех российских карт", reply_markup=Submarkup2)
        elif(message.text == "Нет" or message.text == "Я передумал"):
            bot.send_message(userId,"Как хочешь, " + message.from_user.first_name + ")", reply_markup=markup)
        elif(message.text == "Qiwi"):
            billid = random.randint(100, 10000000)
            sekretKey = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjRuNmFycy0wMCIsInVzZXJfaWQiOiI3OTY3MTAxOTM2MSIsInNlY3JldCI6ImIwOWJlOTQ5ODE2NGYyYTI0Yzg3NTEyODUzYmNkMzVjZDUwZjkzNjZjNmI1NTA5ZjgxZDM0NmZmMGY2MjJhNzMifX0="
            zaprosURL = "https://api.qiwi.com/partner/bill/v1/bills/" + str(billid)
            curTime = time.time()
            tomorrowTime = curTime + (60*5)
            tomorrowTime = time.gmtime(tomorrowTime)
            tomorrowTime = time.strftime("%Y-%m-%dT%H:%M:%S+03:00",tomorrowTime)
            zapros = requests.put(zaprosURL, json = {"amount":{"value":"70.00","currency":"RUB"},"expirationDateTime":tomorrowTime,"customFields":{"themeCode":"Enryke-VIHiGDGElf","tgID":userId}},headers = {"Authorization":"Bearer " + sekretKey,"Content-Type":"application/json","Accept":"application/json"}).json()
            bot.send_message(userId,"Отлично! Перейди по ссылке ниже и оплати")
            bot.send_message(userId,zapros['payUrl'])
            waitPay(userId, str(billid),sekretKey, message)


@bot.message_handler(content_types=['photo'])
def saveFoto(message):
    global posts, canSendFoto
    print(str(message.from_user.username)+"//Состояние в saveFoto - " + str(canSendFoto))
    userId = message.from_user.id
    if(canSendFoto == True):
        posts = int(posts)
        posts += 1
        zapros = requests.post(https+"/CopyMessage",data={'chat_id':"@RandomFotoChannel",'from_chat_id':userId,'message_id':message.message_id,"caption":str(posts)}).json()
        file = open("countPosts.txt","w")
        file.write(str(posts))
        file.close()
        canSendFoto = False
        bot.send_message(userId,"Спасибо за пополнение коллекции бота!")
    elif(canSendFoto == False):
        bot.send_message(userId,"Сначала нажми на кнопку 'Загрузить свою фотку'")

@bot.message_handler(content_types=['video'])
def saveVideo(message):
    global videoPosts, canSendVideo
    print(str(message.from_user.username)+"//Состояние в saveVideo - " + str(canSendVideo))
    userId = message.from_user.id
    if(canSendVideo == True):
        videoPosts = videoPosts
        videoPosts += 1
        zapros = requests.post(https+"/CopyMessage",data={'chat_id':"@RandomniyVidoeChannel",'from_chat_id':userId,'message_id':message.message_id,"caption":str(videoPosts)}).json()
        file = open("countPostsVideo.txt","w")
        file.write(str(videoPosts))
        file.close()
        canSendVideo = False
        bot.send_message(userId,"Спасибо за пополнение коллекции бота!")
    elif(canSendVideo == False):
        bot.send_message(userId,"Сначала нажми на кнопку 'Загрузить свою фотку'")

def PayResult(message):
    month = [31,28,31,30,31,30,31,31,30,31,30,31]
    secInDay = 60*60*24
    CurrentTime = time.localtime(time.time())
    InMonth = round(time.time() + secInDay * month[CurrentTime.tm_mon])
    subscriberId = message.from_user.id
    file = open("Subscribers.txt","a")
    file.write(str(subscriberId) + " " + str(InMonth) + "\n")
    file.close()
    bot.send_message(subscriberId, "Поздравляю," + message.from_user.username + ", вы оформили подписку на месяц для возможности просматривать рандомные видео, спасибо что поддержал разработчика!)",reply_markup=markup)

print("Запущено")
bot.infinity_polling()