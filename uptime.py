import socket
from urllib2 import urlopen, URLError, HTTPError
from random import randint
from time import sleep
from lxml import etree
import random
import requests

# timeout in seconds
socket.setdefaulttimeout( 4 )

def query( url ):
    try :
        response = urlopen( url )
    except HTTPError, e:
        print 'Error:', str(e.code)
        print 'Url:', url
    except URLError, e:
        print 'Failure:', str(e.reason)
        print 'Url:', url
    else :
        html = response.read()
        if response.getcode() == 200:
            print 'Success:', url
        else:
            print 'Response reached, but wrong status:', response.getcode()
            print 'Url:', url

# urls = []

def scanSitemap( url ):
    r = requests.get(url)
    root = etree.fromstring(r.content)
    print "The number of sitemap tags are {0}".format(len(root))
    for sitemap in root:
        children = sitemap.getchildren()
        query(children[0].text)

        # prevent DDOS attack behavior.. is it enough?
        ran = random.uniform(0.5, 2)
        print ran
        sleep(ran)
