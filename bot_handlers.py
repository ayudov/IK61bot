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
    bot.send_message(message.chat.id, "<b>Привіт, тебе вітає телеграм бот групи ІК-61</b>\nБудь-ласка, введи <i>ім'я</i> або <i>призвище</i> <b>українською</b> мовою одногрупника про котрого ти хочеш отримати інформацію", parse_mode='HTML')

@bot.message_handler(commands=['help'])    
def send_help(messsage):
    bot.send_message(message.chat.id, "Ось тобі вся основна інформація:\n", parse_mode='HTML')
    
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
                bot.send_message(message.chat.id, "Я знайшов ось кого:\n\n"+'<b>ПІБ</b>: '+'\n<b>Посилання на Телеграм: </b>'+str(x.get('TG'))+str(x.get('All name'))+'\n<b>e-mail</b>: '+str(x.get('e-mail'))+'\n<b>Номер телефону</b>: '+'0'+str(x.get('tel.'))+'\n<b>День народження</b>: '+str(x.get('Birth date'))+'\n<b>Гуртожиток</b>: '+str(x.get('info')), parse_mode='HTML')
    if send == False:
        bot.send_message(message.chat.id, "Нажаль в списку немає такої людини, ти впевнений, що все вірно ввів?")
    #for x in result:
    
   # if "status - " in message.text:
    #    #if len(input_text_array) >=4 or len(input_text_array) <3:
     #   if len(input_text_array) != 3:
    #        send_array.append("Пожалуйста, используйте верный формат запроса")
    #    elif re.search('\D', input_text_array[2]):
    #        send_array.append("Пожалуйста, номер заказа, который состоит только из цифр")
#			#bot.send_message(message.chat.id, "Пожалуйста, номер заказа, который состоит только из цифр")
#       else:
 #           for x  in result:
  #              if x.get('pyxis_order_uid') == int(input_text_array[2]):
   #                 send = True
	#				
     #       if send == False:
     #           send_array.append("К сожалению, такого кода товара нет")

    #else:
    #    send_array.append("Пожалуйста, используйте верный формат запроса")
			
    #send_message(message.chat.id, send_text, send_array) #Отправляем сообщение



if __name__ == '__main__':
    bot.polling(none_stop=True)