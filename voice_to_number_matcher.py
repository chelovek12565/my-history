import json
from os import listdir
from colorama import Fore, init


init(autoreset=True)

with open('data/match.json', 'rt') as match_file:
    matched = json.loads(match_file.read())

while True:
    print('Введите имя mp-3 файла, 0 - конец ввода')
    name = input()
    if name == '0':
        break
    try:
        print('Введите название выставки:')
        exhibit = input()
        print('Введите номер:')
        n = input()
        if exhibit not in matched.keys():
            matched[exhibit] = {}
        if n in matched[exhibit].keys():
            print(Fore.RED + 'Такой номер уже существует!')
        if name not in listdir('data'):
            raise FileNotFoundError
        matched[exhibit][n] = name
    except FileNotFoundError:
        print(Fore.RED + 'Файл не найден в папке data!')


with open('data/match.json', 'wt') as match_file:
    match_file.write(json.dumps(matched))