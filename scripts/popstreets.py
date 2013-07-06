import sys

from bs4 import BeautifulSoup
import urllib
import urllib2

import httplib

from communities import communities
from streets import streets

def getcommunities():
    
    coms = []
    coms.append((42,"Brighton"))
    coms.append((45,"Brockport"))
    coms.append((46,"Chili"))
    coms.append((47,"Churchville"))
    coms.append((48,"Clarkson"))
    coms.append((50,"East Rochester"))
    coms.append((51,"Fairport"))
    coms.append((52,"Gates"))
    coms.append((53,"Greece"))
    coms.append((25,"Hamlin"))
    coms.append((54,"Henrietta"))
    coms.append((56,"Hilton"))
    coms.append((55,"Honeoye Falls"))
    coms.append((57,"Irondequoit"))
    coms.append((58,"Mendon"))
    coms.append((59,"Ogden"))
    coms.append((60,"Parma"))
    coms.append((61,"Penfield"))
    coms.append((62,"Perinton"))
    coms.append((63,"Pittsford Town"))
    coms.append((64,"Pittsford Village"))
    coms.append((65,"Riga"))
    coms.append((66,"Rochester"))
    coms.append((67,"Rush"))
    coms.append((68,"Scottsville"))
    coms.append((69,"Spencerport"))
    coms.append((70,"Sweden"))
    coms.append((101,"TEST comsMUNITY"))
    coms.append((73,"Webster Town"))
    coms.append((74,"Webster Village"))
    coms.append((75,"Wheatland"))
    return coms

def savecommunity(com):
    c = communities()
    hrid,name = com
    cid = c.add(name,hrid)
    return cid

def getstreets(hrid):
    streets = []

    host = "secure.hyper-reach.com"
    port = 80
    url = "/comsignup-loadstreets.jsp?community={0}".format(hrid)

    conn = httplib.HTTPConnection(host,80)
    req = conn.request("GET", url)
    resp = conn.getresponse()
    html = resp.read()
    soup = BeautifulSoup(html)

    tags = soup.find_all('street')
    for tag in tags:
        streets.append((tag['id'],tag['name']))

    return streets

def savestreets(cid,thestreets):
    s = streets()
    for street in thestreets:
        sid,rawname = street
        name = " ".join(rawname.split(" ")[:-1])
        roadtype = rawname.split(" ")[-1]
        print "raw: {0}, road: {1}, type: {2}".format(rawname,name,roadtype)
        s.add(rawname,name,roadtype,cid)

def main():
    coms = getcommunities()
    for com in coms:
        cid = savecommunity(com)
        hrid,name = com
        streets = getstreets(hrid)
        savestreets(cid,streets)

main()


