#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import uniout
import sys
from bs4 import BeautifulSoup
import re
unsafeScore = 0
foo=[]

def searchall(a):
    global unsafeScore ,foo
    unsafeScore = 0
    foo[:] = []
    a0=a.split('/')
    getwhois(a0[2])
    niz104(a0[2])
    print("||SCORE||")
    foo.append(unsafeScore)
    print (unsafeScore)
    print(foo)
    return foo
    
def getwhois(gettext):
    global unsafeScore,foo
    print("original score")
    print(unsafeScore)
    whois_url = 'https://who.is/whois/'+gettext
    r = requests.get(whois_url)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        stories = soup.find_all('div', class_='col-md-12 queryResponseBodyValue')
        lookuptw=0
        lookupdate=0
        for s in stories:
            isTaiwan = s.text.find("Taiwan")
            isTW = s.text.find("Registrant Country: TW")
            expDate = s.text.find("expir")
            ExpDate = s.text.find("Expir")
            upDate = s.text.find('Updated')
            if isTaiwan != -1 or isTW != -1:
                lookuptw=1
        if lookuptw==0:
            print("WARNING: The address this company registerd isn't in Taiwan.")
            unsafeScore += 1.5
        updDate=s.text.find("-",upDate)
        upYear = s.text[updDate-4:updDate]
        if expDate > 0 :
            Date=s.text.find("-",expDate)
            expYear=s.text[Date-4:Date]
        elif ExpDate > 0:
            Date=s.text.find("-",ExpDate)
            expYear=s.text[Date-4:Date]
        else:
            print("WARNING: Can't find the certificate's expiry date of this company.")
            unsafeScore += 2.5
            foo.append(0)
            foo.append(0)
        if expDate > 0 or ExpDate > 0:
            iexpYear = int(expYear)
            iupYear = int(upYear)
            expDay = s.text[Date-4:Date+6]
            upDay = s.text[updDate-4:updDate+6]
            foo.append(upDay)
            foo.append(expDay)
            if iexpYear - iupYear <= 1:
                print("WARNING: The certificate's effective duration is shorter than 1 year.")
                unsafeScore += 1
    
def niz104(gettext):
    global unsafeScore,foo
    google_url = 'https://www.google.com.tw/search?q=site:www.104.com.tw+ '
    r = requests.get(google_url+gettext)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.select('div.g > h3.r > a[href]')
        if items==[]:
            foo.append(0)
            print("WARNING: Can not find the company under this website")
            unsafeScore += 1
        if len(items) <= 3:
            print("WARNING: Can't find the company's registered name.")
            unsafeScore += 1
        for i in items:
            companyutf8=i.text.encode('utf8')
            if companyutf8.find("公司簡介") == -1:
                print("WARNING: Can't find the company's registered name.")
                unsafeScore += 1
                break
            comp=companyutf8.split('＜')
            compfind=comp[0].find('_')
            if compfind>=0:
                i1=comp[0].split('_')
                print (i1[1].decode("utf-8"))
                nat(i1[1])
                foo.append(i1[1].decode("utf-8"))
            else:
                print (comp[0].decode("utf-8"))
                nat(comp[0])
                foo.append(comp[0].decode("utf-8"))
            break

def nat(compsear):
    global unsafeScore
    s = requests.Session()
    s.keep_alive = False
    url = "https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do"
    s.get(url)
    url = "https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do"
    payload = {
                "validatorOpen":"N",
                "rlPermit":"0",
                "qryCond":compsear,
                "infoType":"D",
                "qryType":"cmpyType",
                "cmpyType":"true",
                "isAlive":"all",
    }
    headers= {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer':'https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do'
}
    res=s.post(url,data=payload,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')
    GUI_url = "https://findbiz.nat.gov.tw"+ soup.select(".hover")[0]["href"]
    GUI_res = s.get(GUI_url, headers = headers)
    GUI_soup = BeautifulSoup(GUI_res.text, "lxml")
    table = GUI_soup.select(".padding_bo")[0].select(".table-striped")[0].select("tr")
    #print len(table)
    for j in range(2):
        table_item = table[j].select("td")[1].text.encode("utf-8").strip()
        ti=table_item.split()
        ti0=ti[0].replace('\xc2\xa0',' ')
        table_title = table[j].select("td")[0].text.encode("utf-8").strip()
        print (table_title.decode("utf-8")+str('   ').decode("utf-8")+ti0.decode("utf-8"))
        print('======')
        if j==2 and table_item != "核准設立" or table <= 0:
            print("WARINING: This company doesn't register in goverment.")
            unsafeScore += 1
