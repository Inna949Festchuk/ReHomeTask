# -*- coding = utf-8 -*-
__version__ = '1.0.3'

import csv
import re

from itertools import groupby

def fix(in_path:str, out_path:str) -> str:
    ''' Функция редактирования списка контактов
        in_path - путь к входному файлу .csv
        out_path - путь к выходному файлу .csv
    '''

    # Удалить запятые вконце строк
    with open(in_path, 'r') as file:
    # file = open(in_path, 'r')
        text_list = file.read().split('\n')
        fix_text_list = []
        for text_str in text_list:
            el_str  = text_str.strip('')
            fix_text_list.append(el_str.split(','))
        # print(fix_text_list)

    # Отредактировать номер телефона
    i = 0
    for text in fix_text_list:
        pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
        sub_ = r'+7(\2)\3-\4-\5\6\7\8'
        result = list(map(lambda z: re.sub(pattern, sub_, z), text)) # валидация списка
        fix_text_list[i] = result # Замена i-го элемента в списке на валидированный
        i += 1
    # print(fix_text_list)

    out_list = [] # Выходной список для выгрузки в .csv
    list_keys_values = [] # Список [(ключ:значение)] для группировки и сортировки

    # Распределить значения ФИО по полям 'lastname', 'firstname', 'surname'
    dict_keys = fix_text_list[0] # Список ключей
    dict_reader = dict.fromkeys(fix_text_list[0])
    for m in range(1, len(fix_text_list)):
        for dict_key in dict_keys:
            dict_reader.update({dict_key:fix_text_list[m][dict_keys.index(dict_key)]})
        # print(dict_reader)
        for n in range(0,2): # разделяем строку на Ф,И,О
            ii = 0
            contacts = dict_reader.get(dict_keys[n]) # n-ый элемент из строки dict_reader исходного словаря
            # print(contacts)
            split_contacts = contacts.split(' ') # разделдяем n-е элементы
            # print(split_contacts)
            for element_string in split_contacts: # Проходим строку по разделенным элементам
                dict_reader.update({dict_keys[n:][ii]: element_string}) # Добавляем элементы в исходный словарь
                ii += 1
        # print(dict_reader)
        l_s = dict_reader.items() # Получаем пары ключ:значение обработанного исходного словаря
        list_keys_values.append(list(l_s)) # И передаем их в список
    # print(list_keys_values)

    # Группировать и сортировать значения в списке list_keys_values
    # Ключ группировки и сортировки (По фамилии, н-р ('lastname', 'Усольцев')) 
    key = lambda x:x[0][1] 
    # Группировка и сортировка 
    gr = groupby(sorted(list_keys_values, key=key), key=key)
    # Получаем группированные значения
    s = [[i for i in el[1]] for el in gr]
    # Объединяем группы на основе механизма пересечение множеств
    j = 0
    list_or = [] 
    while j < len(s):
        if len(s[j]) != 1:
            list_or.append(set(s[j][0]) | set(s[j][1]))
        else:
            list_or.append(set(s[j][0]))                
        j += 1

    jj = 0
    for out_key in range(0, len(dict_keys) - 1):
        # Создание словаря исходной последовательности ключей
        dict_raw_key = dict.fromkeys(dict_keys)
        # Создание словаря из объединенного списка при условии, что
        # по ключу отсутствует пустое значение
        dict_or = {k:v for (k,v) in list_or[jj] if v != ''}
        # Распределяем хаотичное расположение значений по исходной последовательности ключей
        dict_raw_key.update(dict_or)
        out_list.append(list(dict_raw_key.values())) # Значения преобразованного словаря передаем в выходной список 
        jj += 1
    print(out_list)

    with open(out_path, 'w') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(dict_keys)
        datawriter.writerows(out_list)
        
def main():
    fix('phonebook_raw.csv', 'phonebook.csv')

if __name__ == "__main__":
    main()

