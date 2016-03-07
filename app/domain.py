import urllib.request
import xml.etree.ElementTree as ET

def checkDomain(domain):    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    key='2d8db11d657074716eba64'


    if domain[0:3]=="www":
        domain=domain[4::]
    site='https://www.namesilo.com/api/checkRegisterAvailability?version=1&type=xml&key=%s&domains=%s' % (key,domain)
    extension=domain.split(".")
    accepted=['com','org','net', 'co', 'info']
    if extension[1] not in accepted:
        return True
    try:
        req = urllib.request.Request(site, headers=hdr)
        response = urllib.request.urlopen(req)
        print(site)
        tree = ET.parse(response)
        root = tree.getroot()
        avail=root[1][2]
        print(avail)
        avail=avail.tag
    except:
        return False
    if avail=="available":
        return True
    else:
        return False
