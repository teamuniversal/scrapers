import requests, resolveurl
import re
import xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class filmclub(Scraper):
    domains = ['https://filmclub.tv/']
    name = "FilmClub"
    sources = []

    def __init__(self):
        self.base_link = 'https://filmclub.tv/'
        if dev_log=='true':
            self.start_time = time.time()                                                   

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                      
                                                                                        
            start_url = '%ssearch.php?keywords=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print '::::::::::::: START URL '+start_url                                   
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            
            match = re.compile('class="actionsMenu".+?href="(.+?)".+?title="(.+?)"',re.DOTALL).findall(html) 
            for item_url, name in match:
                #print 'item_url>>>>>>>>>>>>>> '+item_url                                
                #print 'name>>>>>>>>>>>>>> '+name
                if year in name:                                                        
                    
                    if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                        #print 'Send this URL> ' + item_url                              
                        self.get_source(item_url)                                       
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')

            
    def get_source(self,item_url):
        try:
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content             

            Endlinks = re.compile('<a href="https://adf.ly/292141/(.+?)"',re.DOTALL).findall(OPEN)      
            for link in Endlinks:
                    if 'openload'in link:
                        if '1080' in link:
                            label = '1080p'
                        elif '720' in link:
                            label = '720p'
                        else:
                            label = 'SD'
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        self.sources.append({'source': host, 'quality': label, 'scraper': self.name, 'url': link,'direct': True}) 


                    else:
                        if 'vidoza'in link:
                            if '1080' in link:
                                label = '1080p'
                            elif '720' in link:
                                label = '720p'
                            else:
                                label = 'SD'
                            host = link.split('//')[1].replace('www.','')
                            host = host.split('/')[0].split('.')[0].title()
                            self.sources.append({'source': host, 'quality': label, 'scraper': self.name, 'url': link,'direct': True})


            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,count)
        except:
            pass

# you will need to regex/split or rename to get host name if required from link unless available on page it self 