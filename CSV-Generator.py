import csv
import sys
import json
from random import choice

def create_sample():
    with open('sample_config.json', "w") as sample_file:
        sample_file.write('''{
    "general": {
        "rows": 15,
        "filename": "demo.csv"
        },
    "columns": [
        {
            "type": "counter",
            "title": "Counter 0",
            "start": 1,
            "stop": 99,
            "step": 1,
            "width": 4,
            "leading_zero": true,
            "enabled": true
        },
        {
            "type": "random_string",
            "title": "Random String 0",
            "length": 12,
            "character_set": "abcdefghijklmnopqrstuvwxyz",
            "enabled": true
        },
        {
            "type": "random_word",
            "title": "Random Word 0",
            "word_list": ["Merkur", "Venus", "Erde", "Mars", "Jupiter", "Saturn", "Uranus", "Neptun", "Pluto"],
            "enabled": true
        },
        {
            "type": "word_cycle",
            "title": "Word Cycle 0",
            "word_list": ["Januar", "Februar", "März", "Aril", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
            "enabled": true
        }
    ]
}
''')


def counter(config_rows, item):
    column = [item['title']]
    counter = item['start']
    for _ in range(config_rows):
        if item['leading_zero']:
            string = str(counter).zfill(item['width'])
        else:
            string = str(counter)

        column.append(string)

        counter = counter + item['step']
        if counter > item['stop'] and item['step'] > 0:
            counter = item['start']
        if counter < item['stop'] and item['step'] < 0:
            counter = item['start']
    return column


def random_string(config_rows, item):
    column = [item['title']]
    for _ in range(config_rows):
        string = ''
        for _ in range(item['length']):
            string = string + choice(item['character_set'])
        column.append(string)
    return column


def random_word(config_rows, item):
    column = [item['title']]
    for _ in range(config_rows):
        column.append(choice(item['word_list']))

    return column


def word_cycle(config_rows, item):
    column = [item['title']]
    column = column + (item['word_list']*(config_rows // len(item['word_list']) + 1))[:config_rows]
    return column


def main():
    if len(sys.argv) == 1:
        print('Es muss ein Dateiname als einziger Parameter übergeben werden.')
        print('z.B.: CSV-Generator.exe d:\\CSV-Generator_config.json')
        print()
        create_sample()
        print('Eine neue Vorlage wurde erstellt.')
        print()
        input('ENTER zum beenden')
        sys.exit()

    #with open('Briefmarken.json') as json_data:
    with open(sys.argv[1]) as json_data:
        config = json.load(json_data)

    config_general = config['general']
    print(f'{config_general = }')
    config_columns = config['columns']
    print(f'{config_columns = }')

    config_rows = config_general['rows']
    print(f'{config_rows = }')
    config_file = config_general['filename']
    print(f'{config_file = }')

    columns = {}
    for column in range(len(config_columns)):
        item = config_columns[column]
        print('############################\n### ' + item['type'])
        print(f'{item = }')

        if item['enabled']:
            match config_columns[column]['type']:
                case 'counter':
                    columns[column] = counter(config_rows, item)
                case 'random_string':
                    columns[column] = random_string(config_rows, item)
                case 'random_word':
                    columns[column] = random_word(config_rows, item)
                case 'word_cycle':
                    columns[column] = word_cycle(config_rows, item)
                case _:
                    print('Fehler')

            print('column[' + str(column) + '] = ',end='')
            print(columns[column])

        else:
            print('disabled')


    with open(config_general['filename'], "w") as csv_file:
        for i in range(config_general['rows']+1): #erste Reihe enthält den Titel
            for column in columns:
                csv_file.write(columns[column][i] + ";")
            csv_file.write('\n')


try:

    if __name__ == '__main__':
        main()

except Exception as e:
    print('Ein Fehler ist aufgetreten:')
    print({e})
    print()
    create_sample()
    print('Eine neue Vorlage wurde erstellt.')
    print()
    input('ENTER zum beenden')
