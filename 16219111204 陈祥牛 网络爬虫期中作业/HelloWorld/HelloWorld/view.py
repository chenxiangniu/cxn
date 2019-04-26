from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pymysql
import time
from selenium import webdriver

def hello(request):
    ulist=Mysqlfind()
    return render(request, 'hello.html',{'movie':ulist})
def hello1(request):
        '''key='手机'
        url='https://search.jd.com/Search?keyword='+key+'&enc=utf-8'
        ulists=[]
        ulists=dgetText(url)
        dSave(ulists)'''
        ulist=dMysqlfind()
        return render(request, 'base.html',{'phone':ulist})
def Mysqlfind():
    db=pymysql.connect(host="localhost",user="root",password="admin",database="test",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    cursor=db.cursor()
    cursor.execute("select * from mymovie")
    ulist=cursor.fetchall()
    cursor.close()
    db.close()
    return ulist

def getHTMLtext(url,flag):
    try:
        if(flag==0):
                kk={}
        else:
                kk={'start':flag,'filter':''}
        r=requests.get(url,params=kk)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return ""

def getText(ulist,html):
    soup=BeautifulSoup(html,"html.parser")
    a=soup.find('ol',attrs={'class':'grid_view'})
    
    for flag in a.find_all('li'):
        s={}
        hd=flag.find('div',attrs={'class':'hd'})
        name=hd.find('span',attrs={'class':'title'}).getText()
        s['Moviename']=name
        grade=flag.find('span',attrs={'class':'rating_num'}).getText()
        s['Grade']=grade
        star=flag.find('div',attrs={'class':'star'})
        pj=star.find_all('span')[-1].getText()
        s['pj']=pj
        dp=flag.find('span',attrs={'class':'inq'})
        if(dp):
                s['dp']=dp.getText()
        else:
                s['dp']='无短评'
        
        ulist.append(s)

    
def Save():
        url='https://movie.douban.com/top250'
        flag=0
        while flag<250:
            html=getHTMLtext(url,flag)
            time.sleep(2)
            ulist=[]
            getText(ulist,html)
            try:
                db=pymysql.connect(host="localhost",user="root",password="admin",database="test",charset="utf8")
                cursor=db.cursor()
                ls={}
                for ls in ulist:
                        cursor.execute("insert into mymovie(Moviename,Grade,pj,dp) values(%s,%s,%s,%s)",(ls['Moviename'],ls['Grade'],ls['pj'],ls['dp'])) 
                        db.commit()
                cursor.close()
                db.close()
            except:
                print("错误！")
            flag=flag+25

def dgetText(url):
    driver = webdriver.Chrome()
    driver.get(url)
    for i in range(10):
        driver.execute_script("var q=document.documentElement.scrollTop={0}".format(i*1000))
        time.sleep(1)
    searchprice=driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li/div/div[3]/strong/i')
    searchname=driver.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li/div/div[4]/a/em')
    names=[]
    for a in searchname:
        name=a.text
        names.append(name)
    prices=[]
    for c in searchprice:
        price=c.text
        prices.append(price)
    ulists=[]
    flag=0
    for b in names:
        ulist={}
        ulist['name']=b
        ulist['price']=prices[flag]
        flag=flag+1
        ulists.append(ulist)
    return ulists
def dSave(ulist):
        try:
                db=pymysql.connect(host="localhost",user="root",password="admin",database="test",charset="utf8")
                cursor=db.cursor()
                ls={}
                for ls in ulist:
                        cursor.execute("insert into Myphone(name,price) values(%s,%s)",(ls['name'],ls['price']))
                        db.commit()
                cursor.close()
                db.close()
        except:
                print("错误！")
def dMysqlfind():
    db=pymysql.connect(host="localhost",user="root",password="admin",database="test",charset="utf8",cursorclass=pymysql.cursors.DictCursor)
    cursor=db.cursor()
    cursor.execute("select * from Myphone")
    ulist=cursor.fetchall()
    cursor.close()
    db.close()
    return ulist