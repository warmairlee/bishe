
import urllib.request
from bs4 import BeautifulSoup
import re,os


'''保存图片'''



num = 1

def saveoneimg(netname,imgurl, imgname):
    try:
        req = urllib.request.Request(imgurl)
        data = urllib.request.urlopen(req).read()
        if (not (os.path.exists('text/textimage/' + netname))):
            os.mkdir('text/textimage/' + netname)
        f = open('text/textimage/'+ netname +'/'+ imgname, 'wb')
        f.write(data)
        f.close()
    except:
        pass

def saveimg(netname,url,flag):
    global num
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    if flag == 1:
        data = response.read().decode('gb2312')
    elif flag == 2:
        data = response.read().decode('gbk')
    elif flag == 3:
        data = response.read().decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    for dataimg in soup.find_all('img', src=re.compile(u'https*://.*')):
        imgurl = dataimg.get('src')
        imgname = str(num)+'.jpg'
        saveoneimg(netname, imgurl, imgname)
        num += 1


def image(url,i,depth,netname):

    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    flag = 0
    try:
        data = response.read().decode('gb2312')
        flag = 1
    except:
        pass
    if flag == 0:
        try:
            data = response.read().decode('gbk')
            if data != '':
                flag = 2
        except:
            pass
    if flag == 0:
        try:
            data = response.read().decode('utf-8')
            flag =3
        except:
            return '解码错误'
    soup = BeautifulSoup(data, 'lxml')
    if i < int(depth):
        i += 1
        for dataa in soup.find_all('a',href=re.compile(u'https*://.*')):
            newurl = dataa.get('href')
            image(newurl,i,depth,netname)
    saveimg(netname,url,flag)
    if i == 1:
        return netname+' 保存完成,'+str(num-1)+'张'


def startimage(url,i,depth,netname):
    global num
    num = 1
    text = image(url, i, depth, netname)
    return text
