from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import feedparser, xbmcplugin, re

feed = feedparser.parse('http://hockeystreams.com/rss/archives.php')
username = xbmcplugin.getSetting('username')
password = xbmcplugin.getSetting('password')

titleDesc = {}
c = 0

for i in feed['entries']:
    title = feed.entries[c].title
    description = feed.entries[c].description
    titleDesc[title] = description
    c += 1

rawData = []

for i in titleDesc.values():
    rawData.append(i)

rawData = str(rawData)
match = re.compile('<a href="(.+?)">').findall(rawData)
print 'match: %s' % match

def cleanRawData(link,dictionary):
    a = link.split('/')
    b = a[5]
    c = re.sub('_',' ',b)
    dictionary[c] = link

hdp = []
hd  = []
hq  = []

gamelinkhdp = {}
gamelinkhd  = {}
gamelinkhq  = {}

for i in match:
    if i[-12:] == 'hi-qual-plus':
        hdp.append(i)                   ## appends directlink to hdp
        cleanRawData(i,gamelinkhdp)     ## creates dict with game,direct
    elif i[-7:] == 'hi-qual':
        hd.append(i)
        cleanRawData(i,gamelinkhd)
    else:
        hq.append(i)
        cleanRawData(i,gamelinkhq)

directlinkshdp = {}
directlinkshd  = {}
directlinkshq  = {}

def getDirectLinks(game,url,usr,pwd,dictToPop):
    ## login
    br = Browser()
    br.open(url)
    br.select_form(nr=0)
    br['username'] = usr
    br['password'] = pwd
    br.submit()
    ## get html
    resp = br.open(url)
    html = resp.read()
    soup = BeautifulSoup(''.join(html))
    find = soup.findAll('input')
    for test in find:
        if 'text' in test.get('type',''):
            direct = str(test['value'])
            dictToPop[game] = direct
                              
def popDirectDicts(which):
    if which == 'hdp':
        for k,v in gamelinkhdp.iteritems():
            getDirectLinks(k,v,username,password,directlinkshdp)
        return directlinkshdp
    if which == 'hd':
        for k,v in gamelinkhd.iteritems():
            getDirectLinks(k,v,username,password,directlinkshd)
        return directlinkshd
    if which == 'hq':
        for k,v in gamelinkhq.iteritems():
            getDirectLinks(k,v,username,password,directlinkshq)
        return directlinkshq
