import json
import random
import sys
import io


def counter():
    print(config[config_type][i]['title'])
    print(config[config_type][i]['start'])
    print(config[config_type][i]['stop'])
    print(config[config_type][i]['step'])
    print(config[config_type][i]['width'])
    print(config[config_type][i]['leading_zero'])
    print(config[config_type][i]['enabled'])
    print('--------------')
    start = config[config_type][i]['start']
    stop = config[config_type][i]['stop']
    step = config[config_type][i]['step']
    width = config[config_type][i]['width']
    column =[]
    counter = config[config_type][i]['start']
    for n in range(config['rows']):
        if config[config_type][i]['leading_zero']:
            string = str(counter).zfill(width)
        else:
            string = str(counter)

        column.append(str(string))

        counter = counter + step
        if counter > stop and step > 0:
            counter = start
        if counter < stop and step < 0:
            counter = start
    return column


def random_string():
    print(config[config_type][i]['title'])
    print(config[config_type][i]['width'])
    print(config[config_type][i]['character_set'])
    print(config[config_type][i]['enabled'])
    print('--------------')
    width = config[config_type][i]['width']
    column = []
    for n in range(config['rows']):
        string = ''
        for o in range(width):
            string = string + random.choice(config[config_type][i]['character_set'])

        column.append(string)
    return column


def random_word():
    print(config[config_type][i]['title'])
    print(config[config_type][i]['word_list'])
    print(config[config_type][i]['enabled'])
    print('--------------')
    column = []
    for n in range(config['rows']):
        random_word = random.choice(config[config_type][i]['word_list'])
        column.append(random_word)
    return column


def word_cycle():
    print(config[config_type][i]['title'])
    print(config[config_type][i]['word_list'])
    print(config[config_type][i]['enabled'])
    print('--------------')
    words = len(config[config_type][i]['word_list'])
    column = (config[config_type][i]['word_list'] * (config['rows'] // words + 1))[:config['rows']]
    return column


if len(sys.argv) == 1:
    print('Es muss ein Dateiname als einziger Parameter übergeben werden')
    print('z.B.: CSV-Generator.exe d:\\test.py.json')
    print()
    input('ENTER zum beenden')
    sys.exit()

with open(sys.argv[1],'r') as file:
    config = json.load(file)

config_types = ['counter', 'random_string', 'random_word', "word_cycle"]
columns = {}
column_names = []

for config_type in config_types:
    print('###############################')
    print('# ' + config_type + ': ', end='')
    print(len(config[config_type]))
    print('###############################')

    for i in range(len(config[config_type])):
        if config[config_type][i]['enabled']:
            columns_name = config[config_type][i]['title']
            column_names.append(columns_name)
            columns[columns_name] = globals()[config_type]()
            print('Result: ', end='')
            print(columns[columns_name])
            print()
            print()

    print()

print(column_names)
for name in column_names:
    print(columns[name])

with open(config['filename'], "w") as csv_file:
    for column in column_names:
        csv_file.write(column + ";")
    csv_file.write('\n')
    for i in range(config['rows']):
        for column in column_names:
            csv_file.write(columns[column][i] + ";")
        csv_file.write('\n')

