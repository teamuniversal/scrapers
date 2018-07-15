import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
#User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

class one23movies(Scraper):
    domains = ['https://www1.123movieshub.sc/']
    name = "123Movies"
    sources = []

    def __init__(self):
        self.base_link = 'https://www1.123movieshub.sc'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        

            start_url = '%s/browse-key/%s' %(self.base_link,search_id.replace(' ','+'))         
            print 'scrapercheck - scrape_movie - start_url:  ' + start_url                                  
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            #print html
            match = re.compile('class="ml-item".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html) 
            for item_url1, name in match:
                item_url = item_url1+'watching/?ep=6'
                #print 'scrapertest - scrape_movie - name: '+name
                #print 'scrapertest - scrape_movie - item_url: '+item_url                                                          
                if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                    print 'scrapertest - scrape_movie - Send this URL: ' + item_url                             
                    self.get_source(item_url,title,year,start_time)                                      
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            season_chk = '- Season %s' %(season)
            #print season_chk
            search_id = clean_search(title.lower())
            start_url = '%s/browse-key/%s' %(self.base_link,search_id.replace(' ','+'))
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            match = re.compile('class="ml-item".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for season_url, title in match:
                #print season_url
                if not season_chk in title:
                    continue
                #print 'PASSED season URL### ' +season_url
                episode_grab = '%s' %(episode)
                html = requests.get(season_url,headers=headers,timeout=5).content
                match = re.compile('onclick=\"watching.+?href="(.+?)"',re.DOTALL).findall(html)
                for item_url in match:
                    #print item_url
                    html=requests.get(item_url, headers=headers, timeout=5).content
                    #print html 
                    match = re.compile('<a title=\"Episode (.+?):.+?data-openload="(.+?)"',re.DOTALL).findall(html)
                    for epi, link1 in match:
                        print epi+ ' first grab'
                        if epi .startswith('0'):
                            epi = epi.replace('0','')
                            link = 'https://openload.co/embed/'+link1
                            #print link + ' <<<<>>>>>>> '+epi
                            if epi in episode_grab:
                        
                                #print 'PASSED epicheck ok' + link + ' <<<<?????????>>>>>>> '+epi
                                host = link.split('//')[1].replace('www.','')
                                host = host.split('/')[0].split('.')[0].title()

                                self.sources.append({'source':host, 'quality':'DVD', 'scraper':self.name, 'url':link, 'direct':False})
                return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 



            


    def get_source(self,item_url,title,year,start_time):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content
            Endlinks = re.compile('<strong>Server Openload.+?data-openload="(.+?)"href',re.DOTALL).findall(OPEN)
            #print 'scrapertest - scrape_movie - EndLinks: '+str(Endlinks)
            for link1 in Endlinks:
                link = 'https://openload.co/embed/'+link1 
                #print 'scrapertest - scrape_movie - link: '+str(link)        
                if '1080' in link:
                    qual = '1080p'
                if '720' in link:
                    qual = '720p'
                else:
                    qual = 'SD'
                    count+=1
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    self.sources.append({'source':host, 'quality':qual, 'scraper':self.name, 'url':link, 'direct':False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]
