import requests
import urlparse
import re
import resolveurl as urlresolver
import xbmc,xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class movdb(Scraper):
    domains = ['https://movdb.net']
    name = "MOVDB"
    sources = []

    def __init__(self):
        self.base_link = 'https://movdb.net'


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        

            start_url = '%s/search?q=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print 'movdb - scrape_movie - start_url:  ' + start_url                                  
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=10).content            
            
            match = re.compile('class="short_entry grid".+?href="(.+?)".+?<b>(.+?)</b>.+?class="year">(.+?)</span>',re.DOTALL).findall(html) 
            for item_url2, name, rls in match:
                item_url1 = item_url2.split('-')[0]
                item_url = item_url1+'/watch.html'
                #print 'movdb - scrape_movie - name: '+name
                #print 'movdb - scrape_movie - item_url: '+item_url                                
                #print 'movdb - scrape_movie - year: '+year
                if year in rls:
                    #print '>>>>>>>>>>>>>>>>>>>>>>>>year'+year                                                       
                    
                    if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                        #print 'movdb - scrape_movie - Send this URL: ' + item_url                             
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
            OPEN = requests.get(item_url,headers=headers,timeout=10).content
            Endlinks = re.compile('id: "player".+?"(.+?)"',re.DOTALL).findall(OPEN)
            #print 'movdb - scrape_movie - EndLinks: '+str(Endlinks)
            for link in Endlinks:
                #print 'movdb - scrape_movie - link: '+str(link)
                if 'movdb' in link:
                    if '1080' in link:
                        qual = '1080p'
                    elif '720' in link:
                        qual = '720p'
                    else:
                        qual = 'DVD'
                    count+=1
                    self.sources.append({'source':'Movdb', 'quality':qual, 'scraper':self.name, 'url':link, 'direct':False})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]