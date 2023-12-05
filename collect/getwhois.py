import requests
import re
from bs4 import BeautifulSoup

def searching(soup):
    result_dict={}
    keys = ['Name', 'Whois Server', 'Expires On', 'Registered On', 'Updated On']
    bodys = soup.find_all(class_='queryResponseBodyKey')
    for body in bodys:
        if body.text.strip() in keys:
            value = body.find_next(class_='queryResponseBodyValue')
            result_dict[body.text.strip()] = value.text.strip()
    return result_dict

def getwhois(gettext):
    foo = []
    unsafeScore = 0
    whois_url = 'https://who.is/whois/'+gettext
    r = requests.get(whois_url)
    if r.status_code != requests.codes.ok:
        result = "Not Available Now."
        print(result)
        return result
    soup = BeautifulSoup(r.text, 'html.parser')
    infos = searching(soup)
    
    expYear = int(infos['Expires On'][:4])
    upYear = int(infos['Updated On'][:4])
    if expYear-upYear <= 1:
        print("WARNING: The certificate's effective duration is shorter than 1 year.")
        unsafeScore += 1
    return unsafeScore, foo
