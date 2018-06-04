import requests
import re,time
import xbmc, xbmcaddon
from ..scraper import Scraper
from ..jsunpack import unpack
from universalscrapers.common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")
  
class onfreecin(Scraper):
    domains = ['http://www.onlinefreecinema.co'] 
    name = "Free Online Cinema"
    sources = [] 

    def __init__(self):
        self.base_link = 'http://www.onlinefreecinema.co'   
        self.search = '/search/node/'  
    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                     
                                                                                        

            start_url = '%s%s%s' %(self.base_link,self.search,search_id.replace(' ','%20'))       
            #print start_url
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            match = re.compile('class="title search title".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(html)                                                                                                     
            for item_url,name in match:
                #print item_url +'    ><><><><><>   '+name
                if clean_title(search_id).lower() == clean_title(name).lower():     
                    self.get_source(item_url,title,year,start_time,'','')           
                    #print 'passedurl>>>>>>>>>>>>>>>>>>>>>>'+item_url                                                                      
                                                                        
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name,argument) 
               

    # def scrape_episode(self,title, show_year, year, season, episode, imdb, tvdb, debrid = False):
    #         try:    
    #             start_time = time.time()            
    #             search_id = clean_search(title.lower())      
    #             headers={'User-Agent':random_agent()}   
                
    #             html = requests.get(self.start_url,headers=headers,timeout=5).content
    #             Regex = re.compile('<h4>.+?class="link" href="(.+?)" title="(.+?)".+?season="(.+?)".+?episode="(.+?)"',re.DOTALL).findall(html)
    #             for item_url,name, seas, epis in Regex:
    #                 if not clean_title(title).lower() == clean_title(name).lower():             
    #                     continue
    #                 if not season == seas:  
    #                     continue
    #                 if not episode == epis:     
    #                     continue
    #                 self.get_source(item_url,title,year,start_time,season,episode)  
                                                                                   
                    
    #             return self.sources
    #         except Exception, argument:        
    #             if dev_log == 'true':
    #                 error_log(self.name,argument)          
    #             return self.sources
            
    def get_source(self,item_url,title,year,start_time,season,episode):
        try:

            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content             

            Endlinks = re.compile('<IFRAME SRC="(.+?)"',re.DOTALL).findall(OPEN)      
            count = 0                                                                  
            for link in Endlinks:
                print link+'::::::::::::::::::::::::::::'
                html = requests.get(link,headers=headers,timeout=5).content
                packed = packed = re.findall("id='flvplayer'.+?<script type='text/javascript'>(.+?)</script>",html.replace('\\',''),re.DOTALL)
                for item in packed:
                    #print item
                    item = unpack(item)
                    print item
                    item = item.split('file:"')[1].split('",')[0]
                    print item+'>>>>>>>>>>>>>..split?'
                    host = item.split('//')[1].replace('www.','')        
                    hostname = host.split('/')[0].split('.')[0].title() 
                    count +=1 
                    self.sources.append({'source': hostname, 'quality': 'DVD', 'scraper': self.name, 'url': item,'direct': False})    
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year, season=season,episode=episode)              
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument) 
            return self.sources

