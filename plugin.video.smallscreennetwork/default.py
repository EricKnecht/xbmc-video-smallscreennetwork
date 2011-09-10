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

def playEpisode(url):
        video_data = videolink(url)
        liz = xbmcgui.ListItem(video_data['title'], path = video_data['video_url'])
        liz.setInfo(type = "Video", infoLabels = {"Title": video_data['title']})
        liz.setProperty('isPlayable', 'true')
        
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
	
	
def shows():
        req = urllib2.Request(site)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<h2><a href="(.+?)">(.+?) <span>').findall(link)
        
        for href,name in match:
                addDir(name,site+href,1,'',1)
               
      
                       
def episodes(url):
        print "Episodes: " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent',userAgent)
              
        response = urllib2.urlopen(req)
        
        link=response.read()
        soup = BeautifulStoneSoup(link)
        response.close()
        episodes=re.compile('<a href="(.+?)">\s*<img src="(.+?)".*>\s*<h3>(.+?)</h3>').findall(link)
       
        count = len(episodes)
        
                
        prevPage = soup.find('a', text="&lt;")
       
        if( prevPage != None):
                count = count + 1
               
                addDir("<< Previous Page", prevPage.parent['href'], 1, '', count)
		
		
        for href, thumb, name in episodes:
            addLink(name,site+href,site+thumb,count)
		
        nextPage = soup.find('a', text="&gt;")
        
        if( nextPage != None):
              
                addDir("Next Page >>", nextPage.parent['href'], 1, '', count)	

def videolink(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', userAgent)
        response = urllib2.urlopen(req)
        page=response.read()
        response.close()
        video_match = re.compile("file: \"(.+?)\",").findall(page)
        descrip_match = re.compile('<div id="sidebarnarrow">\s*<h2 class="title">(.+?)').findall(page)#</h2>\s*<p>(.+?)<p>
        recipe_match = re.compile('<div class="half"><h4>(.+?)</h4>').findall(page)
        result = {}
        result['video_url'] = video_match[0]
        result['title'] = descrip_match[0]
        #result['descrip'] =  descrip_match[1]
        return result


def addLink(name,  url, icon, count):
        print url
	ok = True
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=3&name=" + urllib.quote_plus(name)
	liz = xbmcgui.ListItem(cleanHTML(name), iconImage = icon, thumbnailImage = icon)
	liz.setInfo(type = "Video", infoLabels = {"Title": cleanHTML(name)})
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

elif mode == 3:
	playEpisode(url)



