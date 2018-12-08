#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
a=raw_input("enter url plz:")
print a
a0=a.split('/')
print a0[2]
def getwhois():
    whois_url = 'https://who.is/whois/'+a0[2]
    r = requests.get(whois_url)
    if r.status_code == requests.codes.ok:
      soup = BeautifulSoup(r.text, 'html.parser')
      stories = soup.find_all('div', class_='col-md-12 queryResponseBodyValue')
      for s in stories:
        print(s.text)
def niz104():
    google_url = 'https://www.google.com.tw/search?q=site:www.104.com.tw+ '
    r = requests.get(google_url+a0[2])
    if r.status_code == requests.codes.ok:
      soup = BeautifulSoup(r.text, 'html.parser')
      items = soup.select('div.g > h3.r > a[href]')
      for i in items:
        #print(i.text)
        companyutf8=i.text.encode('utf8')
        comp=companyutf8.split('＜')
        compfind=comp[0].find('_')
        if compfind>=0:
            i1=comp[0].split('_')
            print i1[1]
            nat(i1[1])
        else:
            print comp[0]
            nat(comp[0])
        break
def nat(compsear):
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
    print len(table)
    for j in range(2):
        table_item = table[j].select("td")[1].text.encode("utf-8").strip()
        ti=table_item.split()
        table_title = table[j].select("td")[0].text.encode("utf-8").strip()
        print table_title+str('   ')+ti[0]
        print('======')
getwhois()
niz104()

    
