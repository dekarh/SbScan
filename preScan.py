# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_config
import datetime
from datetime import datetime
import time
import string
from libScan import wj, p, B, chk, authorize, to_spisok, set_filter

webconfig = read_config(section='web')
fillconfig = read_config(section='fill')
dbconfig = read_config(section='mysql')
scanconfig = read_config(section='scan')

driver = webdriver.Chrome()  # Инициализация драйвера
driver.implicitly_wait(1) # Неявное ожидание - ждать ответа на каждый запрос до 1 сек
dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

authorize(driver, **webconfig)  # Авторизация
wj(driver)
to_spisok(driver)
wj(driver)
set_filter(driver, **scanconfig)
wj(driver)

try:
    g = 0
    height = driver.get_window_size()['height'] # Высота окна
    while g < 1000:
        inns = p(d = driver, f = 'vv', **B['inn_spisA'])
        read_cursor.execute('SELECT inn FROM pre_scan WHERE id >-1;')
        rows = read_cursor.fetchall()
        for i, inn in enumerate(inns):
            pass_string = False
            wj(driver)
            for row in rows:
                if row[0] == int(inn):
                    pass_string = True
            if pass_string:
                continue
            write_cursor.execute('INSERT INTO pre_scan(inn, inn2) VALUES( %s, %s )',
                                 (inn, inn))
            dbconn.commit()
            read_cursor.execute('SELECT count(*) FROM pre_scan WHERE id >-1;')
            rows = read_cursor.fetchall()
            if int(rows[0][0]) % 100 == 0:
                print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Сканировано из списка: ', int(rows[0][0]))

        f = p(d=driver, f='c', **B['next'])
        wj(driver)
        time.sleep(3)
        f.click()
        wj(driver)
        print(datetime.strftime(datetime.now(), "%H:%M:%S"),'next внизу')
        time.sleep(3)

    dbconn.close()
    driver.close()

except Exception as ee:
    print(datetime.strftime(datetime.now(), "%H:%M:%S"),'Ошибка: ', ee, '\n перезагружаю')
    dbconn.close()
    driver.close()
    driver = webdriver.Chrome()  # Инициализация драйвера
    driver.implicitly_wait(1)  # Неявное ожидание - ждать ответа на каждый запрос до 10 сек
    dbconn = MySQLConnection(**dbconfig)  # Открываем БД из конфиг-файла
    read_cursor = dbconn.cursor()
    write_cursor = dbconn.cursor()



