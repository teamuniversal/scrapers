import re
import requests
import xbmc,time
import urllib
from ..scraper import Scraper
from ..common import clean_title,clean_search
session = requests.Session()
from universalscrapers.modules import cfscrape
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

# cant get post search works in idle 

class hubmovie(Scraper):
    domains = ['http://hubmovie.cc']
    name = "Hubmovie"
    sources = []

    def __init__(self):
        self.base_link = 'http://hubmovie.cc'
        self.sources = []
        self.scraper = cfscrape.create_scraper()

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s/pages/search2/%s' %(self.base_link,search_id.replace(' ','%20'))
            #print 'SEARCH url > '+start_url
            headers = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','accept-encoding':'gzip, deflate','accept-language':'en-US,en;q=0.9','content-type':'text/html',
                       'User-Agent':User_Agent,
                       'origin':self.base_link,'referer':self.base_link,'x-requested-with':'XMLHttpRequest'}
            response = self.scraper.get(self.base_link,headers=headers,timeout=5)
            html = self.scraper.get(start_url,headers=headers,timeout=5).content
            #print html
            page = html.split('<div id="movies_cont">')[1]
            Regex = re.compile('href="(.+?)".+?<h1>(.+?)</h1>.+?class="poster_tag">(.+?)</li>',re.DOTALL).findall(page)
            for item_url,name,date in Regex:
                #print '%s %s %s' %(item_url,name,date)
                if clean_title(title).lower() == clean_title(name).lower():
                    if year in date:
                        movie_link = item_url.replace('.',self.base_link)
                        print 'CHECK here '+movie_link
                        self.get_source(movie_link,title,year,'','',start_time)
                
            return self.sources
        except Exception, argument:
            return self.sources

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())
            start_url = '%s/pages/search/%s' %(self.base_link,search_id.replace(' ','%20'))
            #print 'SEARCH url > '+start_url
            headers = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','accept-encoding':'gzip, deflate','accept-language':'en-US,en;q=0.9','content-type':'text/html',
                       'User-Agent':User_Agent,
                       'origin':self.base_link,'referer':self.base_link,'x-requested-with':'XMLHttpRequest'}
            response = self.scraper.get(self.base_link,headers=headers,timeout=5)
            html = self.scraper.get(start_url,headers=headers,timeout=5).content
            page = html.split('<div id="movies_cont">')[1]
            Regex = re.compile('href="(.+?)".+?<h1>(.+?)</h1>',re.DOTALL).findall(page)
            for item_url,name in Regex:
                if clean_title(title).lower() == clean_title(name).lower():
                    movie_link = item_url.replace('.',self.base_link)
                    movie_link = movie_link + '/season-%s-episode-%s' %(season,episode)
                    self.get_source(movie_link,title,year,season,episode,start_time)
                
            return self.sources
        except Exception, argument:
            return self.sources

    def get_source(self,movie_link,title,year,season,episode,start_time):
        try:
            print ':::::::::::::::::::::::'+movie_link
            headers = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','accept-encoding':'gzip, deflate','accept-language':'en-US,en;q=0.9','content-type':'text/html',
                       'User-Agent':User_Agent,
                       'origin':self.base_link,'referer':self.base_link,'x-requested-with':'XMLHttpRequest'}
            #response = session.get(self.base_link,headers=headers,timeout=5)
            html = self.scraper.get(movie_link,headers=headers,timeout=5).content
            #print 'new'+html
            sources = re.compile('<div class="link_go".+?href="(.+?)"',re.DOTALL).findall(html)
            for link in sources:
                #print link
                if 'openload' in link:
                    headers = {'User_Agent':User_Agent}
                    get_res=requests.get(link,headers=headers,timeout=5).content
                    rez = re.compile('description" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                    if '1080p' in rez:
                        qual = '1080p'
                    elif '720p' in rez:
                        qual='720p'
                    else:
                        qual='DVD'
                else: qual = 'DVD'
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                self.sources.append({'source': host,'quality': qual,'scraper': self.name,'url': link,'direct': False})
            end_time = time.time()
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)
        except:
            pass
