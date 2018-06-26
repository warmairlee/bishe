from selenium import webdriver
import time,os,sys,urllib.request
import tkinter as tk
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait

# 保存基本信息
def pa(data):
    soup = BeautifulSoup(data, 'lxml')
    datadiv = soup.find('div', id='info_preview')
    title1 = datadiv.find("h4").get_text()
    print(title1)
    datadiv2 = datadiv.find('div', class_='preview_list')
    for datali in datadiv2.find_all('li'):
        title = datali.find('label').get_text().strip()
        title_value = datali.find('div').get_text().strip()
        print(title+title_value)

# 保存相册
def saveimg(driver, sqq):
    driver.switch_to.frame("tphoto")
    driver.find_element_by_class_name("mod-tab-list").find_elements_by_css_selector("li.js-nav-tab")[1].click()
    time.sleep(1)
    if not os.path.exists("text/textqq/" + sqq + "/img"):
        os.mkdir("text/textqq/" + sqq + "/img")
    num = 1
    driver.switch_to.default_content()
    j = 5
    while j >= 0:
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        j -= 1
    time.sleep(1)
    driver.switch_to.frame("tphoto")
    data = driver.page_source
    soup = BeautifulSoup(data, "lxml")
    if soup.find("div", class_="recent_piclist mod-alpha"):
        datadiv = soup.find("div", class_="recent_piclist mod-alpha")
        for datali in datadiv.find_all("li", class_="j-feed-item"):
            datalidiv = datali.find("div", class_="clearfix mod_datelist_bd")
            for dataimg in datalidiv.find_all("li", class_="j-img-item"):
                try:
                    dataimgsrc = dataimg.find("img").get("data-src")
                    req = urllib.request.Request(dataimgsrc)
                    img = urllib.request.urlopen(req).read()
                    f = open("text/textqq/" + sqq + "/img/"+ str(num) + ".jpg", "wb")
                    num += 1
                    f.write(img)
                    f.close()
                except:
                    pass
        print("照片已保存")
    else:
        print("用户无照片")

# 保存留言板
def comment(driver):
    driver.switch_to_frame("app_canvas_frame")
    i = True
    num = 0
    while i == True and num < 10:
        time.sleep(1)
        try:
            WebDriverWait(driver, 3).until(
                lambda x: x.find_element_by_xpath("//*[@id='pager_bottom']/div/p[1]/a[2]"))
            data = driver.page_source
            soup = BeautifulSoup(data, "lxml")
            commentList = soup.find("div", id="commentList")
            dataul = commentList.find("ul", id="ulCommentList")
            if dataul.find_all("li"):
                for li in dataul.find_all("li"):
                    try:
                        datatbody = li.find("tbody").get_text().strip()
                        commenttime = li.find("p", class_="reply_wrap").find("span").get_text().strip()
                        print(datatbody + "    " + commenttime)
                    except:
                        pass
            else:
                print("用户没有好友的留言")
                num = 10
            num += 1
            try:
                WebDriverWait(driver, 3).until(
                    lambda x: x.find_element_by_xpath("//*[@id='pager_bottom']/div/p[1]/a[2]")).click()
            except:
                pass
        except:
            i = False
        print("--------------------------------------------------------")

# 获取说说
def words(driver):

    j = 5
    while j >= 0:
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        j -= 1
    time.sleep(1)
    driver.switch_to.frame("app_canvas_frame")
    data = driver.page_source
    soup = BeautifulSoup(data,"lxml")
    ol = soup.find("ol", id="msgList")

    for li in ol.find_all("li",class_="feed"):
        datadivbd = li.find("div", class_="bd")
        datanickname = datadivbd.find("a").get_text()
        datacontent = datadivbd.find("pre",class_="content").get_text()
        print(datanickname+":"+datacontent)
        datadivmd = li.find("div", class_="md")
        for imgsrc in datadivmd.find_all("img"):
            print(imgsrc.get("src"))
        commentslist = li.find("div", class_="comments_list")
        ul = commentslist.find("ul")
        for comments_content in ul.find_all("div", class_="comments_content"):
            try:
                str = ""
                nickname1 = comments_content.find_all("a", class_="nickname")[0].get_text()
                nickname2 = comments_content.find_all("a", class_="nickname")[1].get_text()
                for comment in comments_content.find_all("span"):
                    if comments_content.find_all("span"):
                        str = str + comment.get_text() + " "
                print("------" + nickname1 + " 回复 " + nickname2 + str)
            except:
                str = ""
                nickname = comments_content.find("a", class_="nickname").get_text()
                for comment in comments_content.find_all("span"):
                    if comments_content.find_all("span"):
                        str = str + comment.get_text() + " "
                print("--- " + nickname + " 回复 " + str)
        print("")



'''提示'''

def message(mess):
    root = tk.Tk()
    root.geometry("100x50")
    root.title('进度提示')
    label = tk.Label(root, text=mess)
    label.pack()
    root.mainloop()



def login(sqq,yourqq,yourpwd):
    url = "https://qzone.qq.com/"

    # browser = webdriver.PhantomJS(r'E:/phantomjs-2.0.0-windows/bin/phantomjs.exe')
    # browser.set_window_size(1920, 1080)
    driver = webdriver.Chrome()
    driver.get(url)
    driver.switch_to.frame("login_frame")
    try:
        WebDriverWait(driver,10).until(
            lambda x: x.find_element_by_id("switcher_plogin")).click()
    except Exception:
        pass

    input_qq = driver.find_element_by_id('u')
    input_qq.send_keys(yourqq)
    time.sleep(0.5)
    input_passwd = driver.find_element_by_id('p')
    input_passwd.send_keys(yourpwd)
    button_submit = driver.find_element_by_id('login_button')
    button_submit.click()
    message('模拟登录成功')
    time.sleep(0.5)

    # 保存基本资料
    infourl = "https://user.qzone.qq.com/" + sqq + "/1"
    driver.get(infourl)
    driver.switch_to.frame("app_canvas_frame")
    driver.find_element_by_id("info_tab").click()
    time.sleep(0.5)
    data = driver.page_source
    if not os.path.exists("text/textqq/"+sqq):
        os.mkdir("text/textqq/"+sqq)
    fo = open("text/textqq/"+sqq+"/基本信息.txt", "w", encoding="utf-8")
    sys.stdout = fo
    try:
        pa(data)
    except:
        print("获取基本资料失败")
    fo.flush()
    fo = open("text/textqq/" + sqq + "/基本信息.txt", "r", encoding="utf-8")
    text = fo.read()
    fo.close()

    
    # 保存照片
    imgurl = "https://user.qzone.qq.com/" + sqq + "/4"
    driver.get(imgurl)
    try:
        saveimg(driver, sqq)
    except:
        print("获取照片失败")

    # 保存留言板
    imgurl = "https://user.qzone.qq.com/" + sqq + "/334"
    driver.get(imgurl)
    if not os.path.exists("text/textqq/" + sqq):
        os.mkdir("text/textqq/" + sqq)
    fo = open("text/textqq/" + sqq + "/留言板.txt", "w", encoding="utf-8")
    sys.stdout = fo
    try:
        comment(driver)
    except:
        print("获取留言板失败")
    fo.flush()
    fo.close()
   
    # 保存说说
    wordsurl = "https://user.qzone.qq.com/" + sqq + "/311"
    driver.get(wordsurl)

    if not os.path.exists("text/textqq/" + sqq):
        os.mkdir("text/textqq/" + sqq)
    fo = open("text/textqq/" + sqq + "/说说.txt", "w", encoding="utf-8")
    sys.stdout = fo
    try:
        words(driver)
    except:
        print("获取说说失败")
    fo.flush()
    fo.close()

    driver.quit()
    return text



