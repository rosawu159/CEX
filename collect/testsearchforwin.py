#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import uniout
import sys
import json

from bs4 import BeautifulSoup
import re
unsafeScore = 0
foo=[]

def searchall(a):
    global unsafeScore ,foo
    unsafeScore = 0
    foo[:] = []
    a0=a.split('/')
    print('a0',a0)
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
    google_url = 'https://www.google.com.tw/search?q=site:www.twincn.com+ '
    r = requests.get(google_url+gettext)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            company_soup = soup.h3.div
        except:
            print("WARNING: Can not find the company under this website")
            unsafeScore += 1
        a = str(company_soup).split(">")
        b = a[1].split()
        nat(b[0])


def nat(compsear):
    global unsafeScore    
    s = requests.Session()
    res=s.get('https://data.gcis.nat.gov.tw/od/data/api')
    try:
        url = 'https://data.gcis.nat.gov.tw/od/data/api/6BBA2268-1367-4B42-9CCA-BC17499EBE8C?$format=json&$filter=Company_Name like '+ compsear +' and Company_Status eq 01&$skip=0&$top=50'
        res=s.get(url)
        print(res)
    except:
        None
    json_data = json.loads(res.text)
    print(json_data[0]['Company_Status_Desc'])
    if json_data[0]['Company_Status_Desc'] != '核准登記':
        print("WARINING: This company doesn't register in goverment.")
        unsafeScore += 1
