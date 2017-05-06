# -*- coding: utf-8 -*-

#
# Загрузка базы фирм из excel
#

from mysql.connector import MySQLConnection, Error
from datetime import datetime
import openpyxl
from openpyxl import Workbook

from libScan import wj, p, B, chk, authorize, to_spisok, set_filter, l, read_config

dbconfig = read_config(section='mysql')
exlconfig = read_config(section='excel_input')

wb = openpyxl.load_workbook(read_only=True, **exlconfig)
sheet = wb[wb.sheetnames[0]]

dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

print('\n\n', datetime.strftime(datetime.now(), "%H:%M:%S"), 'Начинаем импорт из excel в БД')
# read_cursor.execute('SELECT * FROM main WHERE inn >-1;')
# rows = read_cursor.fetchall()


row = []
for i, row in enumerate(sheet.rows):
    if i == 0:
        continue
    id = l(row[0].value)
    id_fil = l(row[1].value)
    name_words = []
    name = row[2].value
    if str(type(name)) == "<class 'str'>":
        for n in name.split(' '):                  # Формируем tuple для таблицы ключевых слов
            name_words.append((id, n))
    full_name = row[3].value
    if str(type(full_name)) == "<class 'str'>":    # Формируем tuple для таблицы ключевых слов
        for n in full_name.split(' '):
            name_words.append((id, n))
    for j, nam in enumerate(name_words):
        n = nam[1].lower()
        if n == 'ооо' or n == 'ип' or n == 'ао' or n == 'аозт' or n == 'пао' or n == 'оао' or n == 'служба' \
                or n == 'компания' or n == 'фирма' or n == 'магазин' or n == 'мастерская' or n == 'центр' \
                or n == 'астрахань' or n == 'астрахани' or n == 'администрация' or n == 'организация' \
                or n == 'отделение' or n == 'предприятие' or n == 'завод' or n == 'астраханская' or n == 'комитет':
            name_words.pop(j)
    if row[4].value.lower().startswith('г. астрах'):
        address = row[4].value.upper() + ', ' + row[5].value.upper()
    else:
        address = 'АСТРАХАНСКАЯ ОБЛ, ' + row[4].value.upper().split(',')[1] + ', ' + row[4].value.upper().split(',')[0]\
                  + ', '+ row[5].value.upper()
    phones_all = []
    mob = row[6].value
    if str(type(mob)) == "<class 'str'>":
        for phone in mob.split(';'):
            phones_all.append((id, 'мобильный', phone))
    no_mob = row[7].value
    if str(type(no_mob)) == "<class 'str'>":
        for phone in no_mob.split(';'):
            phones_all.append((id, 'стационарный', phone))
    fax = row[8].value
    if str(type(fax)) == "<class 'str'>":
        for phone in fax.split(';'):
            phones_all.append((id, 'факс', phone))
    q=0


    rez_row = []
    for j, cell in enumerate(row):
        if cell == None:
            rez_cell = ''
        else:
            if head[j] == 'inn':
                if cell > 9999999999:
                    rez_cell = '{:0>12d}'.format(cell)
                else:
                    rez_cell = '{:0>10d}'.format(cell)
            elif head[j] == 'kpp':
                rez_cell = '{:0>9d}'.format(cell)
            elif head[j] == 'id' or head[j] == 'act_num':
                rez_cell = str(cell)
            elif head[j] == 'phone_1' or head[j] == 'phone_2' or head[j] == 'phone_3' or head[j] == 'phone_4' or \
                            head[j] == 'phone_5':
                rez_cell = '{:0>11d}'.format(cell)
            elif head[j] == 'okpo' or head[j] == 'oktmo':
                rez_cell = '{:0>8d}'.format(cell)
            elif head[j] == 'ogrn':
                rez_cell = '{:0>13d}'.format(cell)
            else:
                rez_cell = cell.strip().replace('\n',' ').replace('\r',' ').replace('"',"'")
            rez_row.append(rez_cell)
    ws.append(rez_row)
    if i % 100 == 0:
        print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Записано в excel:', i)

wb.save(**exlconfig)
dbconn.close()


