import json
from colorama import init, Fore

init(autoreset=True)
print('Редактор вопросов.')
print('Файл вопроса по умолчанию - questions.json. Это верно? Y/n')
answer = input()
if answer.lower() == 'y':
    file = open('questions.json', 'rt')
    file_name = 'questions.json'
else:
    while True:
            file_name = input("Введите имя json-файла: ")
            answer = input("Файл введён верно?(Y/n):")
            if answer.lower('y'):
                break
            else:
                continue
            try:
                file = open(file_name, 'rt')
            except FileNotFoundError:
                print(Fore.RED + 'Ошибка', end = ': ')
                print('файл не найден')
                continue
            
data = []
data.extend(json.loads(file.read()))
while True:
    print("0 - выйти")
    print("1 - новый вопрос")
    print("2 - удалить вопрос")
    answer = input("Введите цифру выбора:")
    if answer == '0':
        print('Выхожу...')
        break
    elif answer == '1':
        print("Введите заголовок вопроса:")
        name = input()
        print("Введите смайлик для вопроса:")
        smile = input()
        print('Введите вопрос:')
        text = input()
        data.append([name, smile, text])
    # elif answer == '2':
file.close()
with open(file_name, 'wt') as file:
    file.write(json.dumps(data))