import requests
from bs4 import BeautifulSoup


def niz104(gettext):
    unsafeScore = 0
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
        unsafeScore = nat(b[0], unsafeScore)
        return unsafeScore

def nat(compsear, unsafeScore):
    s = requests.Session()
    res=s.get('https://data.gcis.nat.gov.tw/od/data/api')
    try:
        url = 'https://data.gcis.nat.gov.tw/od/data/api/6BBA2268-1367-4B42-9CCA-BC17499EBE8C?$format=json&$filter=Company_Name like '+ compsear +' and Company_Status eq 01&$skip=0&$top=50'
        res=s.get(url)
        print(res)
    except:
        None
    json_data = res.json()
    print(json_data[0]['Company_Status_Desc'])
    if json_data[0]['Company_Status_Desc'] != '核准登記':
        print("WARINING: This company doesn't register in government.")
        unsafeScore += 1
    return unsafeScore
