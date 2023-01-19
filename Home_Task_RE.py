__version__ = '1.0.1'

import csv
import re

from itertools import groupby

# читаем адресную книгу в формате csv в список contacts_list
with open('phonebook_raw.csv', 'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    
    i = 0
    for text in contacts_list:
        pattern = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
        sub_ = r'+7(\2)\3-\4-\5\6\7\8'
        result = list(map(lambda z: re.sub(pattern, sub_, z), text)) # валидация списка
        contacts_list[i] = result # Замена i-го элемента в списке на валидированный
        i += 1

with open('phonebook.csv', 'w') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(contacts_list.pop(0)) # хедер
    datawriter.writerows(contacts_list) 

out_list = [] # Выходной список для выгрузки в .csv
list_keys_values = [] # Список ключ:значение для группировки и сортировки

# Распределение значений ФИО по полям 'lastname', 'firstname', 'surname'
with open('phonebook.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    dict_keys = reader.fieldnames # Список ключей
    for row in reader: # получаем строку исходного словаря
        for n in range(0,2): # разделяем строку на Ф,И,О
            i = 0
            contacts = row.get(dict_keys[n]) # n-ый элемент из строки row исходного словаря
            split_contacts = contacts.split() # разделдяем n-е элементы
            for element_string in split_contacts: # Проходим строку по разделенным элементам
                if split_contacts.index(element_string) != '': # Для не отсутствующих индексов получаем индекс элемента
                    row.update({dict_keys[n:][i]: element_string}) # Добавляем элементы в исходный словарь
                    i += 1
                else:
                    continue
        l_s = dict(row).items() # Получаем пары ключ:значение обработанного исходного словаря
        list_keys_values.append(list(l_s)) # И передаем их в список

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
        list_or.append(set((s[j])[0]) | set((s[j])[1]))
    else:
        list_or.append(set((s[j][0])))               
    j += 1

jj = 0
for out_key in range(0, len(dict_keys) - 1):
    # Создание словаря исходной последовательности ключей
    dict_raw_key = dict.fromkeys(dict_keys)
    # Создание словаря из объединенного списка при условии, что
    # по ключу отсутствует пустое значение
    dict_or = {k:v for(k,v) in list_or[jj] if v != ''}
    # Распределяем хаотичное расположение значений по исходной последовательности ключей
    dict_raw_key.update(dict_or)
    out_list.append(list(dict_raw_key.values())) # Значения преобразованного словаря передаем в выходной список 
    jj += 1
print(out_list)

with open('phonebook.csv', 'w') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(reader.fieldnames)
    datawriter.writerows(out_list)


        
   

