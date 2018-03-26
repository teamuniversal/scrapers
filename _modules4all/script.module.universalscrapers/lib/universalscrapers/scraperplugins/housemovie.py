import requests,time
import re, base64
import xbmcaddon
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class housemovie(Scraper):
    domains = ['http://housemovie.to']
    name = "HouseMovie"
    sources = []

    def __init__(self):
        self.base_link = 'http://housemovie.to'
        if dev_log=='true':
            self.start_time = time.time()                                                   

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                      
                                                                                        
            start_url = '%s/search?q=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print '::::::::::::: START URL '+start_url                                   
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            
            match = re.compile('class="item_info".+?href="(.+?)".+?alt="(.+?)">.+?class="item_ganre">(.+?),',re.DOTALL).findall(html) 
            for item_url1, name,rlse in match:
                item_url = self.base_link+item_url1
                #print 'item_url>>>>>>>>>>>>>> '+item_url                                
                #print 'name>>>>>>>>>>>>>> '+name
                #print 'year?>>>>>>>>>>>>>> '+rlse
                if year in rlse:                                                        
                    
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

            Endlinks = re.compile('player_link="(.+?)".+?Quality</span>(.+?)</div>',re.DOTALL).findall(OPEN)      
            for link1,qual in Endlinks:
                link=base64.b64decode(link1)
                #print 'links~~~~~~~~~~~~'+link+'quality'+qual
                
                if '1080' in link:
                    label = '1080p'
                elif '720' in link:
                    label = '720p'
                else:
                    label = qual
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    self.sources.append({'source': host, 'quality': label, 'scraper': self.name, 'url': link,'direct': False})
            Endlinks1 = re.compile('href="" data-type="download".+?data-link="(.+?)".+?Quality</span>(.+?)</div>',re.DOTALL).findall(OPEN)      
            for link1,qual in Endlinks1:
                link2=base64.b64decode(link1)
                dec = re.compile('"link":"(.+?)"').findall(link2)
                for link in dec:
                    link = link.replace('\\','')
                    #print 'links~~~~~~~~~~~~'+link+'quality'+qual
                    
                    if '1080' in link:
                        label = '1080p'
                    elif '720' in link:
                        label = '720p'
                    else:
                        label = qual
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        self.sources.append({'source': host, 'quality': label, 'scraper': self.name, 'url': link,'direct': False, 'debridonly': True}) 
        
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,count)
        except:
            pass
#housemovie().scrape_movie('tomb raider','2018','')
# you will need to regex/split or rename to get host name if required from link unless available on page it self 