# -*- coding: utf-8 -*-

#
# Поиск соответствий между базами
#

from mysql.connector import MySQLConnection, Error
from datetime import datetime
import openpyxl
from openpyxl import Workbook

from libScan import l, s, read_config, norm_phone, append_words, propusk

dbconfig = read_config(section='mysql')
dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла

read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

print('\n\n', datetime.strftime(datetime.now(), "%H:%M:%S"), 'Начинаем поиск соотвествий между БД')
read_cursor.execute('SELECT inn, kpp, firm_full_name FROM main WHERE inn >-1;')
rows = read_cursor.fetchall()

row = []

for i, row in enumerate(rows):
    inn = row[0]
    kpp = row[1]
    firm_full_name = row[2]
    name_words = []                                 # tuple для таблицы ключевых слов
    n_words = []
    append_words(firm_full_name.replace('"',' ').replace('.',' ').replace('(',' ').replace(')',' '), n_words)
    for n in n_words:
        is_skip = False
        for p in propusk:
            if p[len(p)-1:] == '%':
                if n.lower().startswith(p[:len(p)-1]):
                    is_skip = True
                    break
            else:
                if n.lower() == p:
                    is_skip = True
                    break
        if not is_skip:
            name_words.append(n)
    if len(name_words) > 0:
        name_words_t = (name_words[0],)
        sql = 'SELECT id_from_gis, name_word FROM name_words WHERE '
        for j, n in enumerate(name_words):
            if j == 0:
                sql += 'name_word = %s'
            else:
                sql += ' OR name_word = %s'
                name_words_t += (n,)
        read_cursor.execute(sql, name_words_t)
        words = read_cursor.fetchall()
        j = 0
        while j < len(words):
            words[j] = (inn, kpp) + words[j]
            j += 1
        if len(words) > 0:
            sql = 'INSERT INTO main2gis(main_inn, main_kpp, id_from_gis, word) VALUES(%s,%s,%s,%s)'
            write_cursor.executemany(sql, words)
            dbconn.commit()
    if i % 500 == 0:
        print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Просмотрено в БД:', i)

dbconn.close()


