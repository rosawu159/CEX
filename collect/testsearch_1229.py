#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

unsafeScore = 0
a=raw_input("enter url plz:")
print a
a0=a.split('/')
print a0[2]

def getwhois():
    global unsafeScore
    whois_url = 'https://who.is/whois/'+a0[2]
    r = requests.get(whois_url)
    if r.status_code == requests.codes.ok:
      soup = BeautifulSoup(r.text, 'html.parser')
      stories = soup.find_all('div', class_='col-md-12 queryResponseBodyValue')
      for s in stories:
        print(s.text)

    #check if address is in Taiwan
    isTW = s.text.find('Taiwan')
    if isTW < 0:
        if s.text.find('Registrant Country: TW') < 0:
            print("WARNING: The address this company registerd isn't in Taiwan.")
            unsafeScore += 1

    #check if certificate's expiry date is too short
    expDate = s.text.find('expires on 20')
    upDate = s.text.find('Updated: 20')
    expYear = s.text[expDate+13] + s.text[expDate+14]
    upYear = s.text[upDate+11] + s.text[upDate+12]

    if expDate == -1:
        expDate = s.text.find('Expiration Date: 20')
        if expDate != -1:
            expYear = s.text[expDate+19] + s.text[expDate+20]

    if expDate < 0:
        print("WARNING: Can't find the certificate's expiry date of this company.")
        unsafeScore += 1
    else:
        iexpYear = int(expYear)
        iupYear = int(upYear)
        if iexpYear - iupYear <= 1:
            print("WARNING: The certificate's effective duration is shorter than 1 year.")
            unsafeScore += 1

def niz104():
    google_url = 'https://www.google.com.tw/search?q=site:www.104.com.tw+ '
    r = requests.get(google_url+a0[2])
    if r.status_code == requests.codes.ok:
      print("request ok")
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
        #print(compfind)
        if comp[0] == None:
            print("company not found")
        break
    else:
        print("Company name not found.")
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

print("end of test.")                                    
