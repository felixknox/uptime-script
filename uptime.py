import socket, random, requests, json, os, math, datetime, ssl, smtplib
from urllib2 import urlopen, URLError, HTTPError
from email.mime.text import MIMEText
from smtplib import SMTPException
from decimal import Decimal
from time import sleep
from lxml import etree

# timeout in seconds
socket.setdefaulttimeout(5)

global urls
global numTries
global numErrors
numErrors = 0

def query(url) :
    global numTries
    timeout = random.uniform(2, 5)

    print 'query:', url

    try :
        response = urlopen(url)
    except HTTPError, e :
        print 'error:', str(e.code)
        addToErrorLog("Error: " + str(e.code) + "\nUrl: " + url)
        # to many tries, try again after x
        if e.code == 429 :
            # we ignore this call, respect a longer timeout and continue
            if 'retry-after' in e.headers :
                timeout = (Decimal(e.headers["retry-after"]) / 1000) * 2
            else :
                timeout = 5
            
            # call again?
            numTries += 1
            if numTries < 2 :
                sleep(timeout)
                # try again
                query(url)
                return

    except URLError, e :
        if(str(e.reason) == "timed out"):
            # call again?
            numTries += 1
            if numTries < 2 :
                sleep(timeout)
                # try again
                query(url)
                return

        print 'Failure:', str(e.reason)
        addToErrorLog("Failure: " + str(e.reason) + "\nUrl: " + url)
    except ssl.SSLError, e :
        addToErrorLog("SSL failure: " + url)
    else :
        try :
            html = response.read()
            if response.getcode() == 200:
                print 'Success'
            else:
                print 'Response reached, but wrong status:', response.getcode()
                addToErrorLog("Error: " + str(response.getcode()) + "\nUrl: " + url)
        except ssl.SSLError, e :
            # print 'SSL failure:', e
            addToErrorLog("SSL failure: " + url)

    # return timeout
    if math.isnan(timeout):
        timeout = random.uniform(2, 5)

    print '----------------'

    # prevent DDOS attack behavior.. is it enough?
    sleep(timeout)

# clear log
with open('log.txt', 'w') as f:
    f.write('')

def addToErrorLog(message) :
    global numErrors
    numErrors += 1

    with open('log.txt', 'a') as f:
        f.write(message + '\n---\n')

# sitemap fetching and parsing
def scanSitemap(url) :
    root = None
    try :
        r = requests.get(url)
        root = etree.fromstring(r.content)
    except :
        print "Can't get sitemap:", url
        addToErrorLog("Can't get sitemap: " + url)

    if root != None:
        print "The number of sitemap tags are {0}".format(len(root))
        for sitemap in root:
            children = sitemap.getchildren()
            urls.append(children[0].text)

# open config file
with open('config.json') as config:
    config = json.load(config)

urls = [];
# sitemaps.json is a file that shouldn't be commitet
def run():
    global urls
    global numTries
    global config

    # pretty print date, so we now when the last time we ran the script was.
    mylist = []
    today = datetime.date.today()
    mylist.append(today)

    addToErrorLog("Log date: " + str(mylist[0]))
    print "Uptime check: " + str(mylist[0])

    # add urls from sitemaps
    for sitemap in config['sitemaps']:
        scanSitemap(sitemap)

    # add individual urls
    for individualUrl in config['urls']:
        urls.append(individualUrl)

    for url in urls:
        numTries = 0
        query(url)

    # build result file and notify when build.
    text = "Uptime done"
    if numErrors > 0 :
        title = "Errors detected(" + str(numErrors) + "), check log"
    else :
        title = "No errors detected"

    # notify
    os.system("""
      osascript -e 'display notification "{}" with title "{}"'
      """.format(title, text))

    sendStatus()

    # loop every x
    loopTime = int(config['loop-time'])
    print "Waiting " + str(loopTime) + " seconds before next uptime check"
    sleep(loopTime)
    run()

run()

def sendStatus():
    global config

    with open("log.txt") as f:
        msg = f.read().rstrip("\n")

    sender = 'noreply@oneeyeopen.io'
    receivers = ['felix@oneeyeopen.io']

    today = datetime.date.today()

    msg = MIMEText(msg)
    msg['Content-Type'] = 'text/html'
    msg['Subject'] = 'From: ' + str(today)
    msg['From'] = 'Uptime robot <noreply@oneeyeopen.io>'
    msg['To'] = 'Who ever is in charge <felix@oneeyeopen.io>'

    try:
       smtpObj = smtplib.SMTP(config["smtp-server"], int(config["smtp-port"]))
       smtpObj.starttls()
       smtpObj.login(str(config["smtp-user"]), str(config["smtp-password"]))
       smtpObj.sendmail(sender, receivers, msg.as_string())
       print "Successfully sent email"
    except SMTPException, e:
       print "Error: unable to send email\n"
       print vars(e)

