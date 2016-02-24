import urllib.request
import xml.etree.ElementTree as ET


def checkDomain(domain):
  #key='044424ec7338409a9a2819786a0bc148'
  #99.231.108.123
  if domain[0:3]=="www":
    domain=domain[4::]
  site='https://api.namecheap.com/xml.response?ApiUser=JTringer&ApiKey=044424ec7338409a9a2819786a0bc148&UserName=JTringer&Command=namecheap.domains.check&ClientIp=http://www.namegeniuses.com&DomainList=%s' % (domain)

  try:
    response = urllib.request.urlopen(site)
    tree = ET.parse(response)
    root = tree.getroot()
    availdict=root[3][0].attrib
    if availdict['Available'] == "true":
        return True
    else:
        return False
  except:
    return False