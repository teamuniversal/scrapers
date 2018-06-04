import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc
import xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class tornadomov(Scraper):
    domains = ['http://tornadomovies.cc']
    name = "Tornado Movies"
    sources = []

    def __init__(self):
        self.base_link = 'http://tornadomovies.cc'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print 'scrapercheck - scrape_movie - start_url:  ' + start_url                                  
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            
            match = re.compile('class="ml-item".+?href="(.+?)".+?<h2>(.+?)</h2>',re.DOTALL).findall(html) 
            for item_url1, name in match:
                #print 'scrapercheck - scrape_movie - name: '+name
                item_url = item_url1+'?action=watching'
                #print 'scrapercheck - scrape_movie - item_url: '+item_url                                                           
                if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                    #print 'scrapercheck - scrape_movie - Send this URL: ' + item_url                             
                    self.get_source(item_url,title,year,start_time)                                      
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            season_chk = '-season-%s' %(season)
            search_id = clean_search(title.lower())
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            match = re.compile('class="ml-item".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for season_url, title in match:
                if not season_chk in season_url:
                    continue
                #print 'PASSED season URL### ' +season_url
                episode_grab = 'Episode %s ' %(episode)

                season_url = season_url+'?action=watching'
                html=requests.get(season_url, headers=headers, timeout=5).content
                match = re.compile('class="episode-item.+?href="(.+?)".+?class="icon-play_arrow"></i>(.+?) (..)',re.DOTALL).findall(html)
                for link1, epis,episno in match:
                    epi = epis+' '+episno
                    #print epi + link1
                    if not clean_title(epi).lower() == clean_title(episode_grab).lower():
                        continue
                    #print 'Passed episode > '+epi
                    html = requests.get(link1, headers=headers, timeout=10).content
                    match = re.compile('id="playerMovie".+?src="(.+?)"',re.DOTALL).findall(html)
                    for link in match:
                        #print link
                        if link.startswith('//vidnode.net/'):
                            link = link.replace('//vidnode.net/','https://vidnode.net/')
                            #print 'matched link>>> ' + link
                            host = link.split('//')[1].replace('www.','')
                            host = host.split('/')[0].split('.')[0].title()

                        self.sources.append({'source':host, 'quality':'720p', 'scraper':self.name, 'url':link, 'direct':False})
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
            #print '#1#1#1#1#1#1#1#1#1#1#1#11'+OPEN
            Endlinks1 = re.compile('id="content-embed".+?<iframe src="(.+?)"',re.DOTALL).findall(OPEN)
            for emfile in Endlinks1:
                OPENA = requests.get(emfile,headers=headers,timeout=5).content
                Endlinks = re.compile("//\$\(.+?addiframe\('(.+?)',",re.DOTALL).findall(OPENA)
                for link in Endlinks:
                    #print 'scrapercheck - scrape_movie - link: '+str(link)        
                    if urlresolver.HostedMediaFile(link):
                        count+=1
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        self.sources.append({'source':host, 'quality':'DVD', 'scraper':self.name, 'url':link, 'direct':False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]