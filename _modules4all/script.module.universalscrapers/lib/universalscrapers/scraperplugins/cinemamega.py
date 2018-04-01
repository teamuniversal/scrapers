import re
import requests,time
import base64
import xbmc,xbmcaddon
from ..scraper import Scraper
from ..common import clean_search, clean_title,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
from ..modules import cfscrape


class cinemamega(Scraper):
    domains = ['cinemamega.net']
    name = "CinemaMega"
    sources = []
    def __init__(self):
        self.base_link = 'http://www1.cinemamega.net'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time()
                              
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_url = self.base_link+'/search-movies/'+title.replace(' ','+')+'+season+'+season+'.html'
            html = self.scraper.get(start_url,timeout=3,sleep=10).content
            match = re.compile('<div class="ml-item">.+?href="(.+?)".+?onmouseover.+?<i>(.+?)</i>.+?Release: (.+?)<',re.DOTALL).findall(html)
            for url,name,release_year in match:
                clean_title_,clean_season = re.findall('(.+?): Season (.+?)>',str(name)+'>')[0]
                if clean_title(clean_title_)==clean_title(title) and clean_season == season:
                    html2 = requests.get(url).content
                    match = re.findall('<a class="episode.+?href="(.+?)">(.+?)</a>',html2)
                    for url2,episode_ in match:
                        if episode_ == episode:
                            self.get_source(url2)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources                            

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_url = self.base_link+'/search-movies/'+title.replace(' ','+')+'.html'
            html = self.scraper.get(start_url,timeout=3).content
            #print html
            match = re.compile('<div class="ml-item">.+?href="(.+?)".+?onmouseover.+?<i>(.+?)</i>.+?Release: (.+?)<',re.DOTALL).findall(html)
            for url,name,release_year in match:
                #print url
                if clean_title(name)==clean_title(title) and year == release_year:
                    print url
                    self.get_source(url)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources 
    def get_source(self,link):
        try:
            count = 0
            html = self.scraper.get(link,timeout=3).content
            frame = base64.decodestring(re.findall('Base64.decode.+?"(.+?)"',str(html))[0])
            playlink = re.findall('src="(.+?)"',str(frame))[0]
            source = re.findall('//(.+?)/',str(playlink))[0]
            if 'entervideo' in source:
                html = requests.get(url).content
                m = re.findall('source src="(.+?)"',html)
                for playlink in m:
                    playlink = playlink+'|User-Agent=Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0&'+'Referer='+url
                    sources.append({'source': 'Entervideo', 'quality': 'SD', 'scraper': self.name, 'url': playlink,'direct': True})
                    count +=1
                    if dev_log=='true':
                        end_time = time.time() - self.start_time
                        send_log(self.name,end_time,count)                                  
        except:
            pass


