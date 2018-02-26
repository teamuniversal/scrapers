import requests
import resolveurl
import re
import xbmcaddon,time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

  
class hdonline(Scraper):
    domains = ['http://watchfullmovie.co']
    name = "WatchFullMovie"
    sources = []

    def __init__(self):
        self.base_link = 'http://watchfullmovie.co'
        if dev_log=='true':
            self.start_time = time.time()                                                   


    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                     
                                                                                        

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print '::::::::::::: START URL '+start_url                                   
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            #print html
            match = re.compile('class="title".+?href="(.+?)">(.+?)</a>',re.DOTALL).findall(html) 
            for item_url, name in match:
                if year in name:
                    #print 'item_url>>>>>>>>>>>>>>'+item_url                                
                    #print 'name>>>>>>>>>>>>>>'+name
                    #print 'year>>>>>>>>>>>>>>'+year
                    if clean_title(search_id).lower() in clean_title(name).lower():                                                                                             # incuding spaces to get both in same format to match if correct
                        #print 'Send this URL> ' + item_url                              
                        self.get_source(item_url)                                       
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

            
    def get_source(self,item_url):
        try:
            #print '>>>>>>>>>>pass>>>>'+item_url
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content
            #print OPEN             
            Endlinks = re.compile('<iframe class=.+?src="(.+?)"',re.DOTALL).findall(OPEN)      
            for link in Endlinks:
                #print '>>>>>>>>>>>>>>>>>>>link' +link
                if 'openload' in link:
                    try:
                        headers = {'User_Agent':User_Agent}
                        get_res=requests.get(link,headers=headers,timeout=5).content
                        rez = re.compile('',re.DOTALL).findall(get_res)[0]
                        if '1080' in rez:
                            qual ='1080p'
                        elif '720p' in rez:
                            qual='720p'
                        else:
                            qual='DVD'
                    except: qual='DVD'
                    self.sources.append({'source': 'Openload','quality': qual,'scraper': self.name,'url': link,'direct': False})
                else:
                    if urlresolver.HostedMediaFile(link):
                        
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        count +=1
                        self.sources.append({'source': host,'quality': 'DVD','scraper': self.name,'url': link,'direct': False})
                
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)
        except:
            pass