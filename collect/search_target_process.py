#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import uniout
import sys
from bs4 import BeautifulSoup
import threading
from queue import Queue

def finding_thread(target_icon, soup, queue):
    icon_link = soup.find('a', href=lambda href: href and target_icon in href.lower())
    if not icon_link:
        queue.put(1)
    else:
        queue.put(0)

def work_target_process(id,target_infomation,result_queue):
    print("TArget")
    unsafeScore = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(target_infomation, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    icon_list = ["facebook", "line", "app"]

    nat_queue = Queue()
    threads = []
    for icon in icon_list:
        thread = threading.Thread(target=finding_thread, args=(icon, soup, nat_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    results = []
    while not nat_queue.empty():
        results.append(nat_queue.get())
    unsafeScore = 0
    for result in results:
        unsafeScore += result
    print("TA", unsafeScore)
    target_score_dict = {'target_score': unsafeScore}
    result_queue.put(target_score_dict)
