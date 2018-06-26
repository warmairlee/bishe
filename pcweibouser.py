from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
import sys
import urllib.request
import tkinter as tk
from selenium.webdriver.support.ui import WebDriverWait


global i
# 爬取信息
def pa(data):
    global i
    soup = BeautifulSoup(data, 'lxml')
    datadiv = soup.find('div',class_='WB_frame_c')
    for datadiv2 in datadiv.find_all('div',class_='WB_cardwrap S_bg2'):
        dataul = datadiv2.find('ul')
        for datali in dataul.find_all('li'):
            if datali.find('span',class_='pt_title S_txt2'):
                title1 = datali.find('span',class_='pt_title S_txt2').get_text().strip()
            if datali.find('span',class_='pt_detail'):
                title1_value = datali.find('span',class_='pt_detail').get_text().strip()
                if i == 1:
                    nickname = title1_value
                    return nickname
            print(title1+title1_value)


def saveimg(driver,nickname):
    num = 1
    driver.find_elements_by_css_selector('span.S_txt1.t_link')[1].click()
    driver.get(driver.current_url)
    j = 5
    while j >= 0:
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        j -= 1
    time.sleep(1)
    data = driver.page_source
    soup = BeautifulSoup(data,'lxml')
    datadiv = soup.find("div",class_="PCD_photo_album_v2")
    if datadiv.find_all("ul",class_="photo_album_list clearfix"):
        if not (os.path.exists('text/text_weibo_userinfo/' + nickname + '/img')):
            os.mkdir('text/text_weibo_userinfo/' + nickname + '/img')
        for dataul in datadiv.find_all("ul",class_="photo_album_list clearfix"):
            # 一组照片的发布时间
            imgtime = dataul.find("p",class_="S_txt2 photo_face").get_text().strip()
            for datali in dataul.find_all("li"):
                try:
                    imgurl = 'http:'+datali.find("img").get("src")[0:-12]
                    requst = urllib.request.Request(imgurl)
                    response = urllib.request.urlopen(requst).read()
                    f = open("text/text_weibo_userinfo/" + nickname + "/img/" + imgtime+str(num)+".jpg", "wb")
                    num += 1
                    f.write(response)
                    f.close()
                except:
                    pass
    else:
        print("用户无照片")




'''提示'''

def message(mess):
    root = tk.Tk()
    root.geometry("100x50")
    root.title('进度提示')
    label = tk.Label(root, text=mess)
    label.pack()
    root.mainloop()


'''模拟微博登陆'''


def infosearch(suserid, suserurl, yourid, yourpwd):


    global i
    # 提供链接
    if suserurl != '':
        driver = webdriver.Chrome()
        driver.get(suserurl)

    # 提供用户名
    if suserid != '':
        # driver = webdriver.PhantomJS(r'E:/phantomjs-2.0.0-windows/bin/phantomjs.exe')
        # driver.set_window_size(1920, 1080)
        driver = webdriver.Chrome()
        driver.get('https://weibo.com/')
        try:
            WebDriverWait(driver,10).until(
                lambda x: x.find_element_by_class_name('W_input')).send_keys(suserid)
        except Exception:
            driver.quit()
            message("未找到搜索框")

        button_search = driver.find_element_by_class_name('ficon_search')
        button_search.click()
        try:
            WebDriverWait(driver,10).until(
                lambda x: x.find_element_by_link_text('找人')).click()
        except Exception:
            driver.quit()
            message("未找到导航栏找人")

        try:
            WebDriverWait(driver,10).until(
                lambda x: x.find_element_by_css_selector('a.W_texta.W_fb')).click()
        except Exception:
            message("未找到用户")
        time.sleep(1)
        driver.switch_to_window(driver.window_handles[1])
        time.sleep(1)


    try:
        WebDriverWait(driver,10).until(
            lambda x: x.find_element_by_id('Pl_Core_UserInfo__6').find_element_by_css_selector('a.WB_cardmore.S_txt1.S_line1.clearfix')).click()
    except Exception:
        driver.quit()
        message("未找到详细信息按钮")

    try:
        WebDriverWait(driver,10).until(
            lambda x: x.find_element_by_css_selector('div.item.username.input_wrap').find_element_by_name('username')).send_keys(yourid)
    except Exception:
        driver.quit()
    time.sleep(1)
    driver.find_element_by_css_selector('div.item.password.input_wrap').find_element_by_name('password').send_keys(yourpwd)
    driver.find_elements_by_id("login_form_savestate")[0].click()
    driver.find_elements_by_css_selector("a.W_btn_a.btn_34px")[0].click()
    message("登录成功")

    try:
        WebDriverWait(driver,10).until(
            lambda x: x.find_element_by_id('Pl_Core_UserInfo__6').find_element_by_css_selector('a.WB_cardmore.S_txt1.S_line1.clearfix')).click()
    except Exception:
        message("未找到详细信息按钮")
    driver.get(driver.current_url)
    time.sleep(1)
    data = driver.page_source
    output = sys.stdout
    if suserid != '':
        if not os.path.exists('text/text_weibo_userinfo/' + suserid):
            os.mkdir('text/text_weibo_userinfo/' + suserid)
        fo = open('text/text_weibo_userinfo/' + suserid + '/' + suserid + '.txt', 'w', encoding='utf-8')
        sys.stdout = fo
        i = 2
        pa(data)
        time.sleep(1)
        fo.flush()
        sys.stdout = output
        fo = open('text/text_weibo_userinfo/' + suserid + '/' + suserid + '.txt', 'r', encoding='utf-8')
        text = fo.read()
        fo.close()
        saveimg(driver, suserid)
        driver.quit()
        return text

    else:
        i = 1
        nickname = pa(data)
        if not os.path.exists('text/text_weibo_userinfo/' + nickname):
            os.mkdir('text/text_weibo_userinfo/' + nickname)
        fo = open('text/text_weibo_userinfo/' + nickname + '/' + nickname + '.txt', 'w', encoding='utf-8')
        sys.stdout = fo
        i=2
        pa(data)
        time.sleep(1)
        fo.flush()
        sys.stdout = output
        fo = open('text/text_weibo_userinfo/' + nickname + '/' + nickname + '.txt', 'r', encoding='utf-8')
        text = fo.read()
        fo.close()
        saveimg(driver, nickname)
        driver.quit()
        return text





