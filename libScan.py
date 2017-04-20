# -*- coding: utf-8 -*-

#
# Библиотека функций
#

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

# DRIVER_PATH = 'drivers/chromedriver.exe'
#DRIVER_PATH = 'drivers/chromedriver'

B = {
    'menuIII'   : {'t': 'i', 's': 'compact-mode-btn'},
    'login'     : {'t': 'x', 's': '//INPUT[@class="controls-TextBox__field js-controls-TextBox__field  "]'},
    'password'  : {'t': 'x', 's': '//INPUT[@class="js-controls-TextBox__field controls-TextBox__field"]'},
    'a-button'  : {'t': 'x', 's': '//DIV[@class="loginForm__sendButton"]'},
    'menu>>'    : {'t': 'x', 's': '//SPAN[@class="navigation-LeftNavigation__event icon-View"]'
                                                    '[@data-go-event="onClickContragentIcon"]'},
    'menuCats'  : {'t': 'x', 's': '(//SPAN[@class="controls-DropdownList__text"])[2]'},
    'firms_x'   : {'t': 'x', 's': '//DIV[@class="Contragents-CommonRenders__InnCorner '
                                                    'Contragents-CommonRenders__Inn ws-ellipsis"]'},
    'firms_tr'  : {'t': 'x', 's': '//DIV[@sbisname="contragentsBrowser"]//TR[@data-id]'},
    'firms_trA' : {'t': 'x', 's': '//SPAN[@class="Contragents-CommonRenders__Name"]/../../../../..', 'a': 'data-id'},
    'data_id'   : {'t': 'x', 's': '//TR[@class="controls-DataGridView__tr controls-ListView__item '
                                                          'js-controls-ListView__item"][@data-id="'},
    'data_idA'  : {'t': 'x', 's': '//TR[@class="controls-DataGridView__tr controls-ListView__item '
                                    'js-controls-ListView__item"][@data-id="', 'a' : 'data-id'},
    'close'     : {'t': 'x', 's': '//DIV[@class="sbisname-window-title-close ws-button-classic ws-component '
                        'ws-control-inactive ws-enabled ws-field-button ws-float-close-right ws-no-select"]'},
    'first'     : {'t': 'x', 's': '(//I[@sbisname="PagingBegin"])[1]'},
    'next'      : {'t': 'x', 's': '(//I[@sbisname="PagingNext"])[1]'},
    'prev'      : {'t': 'x', 's': '(//I[@sbisname="PagingPrev"])[1]'},
    'innA'      : {'t': 'x', 's': '//INPUT[@name="СтрокаИНН"]', 'a' : 'value'},
    'kppA'      : {'t': 'x', 's': '//INPUT[@name="СтрокаКПП"]', 'a': 'value'},
    'familyA'   : {'t': 'x', 's': '//INPUT[@name="СтрокаФамилия"]', 'a': 'value'},
    'nameA'     : {'t': 'x', 's': '//INPUT[@name="СтрокаИмя"]', 'a': 'value'},
    'surnameA'  : {'t': 'x', 's': '//INPUT[@name="СтрокаОтчество"]', 'a': 'value'},
'firm_full_nameA':{'t': 'x', 's': '//INPUT[@name="СтрокаПолноеНазвание"]', 'a': 'value'},
   'act_num1000': {'t': 'x', 's': '//DIV[@class="custom-select-option"][@value="1000"]'},
    'about'     : {'t': 'x', 's': '//SPAN[@class="ContragentCard_RightAccordion-content"][text()="О компании"]'},
    'contacts'  : {'t': 'x', 's': '//SPAN[@class="ContragentCard_RightAccordion-content"][text()="Контактные данные"]'},
    'rekv'      : {'t': 'x', 's': '//SPAN[@class="ContragentCard_RightAccordion-content"][text()="Реквизиты"]'},
    'owners'    : {'t': 'x', 's': '//SPAN[@class="ContragentCard_RightAccordion-content"][text()="Владельцы"]'},
    'summA'     : {'t': 'x', 's': '//SPAN[@class="Contragents-ContragentCardRatingBanner__title-Revenue  '
                                  'ctrg-subseparator"][text()="Выручка: "]/SPAN', 'a': 'text'},
    'costA'     : {'t': 'x', 's': '//SPAN[@class="Contragents-ContragentCardRatingBanner__title-Cost  '
                                  'ctrg-subseparator"][text()="Стоимость бизнеса: "]/SPAN', 'a': 'text'},
    'rat_sumA'  : {'t': 'x', 's': '//DIV[@class="ctrg-half-left"]//DIV[@class="Contragents-'
                                  'ContragentCardRatingBanner__positions"]/DIV/SPAN', 'a': 'title'},
    'rat_costA' : {'t': 'x', 's': '//DIV[@class="ctrg-half-right"]//DIV[@class="Contragents-'
                                  'ContragentCardRatingBanner__positions"]/DIV/SPAN', 'a': 'title'},
    'phonesA'   : {'t': 'x', 's': '//DIV[@sbisname="Таблица телефонов"]//DIV[@class="crm-phone-number crm-noicon '
                                  'ContragentCardPhones-Ellipsis"]', 'a': 'text'},
   'phones_typA': {'t': 'x', 's': '//DIV[@sbisname="Таблица телефонов"]//SPAN[@class="crm-phone-comment '
                                  'ContragentCardPhones-Ellipsis"]', 'a': 'text'},
         'warnA': {'t': 'x', 's': '//DIV[@sbisname="Реестры"]//DIV[@class="Contragents-ContragentCardIndicators'
                                  '__itemTitle "]//SPAN[@data-component="SBIS3.CONTROLS.Link"]', 'a': 'text'},
    'warn_dataA': {'t': 'x', 's': '//DIV[@sbisname="Реестры"]//DIV[@class="Contragents-ContragentCardIndicators_'
                                  '_listItemFooter"]//SPAN[@data-component="SBIS3.CONTROLS.Link"]', 'a': 'text'},
    'filialsA'  : {'t': 'x', 's': '//DIV[@sbisname="Таблица филиалов"]//DIV[@title]', 'a': 'text'},
    'ogrnA'     : {'t': 'x', 's': '//DIV[@sbisname="СтрокаОГРН"]//SPAN[@title]', 'a': 'text'},
    'okpoA'     : {'t': 'x', 's': '//DIV[@sbisname="СтрокаОКПО"]//SPAN[@title]', 'a': 'text'},
    'oktmoA'    : {'t': 'x', 's': '//DIV[@sbisname="СтрокаОКТМО"]//SPAN[@title]', 'a': 'text'},
    'reg_N_pfrA': {'t': 'x', 's': '//DIV[@sbisname="СтрокаРегНомерПФ"]//SPAN[@title]', 'a': 'text'},
    'reg_comp'  : {'t': 'x', 's': '//DIV[@class="ContragentCardRegistration-Data"]', 'a': 'text'},
    'reg_org'   : {'t': 'x', 's': '//DIV[@class="ContragentCardRegistrationGosOrg-Data"]', 'a': 'text'},
    'uchred'    : {'t': 'x', 's': '//DIV[@sbisname="brwУчредители"]//DIV[@class="ws-browser-cell-paddings"]'
                                  '/DIV[@title]', 'a': 'title'},
    'dochki'    : {'t': 'x', 's': '//DIV[@sbisname="brwДочерниеКомпании"]//DIV[@class="ws-browser-cell-paddings"]'
                                  '/DIV[@title]', 'a': 'title'},
    'cats-link' : {'t': 'x', 's': '//DIV[@sbisname="DropdownList_buttonHasMore"]/SPAN'},
    'inn_spisA' : {'t': 'x', 's': '//DIV[@sbisname="contragentsBrowser"]//DIV[@class="Contragents-CommonRenders_'
                                  '_InnCorner Contragents-CommonRenders__Inn ws-ellipsis"]', 'a': 'text'},
    'search'    : {'t': 'x', 's': '//DIV[@sbisname="strSearch"]//INPUT'},

    'cats'      : {'t': 'c', 's': 'controls-DropdownList__item-text'},
    'firms_c'   : {'t': 'c', 's': 'controls-DataGridView__tr'},
   'ch_surnameA': {'t': 'c', 's': 'Contragents-ContragentCard__Chief__surname', 'a': 'text'},
    'ch_nameA'  : {'t': 'c', 's': 'Contragents-ContragentCard__Chief__name', 'a': 'text'},
    'ch_titleA' : {'t': 'c', 's': 'Contragents-ContragentCard__Chief__title', 'a': 'text'},
    'gen_infoA' : {'t': 'c', 's': 'Contragents-ContragentCardGeneralInfo__State', 'a': 'text'},
    'act_link'  : {'t': 'c', 's': 'Contragents-ContragentCardGeneralInfo__ActivityTypes__title'},
  'act_by_count': {'t': 'c', 's': 'custom-select-text'},
    'acts'      : {'t': 'c', 's': 'ws-browser-table-row'},
    'act_numA'  : {'t': 'c', 's': 'Contragents-ContragentCardGeneralInfo__ActivityTypes__counter', 'a': 'text'},
    'emp_qtyA'  : {'t': 'c', 's': 'Contragents-ContragentCard__EmployeesQuantity__qty', 'a': 'text'},
    'addressA'  : {'t': 'c', 's': 'ContragentCardAddresses-blackLink', 'a': 'text'},
    'predstavA' : {'t': 'c', 's': 'user-info-cell', 'a': 'text'},

}

def wj(driver):  # Ждем, пока динамическая ява завершит все свои процессы
    WebDriverWait(driver, 50).until(lambda driver: driver.execute_script("return jQuery.active == 0"))
    """
    Еще варианты фреймворков/библиотек:
    "return Ajax.activeRequestCount == 0"
    "return dojo.io.XMLHTTPTransport.inFlight.length == 0"
    Ожидание пока все набранные буквы отработют явой:
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
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'v':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.ID, s + data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'vs':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.ID, s + data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return [atr.text for atr in foo]
                else:
                    return [atr.get_attribute(a) for atr in foo]
        elif f == 'vv':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.ID, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo if atr.is_displayed()]
                    else:
                        return [atr.get_attribute(a) for atr in foo if atr.is_displayed()]
            else:
                if a == '':
                    return []
                else:
                    return ['']

        elif f == 'p':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.ID, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return foo.text
                    else:
                        return foo.get_attribute(a)
            else:
                if a == '':
                    return
                else:
                    return ''
        elif f == 'ps':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.ID, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo]
                    else:
                        return [atr.get_attribute(a) for atr in foo]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        else:
            return
    elif t == 'x':
        if   f == 'c':
            foo = WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.XPATH, s+data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'v':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.XPATH, s+data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'vs':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.XPATH, s + data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return [atr.text for atr in foo]
                else:
                    return [atr.get_attribute(a) for atr in foo]
        elif f == 'vv':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.XPATH, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo if atr.is_displayed()]
                    else:
                        return [atr.get_attribute(a) for atr in foo if atr.is_displayed()]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        elif f == 'p':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.XPATH, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return foo.text
                    else:
                        return foo.get_attribute(a)
            else:
                if a == '':
                    return
                else:
                    return ''
        elif f == 'ps':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.XPATH, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo]
                    else:
                        return [atr.get_attribute(a) for atr in foo]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        else:
            return
    elif t == 'c':
        if   f == 'c':
            foo = WebDriverWait(d, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, s + data_id)))
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'v':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, B[s]+data_id)))
            if a == '':
                return foo
            else:
                if a == 'text':
                    return foo.text
                else:
                    return foo.get_attribute(a)
        elif f == 'vs':
            foo = WebDriverWait(d, 20).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, s + data_id)))
            wj(d)
            if a == '':
                return foo
            else:
                if a == 'text':
                    return [atr.text for atr in foo]
                else:
                    return [atr.get_attribute(a) for atr in foo]
        elif f == 'vv':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo if atr.is_displayed()]
                    else:
                        return [atr.get_attribute(a) for atr in foo if atr.is_displayed()]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        elif f == 'p':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_element_located((By.CLASS_NAME, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return foo.text
                    else:
                        return foo.get_attribute(a)
            else:
                if a == '':
                    return
                else:
                    return ''
        elif f == 'ps':
            if chk(d = d, t = t, s = s + data_id):
                wj(d)
                foo = WebDriverWait(d, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, s + data_id)))
                wj(d)
                if a == '':
                    return foo
                else:
                    if a == 'text':
                        return [atr.text for atr in foo]
                    else:
                        return [atr.get_attribute(a) for atr in foo]
            else:
                if a == '':
                    return []
                else:
                    return ['']
        else:
            return

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
            print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Ошибка в to_spisok', ee)
            continue

def set_filter(driver, category = ''):
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
                if cat.text == category and cat.is_displayed():
                    wj(driver)
                    cat.click()
                    break
            wj(driver)
            if chk(d = driver, **B['menuCats']):
                wj(driver)
                if p(d = driver, f = 'p', **B['menuCats']).text == category:
                    wj(driver)
                    return
                wj(driver)
            continue
        except  Exception as ee:
            print(datetime.strftime(datetime.now(), "%H:%M:%S"), 'Ошибка в to_spisok', ee)
            continue
