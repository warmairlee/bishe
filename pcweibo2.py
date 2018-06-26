from selenium import webdriver
import time
import threading
import pickle
import os
from bs4 import BeautifulSoup
import sys
import urllib.request
import tkinter as tk
from selenium.webdriver.support.ui import WebDriverWait
from http import cookiejar
import http.cookiejar


def get_cookie_from_net(yourid, yourpwd):
    driver = webdriver.Chrome()
    driver.get('https://weibo.com/')
    try:
        WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath('//*[@id="loginname"]')).send_keys(yourid)
    except Exception:
        driver.quit()
    time.sleep(0.5)
    input_wd = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
    input_wd.send_keys(yourpwd)
    button = driver.find_element_by_id('login_form_savestate')
    button.click()
    time.sleep(0.5)
    button_sub = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
    button_sub.click()
    time.sleep(2)
    t1 = threading.Thread(target=method1,args=(driver,))
    t2 = threading.Thread(target=method2, args=(driver,))
    t1.start()
    t1.join()
    t2.start()
    t2.join()

def method1(driver):
    js = " window.open('https://weibo.com/u/5523843379')"
    driver.execute_script(js)
    try:
        WebDriverWait(driver,10).until(
            lambda x: x.find_element_by_id('Pl_Core_UserInfo__6').find_element_by_css_selector('a.WB_cardmore.S_txt1.S_line1.clearfix')).click()
    except Exception:
        print("1")


def method2(driver):
    js = " window.open('https://weibo.com/u/5523843379')"
    driver.execute_script(js)
    driver.find_elements_by_css_selector('span.S_txt1.t_link')[1].click()
    print("2")

def do(keywd, pagemax, yourid, yourpwd):
    get_cookie_from_net(yourid, yourpwd)

    '''
    headers = {'cookie': cookie_list}
    req = urllib.request.Request('https://weibo.com/', headers=headers)
    response = urllib.request.urlopen(req)
    text = response.read().decode('utf-8')
    return text
    '''
