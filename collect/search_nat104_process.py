#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import uniout
import sys
import json
from bs4 import BeautifulSoup
import re
import niz104


def nat(compsear, unsafeScore):
    s = requests.Session()
    res=s.get('https://data.gcis.nat.gov.tw/od/data/api')
    try:
        url = 'https://data.gcis.nat.gov.tw/od/data/api/6BBA2268-1367-4B42-9CCA-BC17499EBE8C?$format=json&$filter=Company_Name like '+ compsear +' and Company_Status eq 01&$skip=0&$top=50'
        res=s.get(url)
    except:
        None
    json_data = res.json()
    print(json_data[0]['Business_Accounting_NO'])
    print(json_data[0]['Register_Organization_Desc'])
    print(json_data[0]['Company_Setup_Date'])

    if json_data[0]['Company_Status_Desc'] != '核准登記':
        print("WARINING: This company doesn't register in government.")
        unsafeScore += 1
    return unsafeScore

def work_nat104_process(id,target_infomation,result_queue):
    print("NAT")
    target_domain=target_infomation.split('/')

    unsafeScore = 0
    google_url = 'https://www.google.com.tw/search?q=site:www.twincn.com+ '
    r = requests.get(google_url+target_domain[2])
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            company_soup = soup.h3.div
        except:
            print("WARNING: Can not find the company under this website")
            unsafeScore += 1
        a = str(company_soup).split(">")
        b = a[1].split()
        unsafeScore = nat(b[0], unsafeScore)
    print("NAT", unsafeScore)

    result_queue.put(unsafeScore)
