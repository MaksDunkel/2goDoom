import telebot, re
from t import TOKEN
bot = telebot.TeleBot(TOKEN)
#
# patern = r'54.(.+?)'
# string = input ("input kord: ")
# result = re.match (patern, string)
#
#     print (latitude, longitude)
print('стартанул наверное')
@bot.message_handler(content_types=["text"])
def loco(message):
    patern = r'54.(.+?)'
    result = re.match (patern, message.text)
    if result != None:
        latitude = message.text[:message.text.find(" ")]
        longitude = message.text[message.text.find(" ") + 1:]
        bot.send_location(message.chat.id, latitude, longitude)
        # bot.send_message(message.chat.id, result)
bot.polling(none_stop=True)
