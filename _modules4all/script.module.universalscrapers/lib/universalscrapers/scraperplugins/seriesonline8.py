import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class seriesonline8(Scraper):
    domains = ['https://seriesonline8.com']
    name = "SeriesOnline8"
    sources = []

    def __init__(self):
        self.base_link = 'https://seriesonline8.co'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        

            start_url = '%s/movie/search/%s' %(self.base_link,search_id.replace(' ','-'))         
            #print 'series - scrape_movie - start_url:  ' + start_url                                  
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            
            match = re.compile('class="ml-item".+?href="(.+?)".+?alt="(.+?)"',re.DOTALL).findall(html) 
            for item_url1, name in match:
                #print 'series8 - scrape_movie - name: '+name
                item_url = self.base_link+item_url1+'/watching.html'
                #print 'series8 - scrape_movie - item_url: '+item_url                                                           
                if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                    #print 'series8 - scrape_movie - Send this URL: ' + item_url                             
                    self.get_source(item_url,title,year,start_time)                                      
            return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 

    def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()
            season_chk = '-season-%s' %(season)
            #print season_chk
            search_id = clean_search(title.lower())
            start_url = '%s/movie/search/%s' %(self.base_link,search_id.replace(' ','-'))
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            match = re.compile('class="ml-item".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html)
            for season_url, title in match:
                #print season_url
                if not season_chk in season_url:
                    continue
                #print 'PASSED season URL### ' +season_url
                episode_grab = 'Season %s Episode %s ' %(season,episode)

                item_url = self.base_link+season_url+'/watching.html'
                html=requests.get(item_url, headers=headers, timeout=5).content
                match = re.compile('<a title="(.+?)" player-data="(.+?)"',re.DOTALL).findall(html)
                for epi, link in match:
                    epi = epi.split('-')[1].split('-')[0]

                    if not clean_title(epi).lower() == clean_title(episode_grab).lower():
                        continue
                    #print 'Passed episode > '+epi
                    #if link.startswith('://vidnode.net/'):
                        #link = link.replace('://vidnode.net/','https://vidnode.net/')
                    if link.startswith('//vidnode.net/'):
                        link = link.replace('//vidnode.net/','https://vidnode.net/')
                    #print 'matched link>>> ' + link
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()

                    self.sources.append({'source':host, 'quality':'SD', 'scraper':self.name, 'url':link, 'direct':False})
                return self.sources
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument) 



            #self.get_source(item_url,title,year,season,episode,start_time)


    def get_source(self,item_url,title,year,start_time):
        try:
            print 'PASSEDURL >>>>>>'+item_url
            count = 0
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content
            Endlinks = re.compile('class="les-content.+?player-data="(.+?)"',re.DOTALL).findall(OPEN)
            print 'series8 - scrape_movie - EndLinks: '+str(Endlinks)
            for link in Endlinks:
                #print 'series8 - scrape_movie - link: '+str(link)        
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