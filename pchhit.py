import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import base64


def pa(url):

    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    dataform = soup.find('form',{'id':'searchlistform1'})
    datatable = dataform.find('table')
    for datatr in datatable.find_all('tr'):
        datatd = datatr.find('td')
        dataa = datatd.find('a',{'href':re.compile('^info')})
        if dataa:
            # 标题
            datatitle = dataa.find('span', {'class', 'titlefontstyle106404'}).get_text()
            print('标题：'+datatitle)
            # 链接
            datahref = dataa.get('href')
            href = 'http://www.hhit.edu.cn/'+datahref
            print('链接：'+href)
        #内容
        if datatd.find('span',{'class','contentfontstyle106404'}):
            datacontent = datatd.find('span',{'class','contentfontstyle106404'}).get_text()
            if datacontent:
                print('内容：'+datacontent)
            else:
                print('内容：无')
        #时间
        datatd = datatr.find('td')
        if datatd.find('span', {'class', 'timefontstyle106404'}):
            datatime = datatd.find('span', {'class', 'timefontstyle106404'}).get_text()
            print(datatime)
            print('-----------\r\n')



def pa10(keywd,pagemax):
    keywdb64 = base64.b64encode(keywd.encode('utf-8'))
    keywdb64 = str(keywdb64,'utf-8')
    output = sys.stdout
    fo = open("text/texthhit/hhit"+keywd+".txt", "w",encoding='utf-8')
    sys.stdout = fo
    pagemax = int(pagemax)
    page = 1
    while page <= pagemax:
        page1 = str(page)
        url = u'http://www.hhit.edu.cn/search.jsp?wbtreeid=1022&currentnum='+page1+'&newskeycode2='+keywdb64
        pa(url)
        page = page + 1
    fo.flush()
    sys.stdout = output
    fo = open("text/texthhit/hhit"+keywd+".txt", "r", encoding='utf-8')
    text = fo.read()
    fo.close()
    return text