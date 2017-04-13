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

def chk_xpath(driver, xpath): # Проверка наличия элемента, не вызывающая исключения
# А можно было просто EC.presence_of_element_located((By.XPATH, "xpath")))
    wj(driver)
    try:
        driver.find_element_by_xpath(xpath)
        wj(driver)
    except NoSuchElementException:
        return False
    return True

def authorize(driver, login, password, authorize_page=''):
    time.sleep(1)
    if authorize_page != '':
        driver.get(authorize_page)
    # Ввод логина
    elem = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,
                                      "//INPUT[@class='controls-TextBox__field js-controls-TextBox__field  ']")))
    time.sleep(1)
    elem.send_keys(login)
    # Ввод пароля
    elem = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,
                                        "//INPUT[@class='js-controls-TextBox__field controls-TextBox__field']")))
    time.sleep(1)
    elem.send_keys(password)
    # Отправка формы нажатием кнопки
    elem = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,
                                                                      "//DIV[@class='loginForm__sendButton']")))
    elem.click()
    return

def to_spisok(driver):
    g = 0
    while g < 1000:
        try:
            wj(driver)
            menu = WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.ID, "compact-mode-btn")))  # Три палочки
            wj(driver)
            company = driver.find_element_by_class_name('navigation-LeftNavigation__event')  # >>
            wj(driver)
            menu.click()
            wj(driver)
            if not company.is_displayed():
                continue
            wj(driver)
            company.click()
            wj(driver)
            if chk_xpath(driver, "(//SPAN[@class='controls-DropdownList__text'])[2]"):
                wj(driver)
                if driver.find_element_by_xpath("(//SPAN[@class='controls-DropdownList__text'])[2]").is_displayed():
                    return
            continue
        except:
            continue

def set_filter(driver):
    g = 0
    while g < 1000:
        try:
            wj(driver)
            # Открываем дроплист
            elem = driver.find_element_by_xpath("(//SPAN[@class='controls-DropdownList__text'])[2]")
            wj(driver)
            if not elem.is_displayed():
                continue
            wj(driver)
            elem.click()
            wj(driver)
            # Выбираем категорию
            wj(driver)
            cats = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.CLASS_NAME,
                                                                                'controls-DropdownList__item-text')))
            wj(driver)
            for i, cat in enumerate(cats):
                wj(driver)
                if cat.text == 'Страхование, пенсионное обеспечение':
                    wj(driver)
                    category = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,
                                "(//DIV[@class='controls-DropdownList__item-text'])[" + str(i + 1) + "]")))
                    wj(driver)
                    category.click()
                    break
            wj(driver)
            if chk_xpath(driver, "(//SPAN[@class='controls-DropdownList__text'])[2]"):
                wj(driver)
                if driver.find_element_by_xpath("(//SPAN[@class='controls-DropdownList__text'])[2]").text == 'Страхование,' \
                        ' пенсионное обеспечение':
                    wj(driver)
                    return
            continue
        except:
            continue


def to_card(driver, num):
    g = 0
    while g < 1000:
        try:
            wj(driver)
# Не находит ни так ни так
#            firma = driver.find_element_by_xpath("(//DIV[@class='Contragents-CommonRenders__InnCorner "
#                                                 "Contragents-CommonRenders__Inn ws-ellipsis'])[" + str(num + 1) + "]")
            firma = driver.find_element_by_xpath("(//DIV[@class='controls-DataGridView__tr "
                                         "controls-ListView__item js-controls-ListView__item'])[" + str(num + 1) + "]")
            wj(driver)
            firma.click()
            wj(driver)
            if driver.find_element_by_xpath(
                    "(//SPAN[@class='ContragentCard_RightAccordion-content'])[1]").is_displayed():
                wj(driver)
                return
            elif driver.find_element_by_xpath("(//SPAN[@class='controls-DropdownList__text'])[2]").is_displayed():
                wj(driver)
                continue
            else:
                wj(driver)
                to_spisok(driver)
                wj(driver)
                set_filter(driver)
                wj(driver)
                continue
        except Error:
            wj(driver)
            if chk_xpath(driver,"(//SPAN[@class='ContragentCard_RightAccordion-content'])[1]"):
                wj(driver)
                if driver.find_element_by_xpath("(//SPAN[@class='ContragentCard_RightAccordion-content'])[1]").is_displayed():
                    wj(driver)
                    return
            elif chk_xpath(driver, "(//SPAN[@class='controls-DropdownList__text'])[2]"):
                wj(driver)
                if driver.find_element_by_xpath("(//SPAN[@class='controls-DropdownList__text'])[2]").is_displayed():
                    wj(driver)
                    continue
            else:
                wj(driver)
                to_spisok(driver)
                wj(driver)
                set_filter(driver)
                wj(driver)
                continue

def from_card(driver):
    g = 0
    while g < 1000:
        try:
            wj(driver)
            ex = driver.find_element_by_xpath("(//DIV[@class='sbisname-window-title-close ws-button-classic "
                "ws-component ws-control-inactive ws-enabled ws-field-button ws-float-close-right ws-no-select'])[1]")
            wj(driver)
            ex.click()
            wj(driver)
            if chk_xpath(driver, "(//SPAN[@class='controls-DropdownList__text'])[2]"):
                wj(driver)
                if driver.find_element_by_xpath("(//SPAN[@class='controls-DropdownList__text'])[2]").is_displayed():
                    wj(driver)
                    return
            elif chk_xpath(driver, "(//SPAN[@class='ContragentCard_RightAccordion-content'])[1]"):
                wj(driver)
                if driver.find_element_by_xpath(
                            "(//SPAN[@class='ContragentCard_RightAccordion-content'])[1]").is_displayed():
                    wj(driver)
                    continue
            else:
                wj(driver)
                to_spisok(driver)
                wj(driver)
                set_filter(driver)
                wj(driver)
                return
        except:
            if chk_xpath(driver, "(//SPAN[@class='controls-DropdownList__text'])[2]"):
                wj(driver)
                if driver.find_element_by_xpath("(//SPAN[@class='controls-DropdownList__text'])[2]").is_displayed():
                    wj(driver)
                    return
            elif chk_xpath(driver, "(//SPAN[@class='ContragentCard_RightAccordion-content'])[1]"):
                wj(driver)
                if driver.find_element_by_xpath("(//SPAN[@class="
                                                "'ContragentCard_RightAccordion-content'])[1]").is_displayed():
                    wj(driver)
                    continue
            else:
                wj(driver)
                to_spisok(driver)
                wj(driver)
                set_filter(driver)
                wj(driver)
                return


# driver = webdriver.Chrome(DRIVER_PATH)  # Инициализация драйвера
#driver = webdriver.Firefox()  # Инициализация драйвера

webconfig = read_config(section='web')
fillconfig = read_config(section='fill')
dbconfig = read_config(section='mysql')

driver = webdriver.Chrome()  # Инициализация драйвера
driver.implicitly_wait(20) # Ждать ответа на каждый запрос до 10 сек


authorize(driver, **webconfig)  # Авторизация
#driver.get(**fillconfig)  # Открытие страницы
wj(driver)
to_spisok(driver)
wj(driver)
set_filter(driver)
wj(driver)
firms = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.XPATH,
    "//DIV[@class='Contragents-CommonRenders__InnCorner Contragents-CommonRenders__Inn ws-ellipsis']")))
#firms = WebDriverWait(driver, 50).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, 'controls-DataGridView__tr')))
wj(driver)
g = 0
for i, firm in enumerate(firms):
    wj(driver)
    to_card(driver,i)
    wj(driver)
    from_card(driver)




"""
for i, firm in enumerate(firms):
    firma = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH,
         "(//DIV[@class='Contragents-CommonRenders__InnCorner Contragents-CommonRenders__Inn ws-ellipsis'])["+str(i+1)+"]")))
    firma = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,
         "(//DIV[@class='Contragents-CommonRenders__InnCorner Contragents-CommonRenders__Inn ws-ellipsis'])["+str(i+1)+"]")))
    time.sleep(1)
    firma.click()
    ex = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH,
                  "(//DIV[@class='sbisname-window-title-close ws-button-classic ws-component ws-control-inactive"
                  " ws-enabled ws-field-button ws-float-close-right ws-no-select'])[1]")))
    ex = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,
                  "(//DIV[@class='sbisname-window-title-close ws-button-classic ws-component ws-control-inactive"
                  " ws-enabled ws-field-button ws-float-close-right ws-no-select'])[1]")))
    time.sleep(1)
    ex.click()
"""

#sbisname-window-title-close ws-button-classic ws-component ws-control-inactive ws-enabled ws-field-button ws-float-close-right ws-no-select
#<div tabindex="0" unselectable="on" title="" class="sbisname-window-title-close ws-button-classic ws-component ws-control-inactive ws-enabled ws-field-button ws-float-close-right ws-no-select" hasmarkup="true" sbisname="floatAreaCloseButton" hidefocus="true" wasbuildmarkup="true" id="ws-9h0nayp3o51491985084363" style="z-index: 100; margin-right: 0px; margin-top: 0px;"></div>

#.is_displayed()
#<input class="js-controls-TextBox__field controls-TextBox__field" autocomplete="off" placeholder="Введите название или ИНН" maxlength="255">
#<span class="Contragents-CommonRenders__Name"> Премиум Ассистанс, ООО</span>
#<div class="Contragents-CommonRenders__InnCorner Contragents-CommonRenders__Inn ws-ellipsis" title="7724222547 / 772901001">7724222547</div>

#d.execute_script("return arguments[0].scrollIntoView();", element)

#elem = driver.find_elements_by_class_name('controls-DataGridView__tr')

# <div tabindex="0" unselectable="on" title="" class="sbisname-window-title-close ws-button-classic ws-component ws-control-inactive ws-enabled ws-field-button ws-float-close-right ws-no-select" hasmarkup="true" sbisname="floatAreaCloseButton" hidefocus="true" wasbuildmarkup="true" id="ws-weh4bdrt8uk1491925118199" style="z-index: 100; margin-right: 0px; margin-top: 0px;"></div>
"""
conn = MySQLConnection(**dbconfig) # Открываем БД из конфиг-файла
cursor = conn.cursor()

emptity = []
cursor.execute('SELECT code,text FROM status_employment_position WHERE code >-1;')
rows = cursor.fetchall()
for row in rows:
    emptity.append(row[1])
    
# Пример UPDATE
    if loaded:
        sql = 'UPDATE contracts SET loaded=1 WHERE client_id=' + '"' + res_inp['id'] + '"' + ' AND id>-1'
        cursor.execute(sql)
        conn.commit()

"""

driver.close()



