from selenium import webdriver
import time
import os
from bs4 import BeautifulSoup
import sys
import urllib.request
import re
import xlwt
import io
from PIL import Image, ImageTk
from selenium.webdriver.support.ui import WebDriverWait
import tkinter as tk


'''保存图片'''


def saveimg(keywd, imgurl, imgname):
    try:
        req = urllib.request.Request(imgurl)
        data = urllib.request.urlopen(req).read()
        if (not (os.path.exists('text/textweibo/' + keywd + '/img'))):
            os.mkdir('text/textweibo/' + keywd + '/img')
        f = open('text/textweibo/' + keywd + '/img/' + imgname, 'wb')
        f.write(data)
        f.close()
    except:
        pass



'''爬虫&保存excel'''


def pa(keywd, data, sheet, row):
    soup = BeautifulSoup(data, 'lxml')
    for datadiv in soup.find_all('div', class_='content clearfix'):
        column = 0
        idhref = datadiv.find('a', class_='W_texta W_fb').get('href')
        idnickname = datadiv.find('a', class_='W_texta W_fb').get_text().strip()
        print('博主昵称:' + idnickname)
        sheet.write(row, column, idnickname)
        column += 1
        print('博主主页链接：https:' + idhref)
        sheet.write(row, column, 'https:' + idhref)
        column += 1
        idcontent = datadiv.find('p', class_='comment_txt').get_text().strip()
        print('微博内容：' + idcontent)
        sheet.write(row, column, idcontent)
        column += 1
        idcontentdiv = datadiv.find('div', class_='feed_from W_textb')
        if idcontentdiv.find('a'):
            idcontenthref = idcontentdiv.find('a').get('href')
            if idcontentdiv.find('a').get('title'):
                idcontenttime = idcontentdiv.find('a').get('title')
            else:
                idcontenttime = ''
            print('内容链接：https:' + idcontenthref)
            sheet.write(row, column, 'https:' +idcontenthref)
            column += 1
            print('发布时间：' + idcontenttime)
            sheet.write(row, column, idcontenttime)
        print('-----------\r\n')
        num = 1
        for imgurl in datadiv.find_all('img' ,src=re.compile(u'//ww?')):
            imgurl = 'http:'+imgurl.get('src')
            imgurl = re.sub('square', 'bmiddle', imgurl)
            imgname = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*:：（）|]', '', idcontent[:20]) + str(num)+ '.jpg'
            num = num + 1
            saveimg(keywd, imgurl, imgname)
        row += 1
    return row


'''提示'''

def message(mess):
    root = tk.Tk()
    root.geometry("100x50")
    root.title('进度提示')
    label = tk.Label(root, text=mess)
    label.pack()
    root.mainloop()


'''模拟微博登陆'''


def infosearch(keywd, pagemax, yourid, yourpwd):

    #driver = webdriver.PhantomJS(r'E:/phantomjs-2.0.0-windows/bin/phantomjs.exe')
    #driver.set_window_size(1920, 1080)
    driver = webdriver.Chrome()
    driver.get('https://weibo.com/')

    try:
        WebDriverWait(driver,10).until(
            lambda x: x.find_element_by_xpath('//*[@id="loginname"]')).send_keys(yourid)
    except Exception:
        driver.quit()
        message("未找到账号输入框")

    time.sleep(0.5)
    input_wd = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')
    input_wd.send_keys(yourpwd)
    '''
    checkimg = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/a/img')
    checkurl = checkimg.get_attribute('src')
    if (checkurl != 'about:blank'):
        time.sleep(0.5)
        root = tk.Tk()
        root.geometry("100x50")
        root.title('验证码')
        response = urllib.request.urlopen('https://login.sina.com.cn/cgi/pin.php?r=60143297&s=0&p=yf-bfcb452887cbf7d7dde208d44b73074d96d7')
        data_stream = io.BytesIO(response.read())
        # 以一个PIL图像对象打开
        pil_image = Image.open(data_stream)
        # 把PIL图像对象转变为Tkinter的PhotoImage对象
        tk_image = ImageTk.PhotoImage(pil_image)
        label = tk.Label(root, image=tk_image)
        label.pack()
        print('输入验证码：')
        root.mainloop()
        code = input()
        checkcode = browser.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[3]/div/input')
        checkcode.send_keys(code)
    '''
    button = driver.find_element_by_id('login_form_savestate')
    button.click()
    time.sleep(0.5)
    button_sub = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
    button_sub.click()
    message('模拟登录成功')

    time.sleep(0.5)

    try:
        WebDriverWait(driver,10).until(
            lambda x: x.find_element_by_class_name('W_input')).send_keys(keywd)
    except Exception:
        driver.quit()
        message("未找到搜索栏")

    button_search = driver.find_element_by_class_name('ficon_search')
    button_search.click()
    data = driver.page_source
    message('开始爬取')

    '''保存到txt,excel'''

    output = sys.stdout
    if( not (os.path.exists('text/textweibo/' + keywd) ) ):
        os.mkdir('text/textweibo/' + keywd)
    fo = open('text/textweibo/' + keywd + '/' + keywd + '.txt', 'w', encoding='utf-8')
    sys.stdout = fo


    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(keywd, cell_overwrite_ok=True)
    sheet.write(0, 0, '博主昵称')
    sheet.write(0, 1, '博主主页链接')
    sheet.write(0, 2, '微博内容')
    sheet.write(0, 3, '内容链接')
    sheet.write(0, 4, '发布时间')
    row = 1
    row = pa(keywd, data, sheet, row)

    page = 1
    pagemax = int(pagemax)

    while page < pagemax:
        page += 1
        try:
            button_next = driver.find_element_by_xpath('//a[@class="page next S_txt1 S_line1"]')
            button_next.click()
        except:
            message('共' + str(page-1) + '页')
            page = pagemax
        data = driver.page_source
        row = pa(keywd, data, sheet, row)
    book.save('text/textweibo/' + keywd + '/' + keywd + '.xls')
    fo.flush()
    sys.stdout = output
    fo = open('text/textweibo/' + keywd + '/' + keywd + '.txt', 'r', encoding='utf-8')
    text = fo.read()
    fo.close()
    return text

