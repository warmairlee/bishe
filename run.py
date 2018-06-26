from flask import Flask, request, render_template, session
import pchtml
import pchhit
import pcweibo
import pcbaidu
import pcimage
import pcqqinfo
import pcweibouser
import Case
import random
import os
import src.Person as Person

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/index',methods=['POST','GET'])
@app.route('/',methods=['POST','GET'])
def index():
    return render_template('index.html')

# 爬网页源代码
@app.route('/pcstart',methods=['POST','GET'])
@app.route('/pchtml',methods=['POST','GET'])
def pcstart():
    data = ''
    if request.method=='POST':
        if "sub" in request.form:
            if request.form['url'] != '':
                url = request.form['url']
                session['url'] = url
                data = pchtml.pa(url)
                return render_template('pchtml.html', data=data ,url=session.get('url'))
            else:
                error = "url is error"
                return render_template('pchtml.html', data=error)
        elif "sav" in request.form:
            fo = open("texthtml.txt", "wb")
            data = request.form['data']
            fo.write(data.encode('utf-8'))
            fo.close()
    if 'url' in session:
        url = session.get('url')
    else:
        url = ''
    return render_template('pchtml.html', data=data,url=url)


# 爬淮工
@app.route('/pchh',methods=['POST','GET'])
def pchh():
    data = ''
    if request.method=='POST':
        if request.form['keywd'] != '':
            if request.form['pagemax'] != '':
                pagemax = request.form['pagemax']
            else:
                pagemax = 1
            keywd = request.form['keywd']
            data = pchhit.pa10(keywd,pagemax)
            return render_template('pchhit.html',data=data ,keywd =keywd , pagemax = pagemax)
        else:
            data = '关键词为空'
            return render_template('pchhit.html', data=data)
    return render_template('pchhit.html', data=data)

# 爬微博
@app.route('/pcwb',methods=['POST','GET'])
def pcwb():
    data = ''
    if request.method == "POST":
        if request.form['keywd'] != '':
            keywd = request.form['keywd']
            if request.form['yourid'] != '' and request.form['yourpwd'] != '':
                yourid = request.form['yourid']
                yourpwd = request.form['yourpwd']
                if request.form['pagemax'] != '':
                    pagemax = request.form['pagemax']
                else:
                    pagemax = 1
                data = pcweibo.infosearch(keywd,pagemax,yourid,yourpwd)
                # data = pcweibo2.do(keywd,pagemax,yourid,yourpwd)
                return render_template('pcweibo.html',data=data,keywd = keywd,pagemax = pagemax,yourid=yourid,yourpwd=yourpwd)
            else:
                data = '输入模拟登陆信息'
                return render_template('pcweibo.html', data=data,keywd=keywd)
        else:
            data = '关键词为空'
            return render_template('pcweibo.html', data=data)
    return render_template('pcweibo.html',data=data)

# 爬百度
@app.route('/pcbd',methods=['POST','GET'])
def pcbd():
    data=''
    if request.method=='POST':
        if request.form['keywd'] != '':
            if request.form['pagemax'] != '':
                pagemax = request.form['pagemax']
            else:
                pagemax = 1
            keywd = request.form['keywd']
            data = pcbaidu.baidu(keywd,pagemax)
            return render_template('pcbaidu.html', data = data, keywd = keywd, pagemax = pagemax)
        else:
            data = '关键词为空'
            return render_template('pcbaidu.html',data = data)
    return render_template('pcbaidu.html',data = data)


# 爬网站图片

@app.route('/pcimg',methods=['post','get'])
def pcimg():
    data = ''
    if request.method == 'POST':
        if request.form['url'] != '' and request.form['netname'] != '':
            if request.form['depth'] != '':
                depth = request.form['depth']
            else:
                depth = '1'
            url = request.form['url']
            netname = request.form['netname']
            data = pcimage.startimage(url,1,depth,netname)
            return render_template('pcimage.html', data = data , url = url, depth = depth,netname=netname)
        elif request.form['url'] == '':
            data = '网址为空'
            return render_template('pcimage.html', data=data)
        elif request.form['netname'] != '':
            data = '输入文件夹名称'
            return render_template('pcimage.html',data = data)
    return render_template('pcimage.html',data = data)

@app.route('/pcqq',methods=['post','get'])
def pcqq():
    data = ''
    if request.method == 'POST':
        if request.form['sqq'] != '' and request.form['yourqq'] and request.form['yourpwd'] != '':
            sqq = request.form['sqq']
            yourqq = request.form['yourqq']
            yourpwd = request.form['yourpwd']
            data = pcqqinfo.login(sqq,yourqq,yourpwd)
            return render_template('pcqqinfo.html', data = data , sqq = sqq , yourqq = yourqq , yourpwd = yourpwd)
        else:
            data = '所需内容有空'
            return render_template('pcqqinfo.html', data=data)
    else:
        return render_template('pcqqinfo.html', data=data)


@app.route('/pcwbuser',methods=['post','get'])
def pcwbuser():
    data = ''
    if request.method == 'POST':
        # 提供用户名
        if request.form['suserid'] != '':
            if request.form['yourid'] != '' and request.form['yourpwd'] != '':
              suserid = request.form['suserid']
              suserurl = request.form['suserurl']
              yourid = request.form['yourid']
              yourpwd = request.form['yourpwd']
              data = pcweibouser.infosearch(suserid, suserurl, yourid, yourpwd)
              return render_template('pcweibouser.html', data=data, suserid=suserid, suserurl=suserurl, yourid=yourid, yourpwd=yourpwd)
            else:
                data = '填写模拟登陆信息'
                return render_template('pcweibouser.html', data=data)
        # 提供微博主页链接
        if request.form['suserurl'] != '':
            if request.form['yourid'] and request.form['yourpwd'] != '':
              suserid = request.form['suserid']
              suserurl = request.form['suserurl']
              yourid = request.form['yourid']
              yourpwd = request.form['yourpwd']
              data = pcweibouser.infosearch(suserid, suserurl,yourid,yourpwd)
              return render_template('pcweibouser.html', data=data, suserid=suserid, suserurl=suserurl, yourid=yourid, yourpwd=yourpwd)
            else:
                data = '填写模拟登陆信息'
                return render_template('pcweibouser.html', data=data)
        else:
            data = '用户名或者用户链接必须填一个'
            return render_template('pcweibouser.html', data=data)
    else:
        return render_template('pcweibouser.html', data=data)

# 添加档案


UPLOAD_FOLDER = r"E:\PycharmProjects\bishe\static\upload"
ALLOWED_EXTENSIONS=set(['pdf', 'png', 'jpg', 'jpeg', 'JPG', 'PNG'])


@app.route("/add", methods=["post", "get"])
def add():
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    if request.method == "POST":
        try:
            name = request.form["name"]
            sex = request.form["sex"]
            age = request.form["age"]
            birthday = request.form["birthday"]
            weibo = request.form["weibo"]
            wbregtime = request.form["wbregtime"]
            QQ = request.form["QQ"]
            phone = request.form["phone"]
            placenow = request.form["placenow"]
            home = request.form["home"]
            email = request.form["email"]
            tip = request.form["tip"]
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                filename = str(random.randint(1, 99999)) + name + birthday + ".jpg"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    photo.save(file_path)
                    photo = r"/static/upload/" + filename
                except IOError:
                    return '上传文件失败'
                p = Person.Person("",name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)
                Case.saveinfo(p)
                plist = Case.findall()
                return render_template("viewall.html", plist=plist)
            else:
                photo = r"/static/upload/default.jpg"
                p = Person.Person("",name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)
                Case.saveinfo(p)
                plist = Case.findall()
                return render_template("viewall.html", plist=plist)
        except:
            name = request.form["name"]
            sex = request.form["sex"]
            age = request.form["age"]
            birthday = request.form["birthday"]
            weibo = request.form["weibo"]
            wbregtime = request.form["wbregtime"]
            QQ = request.form["QQ"]
            phone = request.form["phone"]
            placenow = request.form["placenow"]
            home = request.form["home"]
            email = request.form["email"]
            tip = request.form["tip"]
            photo = r"/static/upload/default.jpg"
            p = Person.Person("", name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)
            Case.saveinfo(p)
            plist = Case.findall()
            return render_template("viewall.html",plist=plist)
    else:
        return render_template('adduser.html')


# 浏览全部档案
@app.route("/view", methods=["POST", "GET"])
def view():
    if request.method == "POST":
        return render_template("viewall.html")
    else:
        plist = Case.findall()
        return render_template("viewall.html", plist=plist)

# 查看详情
@app.route("/more/<num>", methods=["POST", "GET"])
def more(num):
    if request.method == "POST":
        return render_template("moreinfo.html")
    else:
        person = Case.info(num)
        return render_template("moreinfo.html", person=person)

# 更改信息


@app.route("/change/<num>/<oriphoto>", methods=["POST", "GET"])
def change(num,oriphoto):
    if request.method == "POST":
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
        try:
            name = request.form["name"]
            sex = request.form["sex"]
            age = request.form["age"]
            birthday = request.form["birthday"]
            weibo = request.form["weibo"]
            wbregtime = request.form["wbregtime"]
            QQ = request.form["QQ"]
            phone = request.form["phone"]
            placenow = request.form["placenow"]
            home = request.form["home"]
            email = request.form["email"]
            tip = request.form["tip"]
            photo = request.files['photo']
            if photo and allowed_file(photo.filename):
                filename = str(random.randint(1, 99999)) + name + birthday + ".jpg"
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    photo.save(file_path)
                    photo = r"/static/upload/" + filename
                except IOError:
                    return '上传文件失败'
                p = Person.Person(num, name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)
                person = Case.update(p)
                return render_template("moreinfo.html", person=person)
            else:
                photo = r"/static/upload/"+oriphoto
                p = Person.Person(num, name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)
                person = Case.update(p)
                return render_template("moreinfo.html", person=person)
        except:
            name = request.form["name"]
            sex = request.form["sex"]
            age = request.form["age"]
            birthday = request.form["birthday"]
            weibo = request.form["weibo"]
            wbregtime = request.form["wbregtime"]
            QQ = request.form["QQ"]
            phone = request.form["phone"]
            placenow = request.form["placenow"]
            home = request.form["home"]
            email = request.form["email"]
            tip = request.form["tip"]
            photo = r"/static/upload/" + oriphoto
            p = Person.Person(num, name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)
            person = Case.update(p)
            return render_template("moreinfo.html", person=person)
    else:
        person = Case.info(num)
        return render_template("changeinfo.html", person=person)


# 删除信息
@app.route("/delete/<num>", methods=["POST", "GET"])
def delete(num):
    if request.method == "POST":
        plist = Case.findall()
        return render_template("viewall.html", plist=plist)
    else:
        Case.delete(num)
        plist = Case.findall()
        return render_template("viewall.html", plist=plist)


@app.route("/search", methods=["POST", "GET"])  # 搜索栏
def search():
    if request.method == "POST":
        if request.form["keyname"] != "" or request.form["keyQQ"] != "" or request.form["keyweibo"] != "":

            keyname = request.form["keyname"]
            keyQQ = request.form["keyQQ"]
            keyweibo = request.form["keyweibo"]
            plist = Case.searchbykey(keyname, keyQQ, keyweibo)
            return render_template("viewall.html", plist=plist)
        else:
            plist = Case.findall()
            return render_template("viewall.html", plist=plist)
    else:
        plist = Case.findall()
        return render_template("viewall.html", plist=plist)

if __name__ == '__main__':
    app.debug = True
    app.run()