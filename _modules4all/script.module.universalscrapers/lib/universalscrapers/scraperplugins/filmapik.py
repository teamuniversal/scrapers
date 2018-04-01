import requests
import re,time
import xbmc,xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")           
requests.packages.urllib3.disable_warnings()

s = requests.session()
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
                                           
class filmapik(Scraper):
    domains = ['https://www.filmapik.io']
    name = "Filmapik"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.filmapik.io'
        if dev_log=='true':
            self.start_time = time.time() 

                        

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            #print 'start>>>>  '+start_url
            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content

            match = re.compile('data-movie-id=.+?href="(.+?)".+?<h2>(.+?)</h2>',re.DOTALL).findall(html)
            for item_url, name in match:
                #print 'clean name >  '+clean_title(name).lower()
                if not clean_title(search_id).lower() == clean_title(name).lower():
                    continue
                if not year in name:
                    continue
                item_url = item_url + 'play'
                mode = 'movie'
                #print item_url
                self.get_source(item_url,mode)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))

            headers={'User-Agent':User_Agent}
            html = requests.get(start_url,headers=headers,timeout=5).content

            match = re.compile('data-movie-id=.+?href="(.+?)".+?<h2>(.+?)</h2>',re.DOTALL).findall(html)
            for item_url, name in match:
                #print item_url
                if clean_title(search_id).lower() == clean_title(name).lower():
                    item_url =  self.base_link + '/episodes/%s-%sx%s/play' %(search_id.replace(' ','-'),season,episode)
                    #print item_url
                    mode = 'tv'
                    self.get_source(item_url,mode)
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources
            
    def get_source(self,item_url,mode):
        try:
            #print 'cfwd > '+item_url
            headers={'User-Agent':User_Agent}
            OPEN = requests.get(item_url,headers=headers,timeout=20).content
            #print OPEN
            if mode == 'movie':
                match = re.compile('<div class="player_nav" id="referNav">(.+?)<div class="swiper-wrapper" style="padding-bottom: 10px;">',re.DOTALL).findall(OPEN)
            else:
                match = re.compile('<div class="player_nav" id="referNav">(.+?)<div class="movies-list-wrap mlw-category">',re.DOTALL).findall(OPEN)
            Sources = re.compile('href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(match))
            count = 0
            for embFile, server in Sources:
                if not 'G-SHARER'in server:
                    if 'FAST' in server:
                        #print embFile
                        qual = server.replace(' ','').replace('FAST','').replace('360p','')
                        #print qual
                        OPEN1 = requests.get(embFile,headers=headers,timeout=10).content
                        #print OPEN1
                        sources1 = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(OPEN1)[1]
                        #print sources1
                        OPEN2 = requests.get(sources1,headers=headers,timeout=10).content
                        match2 = re.compile('"file":"(.+?)"',re.DOTALL).findall(OPEN2)
                        for link in match2:
                            #print link
                            count +=1
                            self.sources.append({'source': self.name, 'quality': qual, 'scraper': self.name, 'url': link,'direct': False})
                    else:
                        #print embFile
                        qual = 'SD'
                        #print qual
                        OPEN1 = requests.get(embFile,headers=headers,timeout=10).content
                        #print OPEN1
                        sources1 = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(OPEN1)[1]
                        host = sources1.split('//')[1].replace('www.','')
                        host = host.split('/')[0].lower()
                        host = host.split('.')[0]
                        count +=1
                        self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': sources1,'direct': False})

                    if dev_log=='true':
                        end_time = time.time() - self.start_time
                        send_log(self.name,end_time,count)                      
        except:
            pass

#filmapik().scrape_movie('tomb raider', '2018','')
#filmapik().scrape_episode('the resident', '2018', '', '1', '2', '', '')