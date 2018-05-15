
import requests,time
import re,resolveurl
import xbmc, xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
from ..modules import cfscrape
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class allrelease(Scraper):
    domains = ['http://allrls.pw']
    name = "allreleases"
    sources = []

    def __init__(self):
        self.base_link = 'http://bestrls.net'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time()



    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            if not debrid:
                return []
            search_id = clean_search(title.lower())                                     
                                                                                        

            start_url = '%s/?s=%s&go=Search' %(self.base_link,search_id.replace(' ','+'))         
            #print '::::::::::::: START URL '+start_url                                  
            
            headers = {'Referer':self.base_link, 'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            match = re.compile('<h2 class="entry-title">.+?href="(.+?)".+?rel="bookmark">(.+?)</a>',re.DOTALL).findall(html) 
            for item_url, name in match:
                if year in name:
                   #print name
                    if clean_title(search_id).lower() in clean_title(name).lower():
                        print item_url
                        self.get_source(item_url,title,year,'','',start_time)                                       
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return self.sources 
               
    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            if not debrid:
                return []
            season_url = "0%s"%season if len(season)<2 else season
            episode_url = "0%s"%episode if len(episode)<2 else episode
            sea_epi ='s%se%s'%(season_url,episode_url)
            
            start_url = "%s/?s=%s+%s&go=Search" % (self.base_link, title.replace(' ','+').lower(),sea_epi)
            #print ' ##search## %s | %s' %(self.name,start_url)
            
            headers = {'Referer':self.base_link, 'User-Agent':random_agent()}
            link = requests.get(start_url,headers=headers,timeout=5).content
            #print link
            content = re.compile('<h2.+?href="([^"]+)"',re.DOTALL).findall(link)
            for url in content:
                if clean_title(title).lower() in clean_title(url).lower():
                    #print ' ##Item to pass## %s | %s' %(self.name,url)
                    self.get_source(url,title,year,season,episode,start_time)                  
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return self.sources 
            
    def get_source(self,item_url,title,year,season,episode,start_time):
        try:
            headers = {'User-Agent':random_agent()}
            OPEN = self.scraper.get(item_url,headers=headers,timeout=5).content             

            block = re.compile('<div class="entry-content">(.+?)</div><!-- .entry-content -->',re.DOTALL).findall(OPEN)
            Endlinks = re.compile('href=(.+?) target=',re.DOTALL).findall(str(block))
            iframe = re.compile('<IFRAME SRC=(.*?) FRAMEBORDER',re.DOTALL).findall(str(block))
            count = 0     
            for link in Endlinks:
                #if link.endswith('.mkv') or link.endswith('.html'):
                if resolveurl.HostedMediaFile(link).valid_url():
                    if not '.rar' in link:
                        if not '.srt' in link:
                        
                            #print link
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
                send_log(self.name,end_time,count,title,year,season,episode) 
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return self.sources 
#allrelease().scrape_movie('Justice League', '2017','')
