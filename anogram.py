import nltk
from streets39 import streets

def isAnagram(str1, str2):
    str1_list = list(str1)
    str1_list.sort()
    str2_list = list(str2)
    str2_list.sort()
    return (str1_list == str2_list)

#print(isAnagram('one',"oen"))
#print(streets[2])
def findStreet(find):
#find = input('какая улица? ')
    for street in streets:
        if isAnagram(find, street):
            print (street)

def clean(text): # Функция убирает знаки припенания и приводит у нижнему регистру
  return ''.join([simbol for simbol in text.lower() if simbol in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '])

def match(example, text):
  return nltk.edit_distance(clean(text), clean(example)) / len(example) < 0.4

def get_intent(text):
    streetList=[]
    for street in streets:
        if match(street.split(' ', 1)[1], text):
            streetList += street
            return streetList
print (get_intent(input("введите улицу ")))

