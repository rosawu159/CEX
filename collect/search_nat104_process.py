#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import uniout
import sys
import json
from bs4 import BeautifulSoup
import re
import niz104
import threading
from queue import Queue


def nat(compsear, unsafeScore):
    session = requests.Session()
    try:
        url = 'https://data.gcis.nat.gov.tw/od/data/api/6BBA2268-1367-4B42-9CCA-BC17499EBE8C?$format=json&$filter=Company_Name like '+ compsear +' and Company_Status eq 01&$skip=0&$top=50'
        response=session.get(url)
        json_data = response.json()
        print("JR", json_data)
    except:
        None
    if json_data != None:
        nat_dict={}
        nat_dict['Business_NO']=json_data[0]['Business_Accounting_NO']
        nat_dict['Register_Organization']=json_data[0]['Register_Organization_Desc']
        nat_dict['Company_Date']=json_data[0]['Company_Setup_Date']

        if json_data[0]['Company_Status_Desc'] != '核准登記':
            print("WARINING: This company doesn't register in government.")
            unsafeScore += 1
        return unsafeScore, nat_dict



def worker0_thread(nat_dict, queue):
    session = requests.Session()
    url = 'https://eip.fia.gov.tw/OAI/api/businessRegistration/'+nat_dict['Business_NO']
    try:
        response=session.get(url)
    except:
        None
    json_data = response.json()
    print(json_data['businessType'])
    matching_values = [value for key, value in json_data.items() if key.startswith('industryNm')]
    data_dict = {'matching_values': matching_values}
    queue.put(data_dict)

def worker1_thread(nat_dict, queue):
    session = requests.Session()
    url = 'https://data.gcis.nat.gov.tw/od/data/api/236EE382-4942-41A9-BD03-CA0709025E7C?$format=json&$filter=Business_Accounting_NO%20eq%20'+ nat_dict['Business_NO'] +'&$skip=0&$top=50'
    try:
        response=session.get(url)
    except:
        None
    json_data = response.json()
    cmp_business = json_data[0]['Cmp_Business']
    business_item_desc_values = [item['Business_Item_Desc'] for item in cmp_business]
    data_dict = {'matching_values': business_item_desc_values}
    queue.put(data_dict)

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
    else:
        return None
    company_title_soup = str(company_soup).split(">")
    print("company_title_soup", company_title_soup)
    company_title = company_title_soup[1].split()
    unsafeScore, nat_dict = nat(company_title[0], unsafeScore)
    print("NAT", unsafeScore)
    nat_score_dict = {'nat_score': unsafeScore}


    nat_queue = Queue()
    threads = []
    thread_0 = threading.Thread(target=worker0_thread, args=(nat_dict, nat_queue))
    thread_1 = threading.Thread(target=worker1_thread, args=(nat_dict, nat_queue))

    threads.extend([thread_0, thread_1])
    thread_0.start()
    thread_1.start()

    for thread in threads:
        thread.join()
    results = []
    while not nat_queue.empty():
        results.append(nat_queue.get())


    result_queue.put(nat_score_dict)
    result_queue.put(results)
