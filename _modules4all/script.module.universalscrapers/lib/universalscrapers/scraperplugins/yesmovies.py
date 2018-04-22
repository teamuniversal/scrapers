import re
import requests,time
from BeautifulSoup import BeautifulSoup as bs
from universalscrapers.common import clean_search, random_agent, send_log, error_log
from universalscrapers.scraper import Scraper
import xbmcaddon
import xbmc
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

session = requests.session()

class Yesmovies(Scraper):
    domains = ['yesmovies.co']
    name = "Yesmovies"
    sources = []
    def __init__(self):
        self.base_link = 'http://yesmovies.co'
        self.search = self.base_link+'/?s='
                              
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            start_url = self.search+title.replace(' ','+')
            print start_url
            html = requests.get(start_url,timeout=5).content
            match = re.compile('a class="ml-mask jt".+?".+?title="(.+?)".+?href="(.+?)"').findall(html)
            for name, url in match:
                if clean_search(title).replace(' ','')==clean_search(name).replace(' ',''):
                    epi_url = url[:-1].replace('/series/','/episode/')+ '-%sx%s' %(season,episode)
                    get_fin_url = requests.get(epi_url).content
                    get_fin_regex = re.findall('class="loader_ds">.+?<a href="(.+?)"',get_fin_url)[0]
                    fin_url = epi_url + get_fin_regex
                    self.get_source(fin_url, title, year, season, episode, start_time)
            return self.sources
        except Exception, argument:
            print argument
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            start_url= self.search+title.replace(' ','+')
            #print start_url
            html = requests.get(start_url,timeout=5).content
            #print html
            match = re.compile('a class="ml-mask jt".+?".+?title="(.+?)".+?href="(.+?)"').findall(html)
            for name,url in match:
                print name
                if clean_search(title).replace(' ','')==clean_search(name).replace(' ',''):
                    get_fin_url = requests.get(url).content
                    get_fin_regex = re.findall('class="loader_ds">.+?<a href="(.+?)"',get_fin_url)[0]
                    fin_url = url + get_fin_regex
                    self.get_source(fin_url, title, year, '', '', start_time)
            return self.sources
        except Exception, argument:
            print argument
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def get_source(self,url, title, year, season, episode, start_time):
        try:
#            print url
            get_cookies = session.get(url,timeout=5).content
            cookie_frame = re.findall('<iframe.+?src="(.+?)"',get_cookies)
            for cookie_page in cookie_frame:
 #               print cookie_page
                if 'gomostream' in cookie_page:
  #                  print cookie_page
                    html2 = session.get(cookie_page,allow_redirects=True).content
   #                 print html2
                    get_cookie_info = re.compile("var tc = '(.+?)'.+?url: \"(.+?)\".+?\"_token\": \"(.+?)\".+?function _tsd_tsd_ds\(s\)(.+?)</script>",re.DOTALL).findall(html2)
                    for tokencode, url_to_open,_token,xtokenscript in get_cookie_info:
    #                    print tokencode,xtokenscript, url_to_open,_token
                        x_token = self.get_x_token(tokencode,xtokenscript)
     #                   print x_token
                        headers = {'User-Agent':random_agent(),
                                   'Host':'gomostream.com',
                                   'Referer':cookie_page,
                                   'x-token':x_token}
                        data = {'tokenCode':tokencode,
                                '_token':_token}
                        html3 = session.post(url_to_open,headers=headers,data=data,timeout=5).json()
                        count = 0
                        for playlink in html3:
                            if playlink!='':
                                try:
                                    if playlink[0]==' ':
                                        playlink = playlink[1:]
                                except:
                                    playlink = playlink
                                try:
                                    source = re.findall('//(.+?)/',str(playlink))[0]
                                except:
                                    source = self.name
                                count += 1
                                self.sources.append({'source': source, 'quality': 'HD', 'scraper': self.name, 'url': playlink,'direct': False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)            
        except Exception, argument:        
            xbmc.log('YESMOVIE : sources ' + argument,xbmc.LOGNOTICE)
            print argument
            if dev_log == 'true':
                error_log(self.name,arguemnt)
            return self.sources

    def get_x_token(self,tokencode,xtokenscript):
        #print tokencode,xtokenscript
        start,finish,add1,add2 = re.findall('slice\((.+?),(.+?)\).+?\+ "(.+?)"\+"(.+?)"',str(xtokenscript))[0]
        #print start,finish,add1,add2
        split = tokencode[int(start):int(finish)]
        reverse = split[::-1]
        x_token = str(reverse)+add1+add2
        return x_token

#Yesmovies().scrape_episode('the blacklist', '2013', '2017', '5', '4', '', '')
#Yesmovies().scrape_movie('Deadpool', '2016','')
