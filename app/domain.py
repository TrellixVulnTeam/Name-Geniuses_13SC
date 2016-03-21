import urllib.request
import json
import requests


#for convertkit
#api_key='3kUbDST4L_292qGSZkkr4g'
#api_secret='j0vImPmMEInW5Y30PAYdO41Sris2N332uhy9pIku1-Q'

def checkDomain(domain):    
    headers={ "X-Mashape-Key": "Cdq6jxIk1fmshETR57Cvq1VmH54dp1QRaj7jsnFIKMU0fnht0u","Accept": "application/json" }
    site="https://domainr.p.mashape.com/v1/info?mashape-key=Cdq6jxIk1fmshETR57Cvq1VmH54dp1QRaj7jsnFIKMU0fnht0u&q=%s" % (domain)

    try:
        req = urllib.request.Request(site, headers=headers)
        response = urllib.request.urlopen(req)
        jsondata = response.read()
        data = json.loads(jsondata.decode('utf-8'))
        avail=data['availability']
    except:
        return False
    if avail=="available":
        return True
    else:
        return False
        
def subscribe(email):
    r = requests.post('https://api.convertkit.com/v3/tags/29555/subscribe?api_key=3kUbDST4L_292qGSZkkr4g', data={'email':email})