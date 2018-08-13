import telebot
from telebot import types
import gspread
import config
import re
from bot import bot
#import collections

#Подключение Google drive
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('IK-61 data.xlsx').sheet1


#----------


#Настройка бота

#bot = telebot.TeleBot(config.TOKEN)
#print(bot.get_me())

#----------
@bot.message_handler(commands=['start'])  # Выполняется, когда пользователь нажимает на start
def send_welcome(message):
    bot.send_message(message.chat.id, "<b>Привіт, тебе вітає телеграм бот групи ІК-61</b>\nБудь-ласка, введи <i>ім'я</i> або <i>призвище</i> <b>українською</b> мовою одногрупника про котрого ти хочеш отримати інформацію.", parse_mode='HTML')

@bot.message_handler(commands=['help'])    
def send_help(message):
    bot.send_message(message.chat.id,'Это /help')
    bot.send_message(message.chat.id, "Ось тобі деяка основна інформація:\n\n%xF0%x9F%x93%x85<b><a href='http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=2c7c806a-e8c2-4dac-a36e-f53c2b9a51f6'>Розклад</a></b>", parse_mode='HTML')
    
@bot.message_handler(content_types=["text"]) #Любой текст
def answer_message(message):

    result = sheet.get_all_records()
    send = False
    send_array = []
    send_text = ""
	
    input_text_array = message.text.split()
    if len(message.text.split(' ')) > 1:
        bot.send_message(message.chat.id, "Будь-ласка, введи лише им'я або прізвище")
        send = True
    else:
        for x in result:
            if message.text in x.get('All name').split(' '):
                send = True
                bot.send_message(message.chat.id, 'Я знайшов ось кого:\n\n'+'<b>ПІБ</b>: '+str(x.get('All name'))+'\n<b>Посилання на Телеграм: </b>'+str(x.get('TG'))+'\n<b>e-mail</b>: '+str(x.get('e-mail'))+'\n<b>Номер телефону</b>: '+'0'+str(x.get('tel.'))+'\n<b>День народження</b>: '+str(x.get('Birth date'))+'\n<b>Гуртожиток</b>: '+str(x.get('info')), parse_mode='HTML')
    if send == False:
        bot.send_message(message.chat.id, "Нажаль в списку немає такої людини, ти впевнений, що все вірно ввів?")


if __name__ == '__main__':
    bot.polling(none_stop=True)