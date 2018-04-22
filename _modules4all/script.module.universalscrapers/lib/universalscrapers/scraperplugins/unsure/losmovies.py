import requests, resolveurl
import re
import xbmcaddon, time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

#blocked  BT works vpn
class losmovies(Scraper):
    domains = ['http://los-movies.com']
    name = "losmovies"
    sources = []

    def __init__(self):
        self.base_link = 'http://los-movies.com'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            search_id = clean_search(title.lower())                                     
                                                                                        

            start_url = '%s/search?type=movies&q=%s' %(self.base_link,search_id.replace(' ','+'))         
            print '::::::::::::: START URL '+start_url                                   
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content
            #print html
            
            match = re.compile('class="showRow showRowImage showRowImage"><a href="(.+?)" ><.+?class=".+?">(.+?)<',re.DOTALL).findall(html) 
            for item_url1, name in match:
                item_url= self.base_link+item_url1
                print 'item_url>>>>>>>>>>>>>> '+item_url                                
                print 'name>>>>>>>>>>>>>> '+name
                #if year in item_url:                                                        
                    
                if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                        print 'Send this URL> ' + item_url                              
                        self.get_source(item_url,title,year,season,episode,start_time)                                       
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            
    def get_source(self,item_url,title,year,season,episode,start_time):
        try:
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content  

            Endlinks = re.compile('data-width=.+?>(.+?)</td>',re.DOTALL).findall(OPEN)      
            for link in Endlinks:
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
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)     
        except:
            pass

 
