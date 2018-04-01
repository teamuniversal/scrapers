import requests,time
import re
import xbmc, xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
from ..modules import cfscrape
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class allrelease(Scraper):
    domains = ['http://allrls.co']
    name = "allreleases"
    sources = []

    def __init__(self):
        self.base_link = 'http://allrls.co'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time()



    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                     
                                                                                        

            start_url = '%s/?s=%s&go=Search' %(self.base_link,search_id.replace(' ','+'))         
            #print '::::::::::::: START URL '+start_url                                  
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            match = re.compile('<h2 class="entry-title">.+?href="(.+?)".+?rel="bookmark">(.+?)</a>',re.DOTALL).findall(html) 
            for item_url, name in match:
                if year in name:
                   #print name
                    if clean_title(search_id).lower() in clean_title(name).lower():
                        #print item_url
                        self.get_source(item_url)                                       
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources
               

            
    def get_source(self,item_url):
        try:
            headers = {'User-Agent':random_agent()}
            OPEN = self.scraper.get(item_url,headers=headers,timeout=5).content             

            block = re.compile('<div class="entry-content">(.+?)</div><!-- .entry-content -->',re.DOTALL).findall(OPEN)
            Endlinks = re.compile('href=(.+?) ',re.DOTALL).findall(str(block))
            iframe = re.compile('<IFRAME SRC=(.*?) ')
            count = 0     
            for link in Endlinks:
                if link.endswith('.mkv') or link.endswith('.html'):
                    print link
                    if '1080' in link:
                        label = '1080p'
                    elif '720' in link:
                        label = '720p'
                    else:
                        label = 'SD'
                    host = link.split('//')[1].replace('www.','')
                    hostname = host.split('/')[0].title()
                    count +=1
                    self.sources.append({'source': hostname,'quality': label,'scraper': self.name,'url': link,'direct': False, 'debridonly': True})
            for link in iframe:
                if '1080' in link:
                    label = '1080p'
                elif '720' in link:
                    label = '720p'
                else:
                    label = 'SD'
                host = link.split('//')[1].replace('www.','')
                hostname = host.split('/')[0].title()
                count +=1
                self.sources.append({'source': hostname,'quality': label,'scraper': self.name,'url': link,'direct': False})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count) 
        except:
            pass
#allrelease().scrape_movie('Justice League', '2017','')