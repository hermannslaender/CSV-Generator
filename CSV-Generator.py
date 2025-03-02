import csv
import sys
import json
from random import choice


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
    with open('CSV-Generator_config.json') as json_data:
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
        else:
            print('disabled')

        print('column[' + str(column) + '] = ',end='')
        print(columns[column])

    with open(config_general['filename'], "w") as csv_file:
        for i in range(config_general['rows']+1):
            for column in columns:
                csv_file.write(columns[column][i] + ";")
            csv_file.write('\n')


if __name__ == '__main__':
    main()