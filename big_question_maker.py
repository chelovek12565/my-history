import json
from colorama import init, Fore

init(autoreset=True)
print('Редактор вопросов.')
print('Файл вопроса по умолчанию - questions.json. Это верно? Y/n')
answer = input()
if answer.lower() == 'y':
    file = open('quizes/questions.json', 'rt')
    file_name = 'quizes/questions.json'
else:
    while True:
            file_name = input("Введите имя json-файла: ")
            answer = input("Файл введён верно?(Y/n):")
            if answer.lower() == 'y':
                try:
                    file = open(file_name, 'rt')
                    break
                except FileNotFoundError:
                    print(Fore.RED + 'Ошибка', end = ': ')
                    print('файл не найден')
                    continue
            else:
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
        text = []
        while True:
            print('Вводите варианты ответа, 0 - конец ввода')
            question = input()
            if question == '0':
                break
            else:
                text.append(question)
        print('Введите номер ответа:')
        n = int(input())
        while n > len(text):
            print('Слишком большое число, попробуйте снова')
            print('Введите номер ответа:')
            n = int(input())

        data.([name, n, text])
    # elif answer == '2':
file.close()
with open(file_name, 'wt') as file:
    file.write(json.dumps(data))
