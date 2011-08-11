import urllib, urllib2, re
import xbmcplugin, xbmcaddon, xbmcgui
from BeautifulSoup import BeautifulStoneSoup

__plugin__ = "Small Screen Network"
__authors__ = "Eric Knecht"
__credits__ = ""
__version__ = "0.1"
__settings__ = xbmcaddon.Addon(id = 'plugin.video.smallscreennetwork')



userAgent =  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
site = 'http://smallscreennetwork.com'

def addDir(name, url, mode, icon, count):
	ok = True
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
	cleanName = cleanHTML(name)
	
	liz = xbmcgui.ListItem(cleanHTML(name), iconImage = icon, thumbnailImage = icon)
	liz.setInfo(type = "Video", infoLabels = {"Title": name})
	ok = xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, liz, isFolder = True, totalItems = count)
	return ok

def playEpisode(video_url):
        print video_url
        liz = xbmcgui.ListItem(name, path = video_url)
        liz.setInfo(type = "Video", infoLabels = {"Title": name})
        liz.setProperty('isPlayable', 'true')
        
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	#xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER).play(str(video_url), liz)
	
	
def shows():
        req = urllib2.Request(site)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<h2><a href="(.+?)">(.+?) <span>').findall(link)
        
        for href,name in match:
                addDir(name,site+href,1,'',1)
               
      
                       
def episodes(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent',userAgent)
              
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)">\s*<img src="(.+?)".*>\s*<h3>(.+?)</h3>').findall(link)
        for href, thumb, name in match:
            addDir(name,site+href,2,site+thumb,1)

def videolinks(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', userAgent)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile("s1\.addVariable\('file','(.+?)'\);").findall(link)
        video_url = match[0]
        addLink(name,  video_url, url, '', 1)


def addLink(name,  url, referer, icon, count):
        print url
	ok = True
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&referer=" + urllib.quote_plus(referer) + "&mode=3&name=" + urllib.quote_plus(name)
	liz = xbmcgui.ListItem(name, iconImage = icon, thumbnailImage = icon)
	liz.setInfo(type = "Video", infoLabels = {"Title": name})
	liz.setProperty('isPlayable', 'true')
	ok = xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, liz, isFolder = False, totalItems = count)
	return ok        
        


def cleanHTML(html):
    return unicode(BeautifulStoneSoup(html, convertEntities=BeautifulStoneSoup.HTML_ENTITIES))

                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass



if mode == None or mode == 0 or url == None or len(url) < 1:
        shows()
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==1:
        episodes(url)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
elif mode==2:
        videolinks(url,name)
	xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing = True)
elif mode == 3:
	playEpisode(url)



