#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import uniout
import sys
import json
from bs4 import BeautifulSoup
import re
import getwhois
import niz104

def searchall(target_url):
    target_domain=target_url.split('/')
    getwhois_Score = getwhois.getwhois(target_domain[2])
    niz104_Score = niz104.niz104(target_domain[2])
    print("getwhois_Score:", getwhois_Score)
    print("niz104_Score:", getwhois_Score)
    total_score = getwhois_Score + niz104_Score
    print("SCORE:", total_score)
    foo.append(total_score)
    return foo
