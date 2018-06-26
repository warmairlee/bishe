import pymysql
import src.Person as Person
UPLOAD_FOLDER = r"/static/upload"


def saveinfo(Person):  # 增
    name = Person.name
    sex = Person.sex
    age = Person.age
    birthday = Person.birthday
    weibo = Person.weibo
    wbregtime = Person.wbregtime
    QQ = Person.QQ
    phone = Person.phone
    placenow = Person.placenow
    home = Person.home
    email = Person.email
    tip = Person.tip
    photo = Person.photo

    db = pymysql.connect("localhost", "root", "root", "info",  charset="utf8")
    cursor = db.cursor()
    sql = "insert into userinfo" \
          "(name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)" \
          " values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ,'%s')" % \
          (name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo.replace("\\", "/"))
    try:
        cursor.execute(sql)
        db.commit()
    except:
        pass
        db.rollback()
    db.close()


def delete(num):  # 按num删
    db = pymysql.connect("localhost", "root", "root", "info", charset="utf8")
    cursor = db.cursor()
    sql = "delete from userinfo where num = '%d'" % int(num)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


def update(Person):  # 按num改
    db = pymysql.connect("localhost", "root", "root", "info", charset="utf8")
    sql = "update userinfo set name = '%s',sex = '%s',age = '%d',birthday = '%s',weibo = '%s',wbregtime = '%s'," \
          "QQ = '%s',phone = '%s',placenow = '%s',home = '%s',email = '%s',tip = '%s',photo = '%s' where num = '%d'" %\
          (Person.name, Person.sex, int(Person.age), Person.birthday, Person.weibo, Person.wbregtime, Person.QQ, Person.phone, Person.placenow, Person.home, Person.email, Person.tip, Person.photo.replace("\\", "/"), int(Person.num))
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()
    return Person


def info(num):  # 按NUM查
    db = pymysql.connect("localhost", "root", "root", "info", charset="utf8")
    cursor = db.cursor()
    sql = "select * from userinfo where num = '%d'" % int(num)
    cursor.execute(sql)
    row = cursor.fetchone()
    num = row[0]
    name = row[1]
    sex = row[2]
    age = row[3]
    birthday = row[4]
    weibo = row[5]
    wbregtime = row[6]
    QQ = row[7]
    phone = row[8]
    placenow = row[9]
    home = row[10]
    email = row[11]
    tip = row[12]
    photo = row[13]
    p = Person.Person(num, name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)
    db.rollback()
    db.close()
    return p


def findall():  # 查所有
    db = pymysql.connect("localhost", "root", "root", "info", charset='utf8')
    cursor = db.cursor()
    sql = "select * from userinfo"
    plist = []
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        num = row[0]
        name = row[1]
        sex = row[2]
        age = row[3]
        birthday = row[4]
        weibo = row[5]
        wbregtime = row[6]
        QQ = row[7]
        phone = row[8]
        placenow = row[9]
        home = row[10]
        email = row[11]
        tip = row[12]
        photo = row[13]
        p = Person.Person(num, name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)
        plist.append(p)
    db.rollback()
    db.close()
    return plist

def searchbykey(keyname, keyQQ, keyweibo):
    db = pymysql.connect("localhost", "root", "root", "info", charset='utf8')
    cursor = db.cursor()
    keyname = '%' + keyname + '%'
    keyQQ = '%' + keyQQ + '%'
    keyweibo = '%' + keyweibo + '%'
    sql = "select * from userinfo where name like '%s' and  QQ like '%s' and  weibo like '%s'" % (keyname, keyQQ, keyweibo)
    plist = []
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        num = row[0]
        name = row[1]
        sex = row[2]
        age = row[3]
        birthday = row[4]
        weibo = row[5]
        wbregtime = row[6]
        QQ = row[7]
        phone = row[8]
        placenow = row[9]
        home = row[0]
        email = row[11]
        tip = row[12]
        photo = row[13]
        p = Person.Person(num, name, sex, age, birthday, weibo, wbregtime, QQ, phone, placenow, home, email, tip, photo)
        plist.append(p)
    db.rollback()
    db.close()
    return plist
