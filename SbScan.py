# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import sys
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_config
import openpyxl
from openpyxl import Workbook
from openpyxl.writer.write_only import WriteOnlyCell
import NormalizeFields as norm
import datetime
import time

# DRIVER_PATH = 'drivers/chromedriver.exe'
#DRIVER_PATH = 'drivers/chromedriver'

BID = {
    'menuIII'   : "compact-mode-btn",
       }
BXPATH = {
    'login'     : "//INPUT[@class='controls-TextBox__field js-controls-TextBox__field  ']",
    'password'  : "//INPUT[@class='js-controls-TextBox__field controls-TextBox__field']",
    'a-button'  : "//DIV[@class='loginForm__sendButton']",
    'menu>>'    : "//SPAN[@class='navigation-LeftNavigation__event icon-View']"
                  "[@data-go-event='onClickContragentIcon']",
    'menuCats'  : "(//SPAN[@class='controls-DropdownList__text'])[2]",
    'firms'     : "//DIV[@class='Contragents-CommonRenders__InnCorner Contragents-CommonRenders__Inn ws-ellipsis']",
    'firms_tr'  : "//TR[@class='controls-DataGridView__tr controls-ListView__item js-controls-ListView__item']",
    'data_id'   : "//TR[@class='controls-DataGridView__tr controls-ListView__item js-controls-ListView__item'][@data-id='",
    'close'     : "//DIV[@class='sbisname-window-title-close ws-button-classic ws-component ws-control-inactive"
                  " ws-enabled ws-field-button ws-float-close-right ws-no-select']",
    'first'     : '(//I[@sbisname="PagingBegin"])[1]',
    'next'      : '(//I[@sbisname="PagingNext"])[1]',
    'prev'      : '(//I[@sbisname="PagingPrev"])[1]',
}

BCLASS = {
    'cats'      : "controls-DropdownList__item-text",
    'firms'     : "controls-DataGridView__tr",
}

def wj(driver):  # Ждем, пока динамическая ява завершит все свои процессы
    WebDriverWait(driver, 50).until(lambda driver: driver.execute_script("return jQuery.active == 0"))
    """
    Еще варианты фреймворков/библиотек:
    "return Ajax.activeRequestCount == 0"
    "return dojo.io.XMLHTTPTransport.inFlight.length == 0"
    Ожидание пока все набранные буквы от-явятся:
    element = WebDriverWait(ff, 10).until(EC.presence_of_element_located((By.ID, "keywordSuggestion")))
    """
    return

def wa(driver): # Типа ловит анимацию. Здесь не ловит :(
    WebDriverWait(driver, 10).until(lambda driver: driver.find_element(By.ID, 'new - element') and
                                                   driver.find_elements(By.ID, 'spinner') == 0)
    return
"""
Прокрутка
driver.execute_script("return arguments[0].scrollIntoView();", elem) # Здесь не точно
driver.execute_script("window.scrollTo(0, 911)") # Здесь вообще не прокручивает

"""

def chk_xpath(d, name_of_xpath): # Проверка наличия элемента, не вызывающая исключения
# А можно было просто EC.presence_of_element_located((By.XPATH, "xpath")))
    wj(d)
    try:
        d.find_element_by_xpath(BXPATH[name_of_xpath])
    except NoSuchElementException:
        return False
    return True

def xc_dataid(d,name_of_xpath,data_id):
    wj(d)
    return WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.XPATH, BXPATH['data_id']+str(data_id)+"']")))

def xc(d,name_of_xpath):
    wj(d)
    return WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.XPATH, BXPATH[name_of_xpath])))

def xv(d,name_of_xpath):
    wj(d)
    return WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.XPATH, BXPATH[name_of_xpath])))

def xp(d,name_of_xpath):
    wj(d)
    return WebDriverWait(d, 20).until(EC.presence_of_element_located((By.XPATH, BXPATH[name_of_xpath])))

def xps(d,name_of_xpath):
    wj(d)
    return WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.XPATH, BXPATH[name_of_xpath])))

def xvs(d,name_of_xpath):
    wj(d)
    return WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.XPATH, BXPATH[name_of_xpath])))

def ic(d,name_of_id):
    wj(d)
    return WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.ID, BID[name_of_id])))

def iv(d,name_of_id):
    wj(d)
    return WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.ID, BID[name_of_id])))

def ip(d,name_of_id):
    wj(d)
    return WebDriverWait(d, 20).until(EC.presence_of_element_located((By.ID, BID[name_of_id])))

def ips(d,name_of_id):
    wj(d)
    return WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.ID, BID[name_of_id])))

def ivs(d,name_of_id):
    wj(d)
    return WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.ID, BID[name_of_id])))

def cc(d,name_of_class):
    wj(d)
    return WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, BCLASS[name_of_class])))

def cv(d,name_of_class):
    wj(d)
    return WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, BCLASS[name_of_class])))

def cp(d,name_of_class):
    wj(d)
    return WebDriverWait(d, 20).until(EC.presence_of_element_located((By.CLASS_NAME, BCLASS[name_of_class])))

def cps(d,name_of_class):
    wj(d)
    return WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, BCLASS[name_of_class])))

def cvs(d,name_of_class):
    wj(d)
    return WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, BCLASS[name_of_class])))

def authorize(driver, login, password, authorize_page=''):
    time.sleep(1)
    if authorize_page != '':
        driver.get(authorize_page)
    # Ввод логина
    elem = xc(driver,'login')
    time.sleep(1)
    elem.send_keys(login)
    # Ввод пароля
    elem = xc(driver, 'password')
    time.sleep(1)
    elem.send_keys(password)
    # Отправка формы нажатием кнопки
    elem = xc(driver, 'a-button')
    elem.click()
    return

def to_spisok(driver):
    g = 0
    while g < 1000:
        try:
            menu = ic(driver, 'menuIII')  # Три палочки
            company = xp(driver, 'menu>>')  # >>
            wj(driver)
            menu.click()
            wj(driver)
            if not company.is_displayed():
                wj(driver)
                continue
            company.click()
            wj(driver)
            if chk_xpath(driver, "menuCats"):
                wj(driver)
                if driver.find_element_by_xpath(BXPATH['menuCats']).is_displayed():
                    return
            continue
        except Exception as ee:
            continue

def set_filter(driver):
    g = 0
    while g < 1000:
        try:
            elem = xv(driver,'menuCats') # Открываем дроплист
            wj(driver)
            elem.click()
            wj(driver)
            cats = cvs(driver, 'cats')  # Выбираем категорию
            wj(driver)
            for i, cat in enumerate(cats):
                wj(driver)
                if cat.text == 'Страхование, пенсионное обеспечение' and cat.is_displayed():
                    wj(driver)
                    cat.click()
                    break
            wj(driver)
            if chk_xpath(driver, 'menuCats'):
                wj(driver)
                if driver.find_element_by_xpath(BXPATH['menuCats']).text == 'Страхование, пенсионное обеспечение':
                    wj(driver)
                    return
                wj(driver)
            continue
        except  Exception as ee:
            continue


# driver = webdriver.Chrome(DRIVER_PATH)  # Инициализация драйвера
#driver = webdriver.Firefox()  # Инициализация драйвера

webconfig = read_config(section='web')
fillconfig = read_config(section='fill')
dbconfig = read_config(section='mysql')

driver = webdriver.Chrome()  # Инициализация драйвера
driver.implicitly_wait(20) # Ждать ответа на каждый запрос до 10 сек


authorize(driver, **webconfig)  # Авторизация
#driver.get(**fillconfig)  # Открытие страницы где надо заполнять
wj(driver)
to_spisok(driver)
wj(driver)
set_filter(driver)
wj(driver)

dbconn = MySQLConnection(**dbconfig) # Открываем БД из конфиг-файла
read_cursor = dbconn.cursor()
write_cursor = dbconn.cursor()

g = 0
while g < 1000:
    firms = xvs(driver, 'firms_tr')
    read_cursor.execute('SELECT data_id, inn, kpp FROM main WHERE data_id >-1;')
    rows = read_cursor.fetchall()
    for i, firm in enumerate(firms):
        pass_string = False
        wj(driver)
        for row in rows:
            if row[0] == int(firm.get_attribute('data-id')):
                pass_string = True
        if pass_string:
            continue
        if firm.location['y'] < 109:
            wj(driver)
            f = xc(driver,'first')
            wj(driver)
            f.click()
            wj(driver)
            print('first')
            time.sleep(1)
            break
        if firm.location['y'] > 862:
            wj(driver)
            f = xc(driver,'next')
            wj(driver)
            f.click()
            wj(driver)
            print('next')
            time.sleep(1)
            break
        wj(driver)
        if firm.is_displayed():
            wj(driver)                                      # Если DOM изменилось доступ через то что не меняется
            firma = xc_dataid(driver,'data_id',str(firm.get_attribute('data-id')))
            wj(driver)
            firma.click()
            wj(driver)
            time.sleep(4)
            sql = 'INSERT INTO main (data_id, inn, kpp) VALUES(' + firma.get_attribute('data-id')+',1,1);'
            write_cursor.execute(sql)
            dbconn.commit()
            wj(driver)
            close = xc(driver,'close')
            wj(driver)
            close.click()
            wj(driver)
            time.sleep(4)

dbconn.close()
driver.close()



