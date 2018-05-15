import requests, resolveurl
import re
import xbmcaddon,time
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
from universalscrapers.modules import cfscrape
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class seehd(Scraper):
    domains = ['http://www.seehd.pl']
    name = "SeeHD.pl"
    sources = []

    def __init__(self):
        self.base_link = 'http://www.seehd.pl'
        self.scraper = cfscrape.create_scraper()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print '::::::::::::: START URL '+start_url                                   
            
            headers={'User-Agent':random_agent()}
            html = self.scraper.get(start_url,headers=headers,timeout=5).content            
            
            match = re.compile('class="post_thumb".+?href="(.+?)".+?class="thumb_title">(.+?)</h2>',re.DOTALL).findall(html) 
            for item_url, name in match:
                if year in name:
                    namecheck = name.replace('Watch Online','').replace(year,'')
                    if clean_title(title)==clean_title(namecheck):                                                        
                                                  
                        self.get_source(item_url, title, year, start_time)                                       
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            
    def get_source(self,item_url, title, year, start_time):
        try:
            count = 0
            headers={'User-Agent':random_agent()}
            OPEN = self.scraper.get(item_url,headers=headers,timeout=5).content             
            Endlinks = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(OPEN)      
            for link in Endlinks:
                if 'seehd' not in link:      
                    if '1080' in link:
                        label = '1080p'
                    elif '720' in link:
                        label = '720p'
                    else:
                        label = 'SD'
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    count += 1
                    self.sources.append({'source': host, 'quality': label, 'scraper': self.name, 'url': link,'direct': False})

            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
