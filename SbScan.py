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

B = {
    'menuIII'   : {'t': 'i', 's' : 'compact-mode-btn'},
    'login'     : {'t': 'x', 's' : '//INPUT[@class="controls-TextBox__field js-controls-TextBox__field  "]'},
    'password'  : {'t': 'x', 's' : '//INPUT[@class="js-controls-TextBox__field controls-TextBox__field"]'},
    'a-button'  : {'t': 'x', 's' : '//DIV[@class="loginForm__sendButton"]'},
    'menu>>'    : {'t': 'x', 's' : '//SPAN[@class="navigation-LeftNavigation__event icon-View"]'
                                                    '[@data-go-event="onClickContragentIcon"]'},
    'menuCats'  : {'t': 'x', 's' : '(//SPAN[@class="controls-DropdownList__text"])[2]'},
    'firms_x'   : {'t': 'x', 's' : '//DIV[@class="Contragents-CommonRenders__InnCorner '
                                                    'Contragents-CommonRenders__Inn ws-ellipsis"]'},
    'firms_tr'  : {'t': 'x', 's' : '//TR[@class="controls-DataGridView__tr controls-ListView__item '
                                                                    'js-controls-ListView__item"]'},
    'data_id'   : {'t': 'x', 's' : '//TR[@class="controls-DataGridView__tr controls-ListView__item '
                                                          'js-controls-ListView__item"][@data-id="'},
    'close'     : {'t': 'x', 's' : '//DIV[@class="sbisname-window-title-close ws-button-classic ws-component '
                        'ws-control-inactive ws-enabled ws-field-button ws-float-close-right ws-no-select"]'},
    'first'     : {'t': 'x', 's' : '(//I[@sbisname="PagingBegin"])[1]'},
    'next'      : {'t': 'x', 's' : '(//I[@sbisname="PagingNext"])[1]'},
    'prev'      : {'t': 'x', 's' : '(//I[@sbisname="PagingPrev"])[1]'},
    'cats'      : {'t': 'c', 's': 'controls-DropdownList__item-text'},
    'firms_c'   : {'t': 'c', 's': 'controls-DataGridView__tr'},
    'ch_surname': {'t': 'c', 's': 'Contragents-ContragentCard__Chief__surname'},
    'ch_name'   : {'t': 'c', 's': 'Contragents-ContragentCard__Chief__name'},
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
def chk(d, t, s, f = '', a = '', data_id = ''): # Проверка наличия элемента, не вызывающая исключения
    wj(d)
    if data_id != '':
        data_id += '"]'
    try:
        if   t == 'i':
            d.find_element(By.ID, s)
        elif t == 'c':
            d.find_element(By.CLASS_NAME, s)
        elif t == 'x':
            d.find_element(By.XPATH, s)
    except NoSuchElementException:
        return False
    return True
"""
^^^
|||
Потому что EC.presence_of_element_located((By.XPATH, "xpath"))) возвращает объект, не нашел где там результат
try:
    assert EC.presence_of_element_located((By.XPATH, '//*[@id="Waldo"]')) is not True
except AssertionError, e:
    self.verificationErrors.append('presence_of_element_located returned True for Waldo')
"""

def p(d, t, f, s, a = '', data_id = ''):
    wj(d)
    if data_id != '':
        data_id += '"]'
    if t == 'i':
        if   f == 'c':
            foo = WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.ID, s + data_id)))
            if a == '':
                return foo
            else:
                return foo.get_attribute(a)
        elif f == 'v':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.ID, s + data_id)))
            if a == '':
                return foo
            else:
                return foo.get_attribute(a)
        elif f == 'vs':
            return WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.ID, s + data_id)))
        elif f == 'p':
            foo = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.ID, s + data_id)))
            if a == '':
                return foo
            else:
                return foo.get_attribute(a)
        elif f == 'ps':
            return WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.ID, s + data_id)))
        else:
            return
    elif t == 'x':
        if   f == 'c':
            foo = WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.XPATH, s+data_id)))
            if a == '':
                return foo
            else:
                return foo.get_attribute(a)
        elif f == 'v':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.XPATH, s+data_id)))
            if a == '':
                return foo
            else:
                return foo.get_attribute(a)
        elif f == 'vs':
            return WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.XPATH, s + data_id)))
        elif f == 'p':
            foo = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.XPATH, s + data_id)))
            if a == '':
                return foo
            else:
                return foo.get_attribute(a)
        elif f == 'ps':
            return WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.XPATH, s + data_id)))
        else:
            return
    elif t == 'c':
        if   f == 'c':
            foo = WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, s + data_id)))
            if a == '':
                return foo
            else:
                return foo.get_attribute(a)
        elif f == 'v':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, B[s]+data_id)))
            if a == '':
                return foo
            else:
                return foo.get_attribute(a)
        elif f == 'vs':
            return WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, s + data_id)))
        elif f == 'p':
            foo = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.CLASS_NAME, s + data_id)))
            if a == '':
                return foo
            else:
                return foo.get_attribute(a)
        elif f == 'ps':
            return WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, s + data_id)))
        else:
            return


def xc_dataid(d,name_of_xpath,data_id):
    wj(d)
    return WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.XPATH, BXPATH['data_id']+str(data_id)+"']")))

def authorize(driver, login, password, authorize_page=''):
    time.sleep(1)
    if authorize_page != '':
        driver.get(authorize_page)
    # Ввод логина
    log = p(d = driver, f = 'c', **B['login'])
    time.sleep(1)
    log.send_keys(login)
    # Ввод пароля
    passwd = p(d = driver, f = 'c', **B['password'])
    time.sleep(1)
    passwd.send_keys(password)
    # Отправка формы нажатием кнопки
    cl = p(d = driver, f = 'c', **B['a-button'])
    cl.click()
    return

def to_spisok(driver):
    g = 0
    while g < 1000:
        try:
            menu = p(d = driver, f = 'c', **B['menuIII']) # Три палочки
            wj(driver)
            company = p(d = driver, f = 'p', **B['menu>>'])  # >>
            wj(driver)
            menu.click()
            wj(driver)
            if not company.is_displayed():
                wj(driver)
                continue
            company.click()
            wj(driver)
            if chk(d = driver, **B['menuCats']):
                wj(driver)
                if p(d = driver, f = 'p', **B['menuCats']).is_displayed():
                    return
            continue
        except Exception as ee:
            continue

def set_filter(driver):
    g = 0
    while g < 1000:
        try:
            elem = p(d = driver, f = 'v', **B['menuCats']) # Открываем дроплист
            wj(driver)
            elem.click()
            wj(driver)
            cats = p(d = driver, f = 'vs', **B['cats'])  # Выбираем категорию
            wj(driver)
            for i, cat in enumerate(cats):
                wj(driver)
                if cat.text == 'Страхование, пенсионное обеспечение' and cat.is_displayed():
                    wj(driver)
                    cat.click()
                    break
            wj(driver)
            if chk(d = driver, **B['menuCats']):
                wj(driver)
                if p(d = driver, f = 'p', **B['menuCats']).text == 'Страхование, пенсионное обеспечение':
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
height = driver.get_window_size()['height'] # Высота окна
while g < 1000:
    firms = p(d = driver, f = 'vs', **B['firms_tr'])
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
        if firm.location['y'] < 105:
            wj(driver)
            f = p(d = driver, f = 'c', **B['prev'])
            wj(driver)
            f.click()
            wj(driver)
            print('prev')
            time.sleep(1)
            break
        if firm.location['y'] > (height - 79):
            wj(driver)
            f = p(d = driver, f = 'c', **B['next'])
            wj(driver)
            f.click()
            wj(driver)
            print('next')
            time.sleep(1)
            break
        wj(driver)
        if firm.is_displayed():
            wj(driver)                                      # Если DOM изменилось доступ через data-id (он не меняется)
            firma = p(d = driver, f = 'c', **B['data_id'], data_id = str(firm.get_attribute('data-id')))
#            xc_dataid(driver,'data_id',str(firm.get_attribute('data-id')))
            wj(driver)
            firma.click()
            wj(driver)
            time.sleep(4)
            sql = 'INSERT INTO main (data_id, inn, kpp) VALUES(' + firma.get_attribute('data-id')+',1,1);'
            write_cursor.execute(sql)
            dbconn.commit()
            wj(driver)
            close = p(d = driver, f = 'c', **B['close'])
            wj(driver)
            close.click()
            wj(driver)
            time.sleep(4)

dbconn.close()
driver.close()



