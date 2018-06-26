import urllib.parse,urllib.request
from bs4 import BeautifulSoup
import re,os,sys
import xlwt

def pa(data,sheet,row):
    request = urllib.request.Request(data)
    response = urllib.request.urlopen(request)
    data = response.read()
    data =data.decode('utf-8')

    soup = BeautifulSoup(data, 'lxml')
    for datadiv in soup.find_all('div',class_=re.compile(u'result.*?c-container.*?')):
        column = 0
        datatitle = datadiv.find('h3',class_=re.compile(u't.*?'))
        datatitlename = datatitle.find('a').get_text().strip()
        datatitleurl = datatitle.find('a').get('href')
        print('标题:'+datatitlename)
        sheet.write(row, column, datatitlename)
        column += 1
        print('链接:'+datatitleurl)
        sheet.write(row, column, datatitleurl)
        column += 1
        if datadiv.find('div',class_='c-abstract'):
            datacontent = datadiv.find('div',class_='c-abstract').get_text()
            print('内容简介:'+datacontent)
            sheet.write(row, column, datacontent)
        print('-----------\r\n')
    row += 1
    return row


def baidu(keywd,pagemax):

    output = sys.stdout
    if (not (os.path.exists('text/textbaidu/' + keywd))):
        os.mkdir('text/textbaidu/' + keywd)
    fo = open('text/textbaidu/' + keywd + '/' + keywd + '.txt', 'w', encoding='utf-8')
    sys.stdout = fo

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(keywd, cell_overwrite_ok=True)
    sheet.write(0, 0, '百度标题')
    sheet.write(0, 1, '链接')
    sheet.write(0, 2, '内容简介')
    row = 1
    keywdenurl = urllib.parse.quote(keywd)
    page = 0
    url = 'http://www.baidu.com/s?wd=' + keywdenurl + '&pn='+str(page*10)
    row = pa(url,sheet,row)
    while page < int(pagemax)-1:
        page += 1
        url = 'http://www.baidu.com/s?wd=' + keywdenurl + '&pn=' + str(page*10)
        row = pa(url, sheet,row)
    if not os.path.exists('text/textbaidu/' + keywd):
        os.mkdir('text/textbaidu/' + keywd)
    book.save('text/textbaidu/' + keywd + '/' + keywd + '.xls')
    fo.flush()
    sys.stdout = output
    fo = open('text/textbaidu/' + keywd + '/' + keywd + '.txt', 'r', encoding='utf-8')
    text = fo.read()
    fo.close()
    return text