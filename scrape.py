import requests
# -*- coding: utf-8 -*-
import csv
from time import sleep
import re
import requests
from BeautifulSoup import BeautifulSoup


output = "brma.csv"
inputs = "postcodes.csv"


def listmaker():
    with open(inputs,'rb') as csvfile:
        linkreader = csv.reader(csvfile, delimiter=str(","), quotechar=str('|'))
        postcodes = list(linkreader)
        return postcodes
        

def main(postcode):
    try:
        requests_url = "https://lha-direct.voa.gov.uk/SearchResults.aspx?Postcode=%s&LHACategory=999&Month=9&Year=2015&SearchPageParameters=true" % postcode
        print requests_url
        response = requests.get(requests_url)
        html = response.content
        soup = BeautifulSoup(html)
        box = soup.find('div', attrs={'class': 'scl_complex brma-rates'})
        text = box.prettify()
        result = re.sub("<.*?>", "", text)
        money = re.findall("£\d+\.\d*",text)

    except:
        result,money = "Failed"
        
    return result,money




def scrape():
    with open(output, 'w') as csvfile:
        fieldnames = ['postcode','shared','onebed','twobed','threebed','fourbed','dump']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        postcodes = listmaker()
        for postcode in postcodes:
            try:
                print "Sleeping 2 second"
                sleep(2)
                scraped,money = main(postcode[0])
                shared = money[0]
                onebed = money[1]
                twobed = money[2]
                threebed = money[3]
                fourbed = money[4]
                dump = scraped
                print postcode[0]
                print shared
                print onebed
                print twobed
                print threebed
                print fourbed
                writer.writerow({'postcode':postcode[0],'shared':shared,'onebed':onebed,'twobed':twobed,'threebed':threebed,'fourbed':fourbed,'dump':dump})
            except:
                writer.writerow({'postcode':postcode[0],'dump':"Error"})
                continue
        csvfile.close()    
    
scrape()
