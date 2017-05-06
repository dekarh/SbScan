# -*- coding: utf-8 -*-

#
#    Дополнительный сканер учредителей
#

from selenium import webdriver

from mysql.connector import MySQLConnection, Error

from datetime import datetime
import time
import string
import sys
import traceback

from libScan import wj, p, B, chk, authorize, to_spisok, set_filter, l, read_config, unique

err_count = 0 # Счетчик ошибок

webconfig = read_config(section='web')
fillconfig = read_config(section='fill')
dbconfig = read_config(section='mysql')
scanconfig = read_config(section='scan')

driver = webdriver.Chrome()  # Инициализация драйвера
driver.implicitly_wait(1) # Неявное ожидание - ждать ответа на каждый запрос до 10 сек
dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

authorize(driver, **webconfig)  # Авторизация
#driver.get(**fillconfig)  # Открытие страницы где надо заполнять
wj(driver)
to_spisok(driver)
wj(driver)
set_filter(driver, **scanconfig)
wj(driver)

read_cursor.execute('SELECT inn_f FROM log WHERE id >-1 GROUP BY inn_f;')
# Если надо добавить из mai2fio (не забыть закомментить DELETE FROM внизу)
#read_cursor.execute('SELECT main_inn FROM main2fio WHERE id >-1 GROUP BY main_inn;')
logged_inns_db = read_cursor.fetchall()
logged_inns = []
logged_inns_t = []
for h in logged_inns_db:
    logged_inns.append(h[0])
    logged_inns_t.append((h[0],))
read_cursor.execute('SELECT inn FROM main WHERE inn >-1;')
had_inns_db = read_cursor.fetchall()
had_inns = []
for h in had_inns_db:
    had_inns.append(h[0])
print('\n\n\n----------------------------------\n', datetime.strftime(datetime.now(), "%H:%M:%S"),
      'Начинаем доп. сканирование учредителей. Всего спарсено компаний:', len(had_inns),
      '\n----------------------------------\n\n\n')
for i, had_inn in enumerate(had_inns):
    pass_string = False
    for h in logged_inns:
        if h == had_inn:
            pass_string = True
    if pass_string:
        continue
    g = 0
    while g < 1000:
        try:
            inn = had_inn
            logged_inns.append(had_inn)
            logged_inns_t.append((had_inn,))
            #    inn = 3015055287
            search = p(d = driver, f = 'c', **B['search'])
            wj(driver)
            if inn > 9999999999:
                inn_str = '{:0>12d}'.format(inn)
            else:
                inn_str = '{:0>10d}'.format(inn)
            search.clear()
            wj(driver)
            search.send_keys(inn_str)
            wj(driver)
            firma = p(d = driver, f = 'p', **B['firms_tr'])
            wj(driver)
            if firma == None:
                print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Компания ИНН ', inn_str,
                      ' - не найдена в категории')
                break
            wj(driver)
            firma.click()
            wj(driver)
            time.sleep(4)
            firm_full_name = p(d = driver, f = 'p', **B['firm_full_nameA'])
            kpp = p(d=driver, f='p', **B['kppA'])
            next_firm = False
            if firm_full_name == '':
                firm_full_name = p(d = driver, f = 'p', **B['familyA']) + ' ' + p(d = driver, f = 'p', **B['nameA'])\
                                 + ' ' + p(d = driver, f = 'p', **B['surnameA'])
            firm_full_names = firm_full_name.split()
            for ffn_i in firm_full_names:
                if ffn_i.strip().lower().startswith('акционерное') \
                        or ffn_i.strip().lower().startswith('государственное') \
                        or ffn_i.strip().lower().startswith('муниципальное') \
                        or ffn_i.strip().lower().startswith('потребительск')\
                        or ffn_i.strip().lower().startswith('общественная')\
                        or ffn_i.strip().lower().startswith('некоммерческ'):
                    next_firm = True
                    print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'В компании', firm_full_name,' (ИНН ', inn_str,
                          ') нет смысла искать учредителей')
                    break
            if next_firm:
                wj(driver)
                close = p(d=driver, f='c', **B['close'])
                wj(driver)
                close.click()
                wj(driver)
                time.sleep(4)
                break
            summ_s = p(d = driver, f = 'p', **B['summA'])
            if l(summ_s) > 0:
                summ = eval(summ_s.replace('тыс. ₽', '* 1000').replace('млн ₽', '*'
                        ' 1000000').replace('млрд ₽', '* 1000000000').replace('₽', '* 1').replace(',', '.'))
            else:
                summ = None
            cost_s = p(d = driver, f = 'p', **B['costA'])
            if l(cost_s) > 0:
                cost = eval(cost_s.replace('тыс. ₽', '* 1000').replace('млн ₽', '*'
                        ' 1000000').replace('млрд ₽', '* 1000000000').replace('₽', '* 1').replace(',', '.'))
            else:
                cost_s = None
            if chk(d = driver, **B['owners']):
                own_page = p(d = driver, f = 'c', **B['owners'])
                wj(driver)
                own_page.click()
            else:
                wj(driver)
                close = p(d=driver, f='c', **B['close'])
                wj(driver)
                close.click()
                wj(driver)
                time.sleep(4)
                break
            more_uchred = p(d=driver, f='p', **B['more_uchr'])
            wj(driver)
            had_more_uchred = more_uchred.is_displayed()
            if had_more_uchred:
                more_uchred.click()
                wj(driver)
                time.sleep(4)

            uchred_ids = p(d=driver, f='ps', **B['uchredsA'])
            unique(uchred_ids)
            wj(driver)
            for j, uchred_id in enumerate(uchred_ids):
                uchred_name = p(d=driver, f='p', data_id = uchred_id, **B['uchred_nameAD'])
                if uchred_name == '':
                    continue
                uchred_inn = p(d=driver, f='p', data_id = uchred_id, **B['uchred_innAD'])
                uchred_percent = p(d=driver, f='p', data_id = uchred_id, **B['uchred_%AD'])
                if l(uchred_inn) > 9999999999 and l(uchred_percent) > 1:
                    fio_fio = uchred_name.split()
                    name_fio = fio_fio[1]
                    family_fio = fio_fio[0]
                    if len(fio_fio) > 2:
                        surname_fio = fio_fio[2]
                    else:
                        surname_fio = ''
                    read_cursor.execute('SELECT * FROM fio WHERE fio.inn_fio = %s;', (uchred_inn,))
                    had_fio = read_cursor.fetchall()
                    if len(had_fio) < 1:
                        sql = 'INSERT INTO fio(inn_fio, name, surname, family) VALUES(%s,%s,%s,%s)'
                        write_cursor.execute(sql, (uchred_inn, name_fio, surname_fio, family_fio))
                    read_cursor.execute('SELECT * FROM main WHERE main.inn = %s AND main.kpp = %s;', (inn, kpp))
                    had_main = read_cursor.fetchall()
                    if len(had_main) < 1:
                        sql = 'INSERT INTO main(inn, kpp, firm_full_name, cost, summ) VALUES(%s,%s,%s,%s,%s)'
                        write_cursor.execute(sql, (inn, kpp, firm_full_name, cost_s, summ_s))
                    read_cursor.execute('SELECT * FROM main2fio WHERE main_inn=%s AND main_kpp=%s AND fio_inn_fio = %s;'
                                        , (inn, kpp, uchred_inn))
                    had_main2fio = read_cursor.fetchall()
                    if len(had_main2fio) < 1:
                        sql = 'INSERT INTO main2fio(percent, cost, summ, main_inn, main_kpp, fio_inn_fio) ' \
                                           'VALUES(%s,%s,%s,%s,%s,%s)'
                        write_cursor.execute(sql, (uchred_percent, int(cost * l(uchred_percent)/100),
                                           int(summ * l(uchred_percent)/100), inn, kpp, uchred_inn))
                    dbconn.commit()

            if had_more_uchred:
                wj(driver)
                close = p(d=driver, f='c', **B['close'])
                wj(driver)
                close.click()
                wj(driver)
                time.sleep(4)
                break

            print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Сохранил учредителей компании (ИНН ', inn_str,
                  ') всего сохранено:', len(logged_inns), 'из:', len(had_inns))
            if len(had_inns) % 100 == 0:
                print('\n---------------------------\n', datetime.strftime(datetime.now(), "%H:%M:%S"),
                      'Спарсено', len(had_inns), '\n---------------------------\n')
                err_count = 0                              # Обнуляем счетчик ошибок
            wj(driver)
            close = p(d = driver, f = 'c', **B['close'])
            wj(driver)
            close.click()
            wj(driver)
            time.sleep(4)
            break
        except Exception as ee:
            err_count += 1
            write_cursor.execute('DELETE FROM log WHERE id > -1')
            logged_inns_t.pop()
            logged_inns.pop()
            write_cursor.executemany('INSERT INTO log(inn_f) VALUES(%s)', logged_inns_t)
            dbconn.commit()
            if err_count > 10:
               driver.close()
               print('\n\n----------------------------------\n', datetime.strftime(datetime.now(), "%H:%M:%S"),
                      'Слишком много ошибок: ', ee, '\n начнем-ка заново :)\n----------------------------------\n\n')

               sys.exit()
            print('\n\n----------------------------------\n', datetime.strftime(datetime.now(), "%H:%M:%S"),
                  'Ошибка: ')
            traceback.print_exception(type(ee), ee, sys.exc_info()[2])
            print('\n перезагружаю\n----------------------------------\n\n')
            driver.close()
            driver = webdriver.Chrome()  # Инициализация драйвера
            driver.implicitly_wait(1)  # Неявное ожидание - ждать ответа на каждый запрос до 10 сек
            authorize(driver, **webconfig)  # Авторизация
            # driver.get(**fillconfig)  # Открытие страницы где надо заполнять
            wj(driver)
            to_spisok(driver)
            wj(driver)
            set_filter(driver, **scanconfig)
            wj(driver)

dbconn.close()
driver.close()
