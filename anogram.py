import nltk
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
        if isAnagram(street.split(' ', 1)[1], text):
            streetList.append(str(street))
    return streetList

print (get_streets(input("введите улицу "))) #вызов функции для тестирования