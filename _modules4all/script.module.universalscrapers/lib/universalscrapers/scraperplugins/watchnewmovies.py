import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
#logging not working atm.

class watchnewmovies(Scraper):
    domains = ['https://watchnewmovies.ws']
    name = "watchnewmovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://watchnewmovies.ws'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))                                  
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            match = re.compile('<section>.+?href="(.+?)" title="(.+?)">.+?rel="category tag">(.+?)</a>,',re.DOTALL).findall(html) 
            for item_url, name, rls in match:
                name = name.replace('Watch','').split('(')[0]
                if year in rls:                                        
                    if clean_title(search_id).lower() == clean_title(name).lower():                                  
                        self.get_source(item_url,title,year,start_time)                                      
            
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]

            
    def get_source(self,item_url,title,year,start_time):
        try:
            count = 0
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content
            block = re.compile('class="free_links"(.+?)class="coment"',re.DOTALL).findall(OPEN)
            Endlinks = re.compile('<a href="(.+?)" title=',re.DOTALL).findall(str(block))
            for link in Endlinks:
                if link.startswith('//'):
                    link = 'https:'+link
                    if '1080' in link:
                        qual = '1080p'
                    if '720' in link:
                        qual = '720p'
                    else:
                        qual = 'SD'
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        count+=1
                        self.sources.append({'source':host, 'quality':qual, 'scraper':self.name, 'url':link, 'direct':False})
            
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]