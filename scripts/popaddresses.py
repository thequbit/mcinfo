import sys

import urllib
import urllib2

import simplejson

from streets import streets
from addresses import addresses
from communities import communities

def geocodemq(address):
    key = "Fmjtd%7Cluub2gurll%2C8w%3Do5-9uagq4"
    vals = {'location': address}
    qstr = urllib.urlencode(vals)
    #print "QSTR = '{0}'".format(qstr)
    reqstr = "http://www.mapquestapi.com/geocoding/v1/address?key={0}&outFormat=json&maxResults=1&{1}".format(key,qstr)
    #print "Sending: {0}".format(reqstr)
    _json = simplejson.loads(urllib.urlopen(reqstr).read())
    return _json

def pulldatamq(_json):
    #print _json

    fulladdress = ""
    lat = ""
    lng = ""
    zipcode = ""
    streetnumber = ""
    route = ""
    locality = ""
    state = ""
    country = ""

    try:
        #print _json['results'][0]
        street = _json['results'][0]['locations'][0]['street']
        town = _json['results'][0]['locations'][0]['adminArea5']
        state = _json['results'][0]['locations'][0]['adminArea3']
        zipcode = _json['results'][0]['locations'][0]['postalCode'].split('-')[0]
        lat = _json['results'][0]['locations'][0]['latLng']['lat']
        lng = _json['results'][0]['locations'][0]['latLng']['lng']
        route = " ".join(_json['results'][0]['locations'][0]['street'].split(" ")[1:])
        locality = _json['results'][0]['locations'][0]['adminArea5']
        country = "US"
        fulladdress = "{0}, {1}, {2}, {3}, Monroe County, USA".format(street,town,state,zipcode)
       
        # make sure its really an address
        if _json['results'][0]['locations'][0]['geocodeQuality'] == "ADDRESS":
            valid = True
        else:
            valid = False

    except:
        valid = False

    #print _json['results'][0]['locations'][0]['geocodeQuality']

    retval = valid,fulladdress,lat,lng,zipcode,streetnumber,route,locality,state,country
    #print retval
    return retval

def main():
    s = streets()
    a = addresses()
    c = communities()
    thestreets = s.getall()

    print "[INFO   ] Trying to geocode {0} streets ...".format(len(thestreets))

    for street in thestreets:
        _sid,rawname,_name,_streettype,cid = street
        _cid,community,hrid = c.get(cid)
        badcount = 0
        for num in range(1,4096):
            _addr = "{0} {1}, {2}, Monroe County, NY".format(num,rawname,community)
            if a.checkexists(_addr) == False:
                result = geocodemq(_addr)
                valid,fulladdress,lat,lng,zipcode,streetnumber,route,locality,state,country = pulldatamq(result)
                if valid == True:
                    a.add(_addr,fulladdress,num,route,_streettype,zipcode,community,locality,"Monroe County","New York","NY",lat,lng)
                    print "[INFO   ] Added: {0}".format(fulladdress)
                else:
                    badcount += 1
            else:
                print "[INFO   ] Ignoring duplicate address"
            if badcount == 16:
                print "[WARNING] 16 bad street numbers in a row, giving up on street."
                break

    print "[INFO   ] Done!"

main()
