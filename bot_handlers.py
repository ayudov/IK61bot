import gspread
from bot import bot

#  Подключение Google drive
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('IK-61 data.xlsx').sheet1


#  ----------


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id,
                     "<b>Привіт, тебе вітає телеграм бот групи ІК-61</b>\nБудь-ласка, введи <i>ім'я</i> або "
                     "<i>призвище</i> <b>українською</b> мовою одногрупника про котрого ти хочеш отримати "
                     "інформацію.\n\n<i>Для додаткової інформації відправ команду</i> /help",
                     parse_mode='HTML')


@bot.message_handler(commands=['sites'])
def sen_sites(message):
    bot.send_message(message.from_user.id,
                     "Сайти КПІ:\n\n" +
                     "📅 <a href='http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=2c7c806a-e8c2-4dac-a36e"
                     "-f53c2b9a51f6'>Розклад</a>" +
                     '\n📖 <a href="https://telegra.ph/IK-61-Vol-31-06-08">Довідник IK-61</a>'
                     '\n💻 <a href="http://tc.kpi.ua/uk/">КТК</a>'
                     '\n🏫 <a href="http://kpi.ua/fiot">ФІОТ</a>'
                     '\n🚁 <a href="http://kpi.ua/">КПІ</a>',
                     parse_mode='HTML')


@bot.message_handler(commands=['links'])
def send_links(message):
    bot.send_message(message.from_user.id,
                     '6⃣1⃣ <a href="https://t.me/joinchat/DwX0v1Mt-5QnUkFZBprmNA">ІК-61</a>'
                     '\n⚠ <a href="https://t.me/joinchat/AAAAAE-kIuhUM1q1jqz2fQ">Important & Files IK-6X</a>'
                     '\n👥 <a href="https://t.me/joinchat/AAAAAE-kIuhx0nGWBY8uiQ">IK-6X chat</a>',
                     parse_mode='HTML')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id,
                     '/links - посилання на бесіди та канали\n'
                     '/sites - сайти КПІ\n'
                     '/other - додаткова інформація')


@bot.message_handler(commands=['other'])
def send_other(message):
    bot.send_message(message.from_user.id,
                     'Запитання та побажання писати <a href="https://t.me/AndreyYudov">сюди</a>',
                     parse_mode='HTML')


@bot.message_handler(content_types=["text"])  # Любой текст
def answer_message(message):
    result = sheet.get_all_records()
    send = False

    if len(message.text.split(' ')) > 1:
        bot.send_message(message.from_user.id, "Будь-ласка, введи лише им'я або прізвище")
        send = True
    else:
        for x in result:
            if message.text in x.get('All name').split(' '):
                send = True
                bot.send_message(message.from_user.id,
                                 'Я знайшов ось кого:\n\n' + '<b>ПІБ</b>: ' + str(x.get('All name')) +
                                 '\n<b>Посилання на Телеграм: </b>' + str(x.get('TG')) + '\n<b>e-mail</b>: ' +
                                 str(x.get('e-mail')) + '\n<b>Номер телефону</b>: ' + '0' + str(x.get('tel.')) +
                                 '\n<b>День народження</b>: ' + str(x.get('Birth date')) + '\n<b>Гуртожиток</b>: ' +
                                 str(x.get('info')), parse_mode='HTML')
    if send is False:
        bot.send_message(message.from_user.id, "Нажаль в списку немає такої людини.\nТи впевнений, що все вірно ввів? "
                                               "<b>Українською</b> мовою та з <b>великої</b> літери?)",
                         parse_mode='HTML')


@bot.message_handler(
    content_types=['sticker', 'user', 'chat', 'photo', 'audio', 'document', 'video', 'voice', 'contact', 'location',
                   'venue', 'file'])
def answer_sticker(message):
    bot.send_message(message.chat.id, "Я розумію лише текст(")


if __name__ == '__main__':
    bot.polling(none_stop=True)
