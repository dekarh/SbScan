# -*- coding: utf-8 -*-

#
# Загрузка базы фирм из excel
#

propusk = [
    'ооо', 'ип', 'ао','ao' 'аозт', 'пао', 'оао', 'служба', 'компания', 'фирма', 'магазин', 'мастерская', 'центр',
    'астрахань', 'астрахани', 'астраханская', 'астраханское', 'астраханский', 'астраханские', 'администрация',
    'организация', 'отделение', 'предприятие', 'завод', 'комитет', 'филиал', 'и', 'а', 'в', 'от', 'под', 'на', 'или'
           ]

from mysql.connector import MySQLConnection, Error
from datetime import datetime
import openpyxl
from openpyxl import Workbook

from libScan import l, s, read_config, norm_phone, append_words

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
try:
    for i, row in enumerate(sheet.rows):
        if i == 0:
            continue
        id = l(row[0].value)
        id_fil = l(row[1].value)
        name_words = []                                 # tuple для таблицы ключевых слов
        n_words = []
        name = s(row[2].value)
        full_name = s(row[3].value)
        append_words(name,n_words)
        append_words(full_name,n_words)
        for n in n_words:
            if n.lower() in propusk:
                continue
            else:
                name_words.append((id,n))
        if len(s(row[4].value).upper().split(',')) < 2:
            address = s(row[4].value).upper() + ', ' + s(row[5].value).upper() + ', ' + s(row[6].value).upper()
        else:
            address = 'АСТРАХАНСКАЯ ОБЛ, ' + s(row[4].value).upper().split(',')[1] + ', ' + \
                      s(row[4].value).upper().split(',')[0] + ', '+ s(row[5].value).upper() + ', ' + s(row[6].value).upper()
        phones_all = []                                 # tuple для таблицы телефонов
        mob = row[7].value
        if str(type(mob)) == "<class 'str'>":
            for phone in mob.split(';'):
                phones_all.append((id, 'мобильный', norm_phone(phone)))
        no_mob = row[8].value
        if str(type(no_mob)) == "<class 'str'>":
            for phone in no_mob.split(';'):
                phones_all.append((id, 'стационарный', norm_phone(phone)))
        fax = row[9].value
        if str(type(fax)) == "<class 'str'>":
            for phone in fax.split(';'):
                phones_all.append((id, 'факс', norm_phone(phone)))
        contacts = []                           # tuple для таблицы контактов
        wwws = row[10].value
        if str(type(wwws)) == "<class 'str'>":
            for www in wwws.split('|'):
                contacts.append((id, 'www', www.strip()))
        emails = row[11].value
        if str(type(emails)) == "<class 'str'>":
            for email in emails.split(','):
                contacts.append((id, 'e-mail', email.strip()))
        socset = row[12].value
        if str(type(socset)) == "<class 'str'>":
            contacts.append((id, 'facebook', socset.strip()))
        socset = row[13].value
        if str(type(socset)) == "<class 'str'>":
            contacts.append((id, 'instagram', socset.strip()))
        socset = row[14].value
        if str(type(socset)) == "<class 'str'>":
            contacts.append((id, 'twitter', socset.strip()))
        socset = row[15].value
        if str(type(socset)) == "<class 'str'>":
            contacts.append((id, 'vk', socset.strip()))
        opisan = s(row[16].value)
        read_cursor.execute('SELECT * FROM two_gis WHERE two_gis.id = %s;', (id,))
        had_in_gis = read_cursor.fetchall()
        if len(had_in_gis) < 1:
            sql = 'INSERT INTO two_gis(id, id_fil, `name`, full_name, address, opisan) VALUES(%s,%s,%s,%s,%s,%s)'
            write_cursor.execute(sql, (id, id_fil, name, full_name, address, opisan))
        sql = 'INSERT INTO name_words(id_from_gis, name_word) VALUES(%s,%s)'
        write_cursor.executemany(sql, name_words)
        sql = 'INSERT INTO phones(id_from_gis, `type`, phone) VALUES(%s,%s,%s)'
        write_cursor.executemany(sql, phones_all)
        sql = 'INSERT INTO contacts(id_from_gis, `type`, contact) VALUES(%s,%s,%s)'
        write_cursor.executemany(sql, contacts)
        dbconn.commit()
        if i % 500 == 0:
            print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Записано в БД:', i)
except Exception as ee:
    q = 0

wb.save(**exlconfig)
dbconn.close()


