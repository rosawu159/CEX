import requests
from bs4 import BeautifulSoup


def getwhois(gettext):
    foo = []
    unsafeScore = 0
    whois_url = 'https://who.is/whois/'+gettext
    r = requests.get(whois_url)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'html.parser')
        stories = soup.find_all('div', class_='col-md-12 queryResponseBodyValue')
        lookuptw = 0
        lookupdate = 0
        for s in stories:
            isTaiwan = s.text.find("Taiwan")
            isTW = s.text.find("Registrant Country: TW")
            expDate = s.text.find("expir")
            ExpDate = s.text.find("Expir")
            upDate = s.text.find('Updated')
            if isTaiwan != -1 or isTW != -1:
                lookuptw = 1
        if lookuptw == 0:
            print("WARNING: The address this company registered isn't in Taiwan.")
            unsafeScore += 1.5
        updDate = s.text.find("-", upDate)
        upYear = s.text[updDate-4:updDate]
        if expDate > 0:
            Date = s.text.find("-", expDate)
            expYear = s.text[Date-4:Date]
        elif ExpDate > 0:
            Date = s.text.find("-", ExpDate)
            expYear = s.text[Date-4:Date]
        else:
            print("WARNING: Can't find the certificate's expiry date of this company.")
            unsafeScore += 2.5
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
    return unsafeScore, foo
