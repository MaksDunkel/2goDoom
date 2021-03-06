import telebot, re, nltk
from t import TOKEN
from streets39 import streets, elements
import subprocess
import os, datetime
import speech_recognition as speech_recog
from requests import get
from bs4 import BeautifulSoup as BS
from dadata import Dadata 

def find_streets(search): #парсинг сайта для получения списка улиц
    a = {'а': '%E0', 'б': '%E1', 'в': '%E2', 'г': '%E3', 'д': '%E4', 'е': '%E5', 'ё': '%B8', 'ж': '%E6', 'з': '%E7',
         'и': '%E8', 'й': '%E9', 'к': '%EA', 'л': '%EB', 'м': '%EC', 'н': '%ED', 'о': '%EE', 'п': '%EF', 'р': '%F0',
         'с': '%F1', 'т': '%F2', 'у': '%F3', 'ф': '%F4', 'х': '%F5', 'ц': '%F6', 'ч': '%F7', 'ш': '%F8', 'щ': '%F9',
         'ъ': '%FA', 'ы': '%FB', 'ь': '%FC', 'э': '%FD', 'ю': '%FE', 'я': '%FF'}
    search = search.lower()
    tbl = search.maketrans(a)
    key = search.translate(tbl)
    href = get(r'https://www.klgd.ru/city/streets/index.php?key=' + key + '&SHOWALL_1=1').text
    soup = BS(href, 'html.parser')
    table = soup.find_all('td')
    result = ''
    for street in table:
        try:
            title = street.find('b').get_text()
            result += title + '\n'
        except:
            pass
    return (result)

def global_streets(glo): # поиск улицы через ДАДАТА
    token = "0dfce3e883b7c40ba607cf4039e17271d53407f3"
    secret = "832eace0bb5f6608d4471c4517de2f066e9bd5f9"
    dadata = Dadata(token, secret)
    city = "Калининград"
    find = "овая"
    result = dadata.suggest("address", f'{city} {glo}', 20)
    ans = ''
    for r in result:
        try:
            title = r['value']
            ans += title + '\n'
        except:
            pass
    return (ans)

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

alfa = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
def alf(qu): # переводит слова в цифры, цыфры в буквы 
  qu=qu.lower()
  q = qu.split()
  ap = ''
  an = ''
  wr = ''
  for l in q:
    if  l.isdigit():
      if int(l) in range(1,34):
        ap += alfa[int(l)-1]
        an += alfa[33-int(l)]
    else:
      n = ''
      w = clean(l)
      for s in w:
        n += ' ' + (str(alfa.index(s)+1))
      wr += w + ':' + n + '\n'   
  ans = ap + '\n' + an +'\n' + wr
  return(ans)

def mendeleev(qu):  #ищет элементы в таблице менделеева
    nums = ''
    names = ''
    rus = ''
    qu=qu.lower()
    qu=qu.split()
    for q in qu:
        if q[0] in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            for el in elements:
                if el['ru'].lower() == str(q):
                    nums += el['num']
                    names += el['name']
                    rus += el['ru']
            nums += ' '
            names += ' '
            rus += ' '
        elif q[0] in 'abcdefghijklmnopqrstuvwxyz':
            for el in elements:
                if el['name'].lower() == str(q):
                    nums += el['num']
                    names += el['name']
                    rus += el['ru']
            nums += ' '
            names += ' '
            rus += ' '
        elif q[0] in '123456789':
            for el in elements:
                if el['num'].lower() == str(q):
                    nums += el['num']
                    names += el['name']
                    rus += el['ru']
            nums += ' '
            names += ' '
            rus += ' '
    ans = nums + '\n' + names + '\n' + rus
    return(ans)

def speach_code():
  ans = ''
  src_filename = 'audio_2021.ogg'
  dest_filename = 'output.wav'
  if os.path.exists('output.wav'):
      os.remove('output.wav')
  #os.remove('/content/output.wav')
  process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
  if process.returncode != 0:
      raise Exception("Something went wrong")
#вариант конвертации который не работает с голосовыми телеграмма
#data, samplerate = sf.read('/content/audio_2021.ogg')
#sf.write('/content/audio_2021.wav', data, samplerate)
  sample_audio = speech_recog.AudioFile('output.wav')
  with sample_audio as audio_file:
    recog=speech_recog.Recognizer()
    #recog.adjust_for_ambient_noise(audio_file) #удаление шума для улучшения качества
    audio_content = recog.record(audio_file)
  try:
    ans = recog.recognize_google(audio_content, language="ru-RU")
  except Exception as e:
    print ("Error: " + str(e))
  return(ans)

bot = telebot.TeleBot(TOKEN)

print('стартанул наверное')

@bot.message_handler(commands=['help'])
def start_message(message):
    help_message = """Для получения геолокации отправьте кординаты 
в формате 54.хххх 20,2222 (точка или запятая)
------------
введите: алф 1 2 3 получите буквы 
по номерам с начала и с конца
если ввести слово - результат обратный
------------
для поиска улицы или её анаграмы введите:
ищем "искомаяУлица" (без кавычек)

для глобального поиска улиц введите:
глоб "искомаяУлица" (без кавычек)
------------
для поиска элементов таблицы Менделеева 
введите элементы через пробел:
менд 12 Br хром, ответ:  
12 35 24
Mg Br Cr
Магний Бром Хром
------------
Голосовые сообщения, переводятся в текст"""

    bot.send_message(message.chat.id, help_message)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
  #bot.send_message(message.chat.id, 'распознал команду') #убрать в продакшене
  #print(message.voice)
  file_info = bot.get_file(message.voice.file_id)
  #file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
  file = bot.download_file(file_info.file_path)
  if os.path.exists('audio_2021.ogg'):
      os.remove('audio_2021.ogg')
  with open('audio_2021.ogg', 'wb') as new_file:
      new_file.write(file)
  mess = speach_code()
  if os.path.exists('output.wav'):
      os.remove('output.wav')
  if os.path.exists('audio_2021.ogg'):
      os.remove('audio_2021.ogg')
  bot.reply_to(message, mess)
  mess = mess.replace(' ', '')
  if mess[0] in '0123456789':
      bot.send_message(message.chat.id, f'{mess}')

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

    # вызов анагроматора улиц
    elif message.text.split(' ',1)[0] == 'ищем' or message.text.split(' ',1)[0] == 'Ищем':
        ans = ''
        for street in get_streets(message.text.split(' ', 1)[1]):
            ans += str(street) + '\n'
        if ans != '':
            bot.send_message(message.chat.id, ans)
        else:
            bot.send_message(message.chat.id, "анаграмма улицы не найдена")
        bot.send_message(message.chat.id, "\n-список улиц, содержащих: "+message.text.split(' ', 1)[1]+'\n'+find_streets(message.text.split(' ', 1)[1]))
    
    #вызов поиска через дадата
    elif message.text.split(' ',1)[0] == 'глоб' or message.text.split(' ',1)[0] == 'Глоб':
        bot.send_message(message.chat.id, "\n-список улиц, содержащих: "+message.text.split(' ', 1)[1]+'\n'+global_streets(message.text.split(' ', 1)[1]))

        
    #вызов функции поиска по таблице менделеева
    elif message.text.split(' ', 1)[0] == 'менд' or message.text.split(' ', 1)[0] == 'Менд':
        bot.send_message(message.chat.id, mendeleev(message.text.split(' ', 1)[1]))

    #вызов алфавита по номерам
    elif message.text.split(' ', 1)[0] == 'алф' or message.text.split(' ', 1)[0] == 'Алф':
        bot.send_message(message.chat.id, alf(message.text.split(' ', 1)[1]))

    #обратный отсчет до определенной даты
    elif message.text.split(' ', 1)[0] == 'when' or message.text.split(' ', 1)[0] == 'When':
        now = datetime.datetime.now()
        then = datetime.datetime(2021, 8, 11, 9, 10, 00)
        # Кол-во времени между датами.
        delta = then - now
        h = delta.seconds // 3600 #час
        m = (delta.seconds - (h*3600)) // 60
        #print(h, m)
        bot.send_message(message.chat.id, f'до встречи осталось: \n days: {delta.days} \n hours: {h} \n min: {m}')
bot.polling(none_stop=True)
