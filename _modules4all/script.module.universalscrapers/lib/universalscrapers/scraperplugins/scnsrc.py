import requests
import re
import xbmcaddon
import time
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
from ..modules import cfscrape

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class scnsrc(Scraper):
    domains = ['http://www.scnsrc.me']
    name = "scnsrc"
    sources = []

    def __init__(self):
        self.base_link = 'http://www.scnsrc.me'
        self.scraper = cfscrape.create_scraper()
        if dev_log=='true':
            self.start_time = time.time()



    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            search_id = clean_search(title.lower())                                     
                                                                                        

            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            # print '::::::::::::: START URL '+start_url                                  
            
            headers={'User-Agent':random_agent()}
            html = self.scraper.get(start_url,headers=headers,timeout=5).content            
            match = re.compile('class="post".+?href="(.+?)".+?class=\'right\'.+?href="(.+?)".+?</div>',re.DOTALL).findall(html) 
            for item_url, name in match:
                name = name.replace('http://www.scnsrc.me/','')
                name = name.replace('/#comments','')
                if year in name:
                    # print '>>>>>>>>>>>>>>'+clean_title(search_id) 
                    # print clean_title(name)
                    if clean_title(search_id).lower() in clean_title(name).lower():                             
                        self.get_source(item_url)                                       
                return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')

    
    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            SS = "0%s"%season if len(season)<2 else season
            EE = "0%s"%episode if len(episode)<2 else episode
            
            search_term = clean_search(title.lower())+' '+'s'+SS+'e'+EE
            search_id = clean_search(title.lower())

            search = '%s/?s=%s'  %(self.base_link,search_term.replace(' ','+'))
            print 'SEARCH > '+search
            contents = self.scraper.get(search,timeout=5).content
            match = re.compile('class="post".+?href="(.+?)".+?class=\'right\'.+?href="(.+?)".+?</div>',re.DOTALL).findall(contents)
            for item_url, name in match:
                name = name.replace('http://www.scnsrc.me/','')
                name = name.replace('/#comments','')
                # if show_year in name:
                if clean_title(search_id).lower() in clean_title(name).lower():
                    print '>>>>>>>>>>'+item_url
                self.get_source(item_url)                                       
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')         

            
    def get_source(self,item_url):
        try:
            headers = {'User-Agent':random_agent()}
            OPEN = self.scraper.get(item_url,headers=headers,timeout=5).content             

            Endlinks = re.compile('<p><a href="(.+?)".+?</a></p>',re.DOTALL).findall(OPEN)      
            count = 0
            for link in Endlinks:
                rar = '.rar'
                if link.endswith('.mkv'):
                    #print link
                    if '1080' in link:
                        label = '1080p'
                    elif '720' in link:
                        label = '720p'
                    else:
                        label = 'SD'
                    host = link.split('//')[1].replace('www.','')
                    hostname = host.split('/')[0].split('.')[0].title()
                    count +=1
                self.sources.append({'source': hostname,'quality': label,'scraper': self.name,'url': link,'direct': False, 'debridonly': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,count)
        except:
            pass
#scnsrc().scrape_movie('Justice League', '2017','')