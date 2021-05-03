import telebot, re, nltk
from t import TOKEN
from streets39 import streets

def isAnagram(str1, str2): #проверяет анограмма и игнорирует опечатки
    str1_list = list(clean(str1))
    str1_list.sort()
    str2_list = list(clean(str2))
    str2_list.sort()
    return (nltk.edit_distance(str1_list, str2_list) / len(str2_list) < 0.35)

def clean(text): # Функция убирает знаки припенания и приводит у нижнему регистру
    return ''.join([simbol for simbol in text.lower() if simbol in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '])

def get_streets(text): #возвращает список улиц, анаграм и похожих
    streetList=[]
    for street in streets:
        for word in street.split():
            if isAnagram(word, text):
                streetList.append(str(street))
    return streetList


bot = telebot.TeleBot(TOKEN)

print('стартанул наверное')

@bot.message_handler(commands=['help'])
def start_message(message):
    help_message = """Для получения геолокации отправьте кординаты 
в формате 54.хххх 20,2222 (точка или запятая)
для поиска анаграмы улицы введите:
анаг "искомаяУлица" (без кавычек)"""

    bot.send_message(message.chat.id, help_message)

#все декораторы что ниже не включаются
@bot.message_handler(content_types=["text"])
def loco(message):
    patern = r'54.(.+?)'
    result = re.match (patern, message.text)
    if result != None:
        latitude = message.text[:message.text.find(" ")]
        longitude = message.text[message.text.find(" ") + 1:]
        bot.send_location(message.chat.id, latitude.replace(',','.'), longitude.replace(',','.'))
        #bot.send_message(message.chat.id, result)
    elif message.text.split(' ',1)[0] == 'анаг' or message.text.split(' ',1)[0] == 'Анаг':
        #bot.send_message(message.chat.id, 'распознал команду')
        ans = ''
        for street in get_streets(message.text.split(' ', 1)[1]):
            ans += str(street) + '\n'
        if ans != '':
            bot.send_message(message.chat.id, ans)
        else:
            bot.send_message(message.chat.id, "улица не найдена")

bot.polling(none_stop=True)