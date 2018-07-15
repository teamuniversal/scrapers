# -*- coding: utf-8 -*-
# Universal Scrapers
import requests, resolveurl
import re
import xbmcaddon,time
import xbmc
from ..scraper import Scraper
from ..common import clean_title,clean_search,random_agent,send_log,error_log
#from universalscrapers.modules import cfscrape
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class iwatchflix(Scraper):
    domains = ['https://www.iwatchflix.net/']
    name = "iwatchflix"
    sources = []

    def __init__(self):
        self.base_link = 'https://www.iwatchflix.net'
        #self.scraper = cfscrape.create_scraper()

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print '::::::::::::: START URL '+start_url                                   
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            
            match = re.compile('data-movie-id=.+?href="(.+?)".+?<h2>(.+?)</h2>.+?rel="tag">(.+?)</a>',re.DOTALL).findall(html) 
            for item_url, name, date in match:
                if clean_title(title)==clean_title(name):
                    if year == date:
                        #print 'PASS THIS >> '+item_url
                        self.get_source(item_url,title,year)
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        
            start_url = '%s/?s=%s' %(self.base_link,search_id.replace(' ','+'))         
            #print '::::::::::::: START URL '+start_url                                   
            
            season_check = '-season-%s/' %season
            
            headers={'User-Agent':random_agent()}
            html = requests.get(start_url,headers=headers,timeout=5).content            
            
            match = re.compile('data-movie-id=.+?href="(.+?)".+?<h2>(.+?)</h2>',re.DOTALL).findall(html) 
            for item_url, name in match:
                if '/series/' in item_url:
                
                    if clean_title(title).lower() in clean_title(name).lower():
                    
                        if season_check in item_url:
                        
                            #print 'Should be correct show and season url >> '+item_url
                            # NOW # replace and add to get exact url of episode
                            item_url = item_url[:-1].replace('/series/','/episode/') + '-episode-%s/' %(episode)  
                            
                            #print 'PASS THIS EPISODE >>>>>> '+item_url
                            
                            self.get_source(item_url,title,year)
             
                
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources 
            
    def get_source(self,item_url,title,year):
        try:
            count = 0
            
            headers={'User-Agent':random_agent()}
            OPEN = requests.get(item_url,headers=headers,timeout=5).content             
            links = re.compile('IFRAME SRC="(.+?)"',re.I|re.DOTALL).findall(OPEN)      
            for link in links:
                if 'vidoza.net' in link:
                    #print link
                    headers={'User-Agent':random_agent()}
                    Holderpage = requests.get(link,headers=headers,timeout=5).content
                    #print Holderpage
                    PAGE = re.compile('src: "(.+?)".+?res:\'(.+?)\'',re.DOTALL).findall(Holderpage)
                    for final_url,rez in PAGE:
                        if '1080' in rez:
                            qual = '1080p'
                        elif '720' in rez:
                            qual = '720p'
                        else:
                            qual = 'SD'
                        count +=1
                        #print final_url
                        #print qual
                        self.sources.append({'source': 'Direct', 'quality': qual, 'scraper': self.name, 'url': final_url,'direct': False})
                
                elif 'openload' in link:
                        try:
                            get_res=requests.get(link,headers=headers,timeout=5).content
                            rez = re.compile('description" content="(.+?)"',re.DOTALL).findall(get_res)[0]
                            if '1080' in rez:
                                qual = '1080p'
                            elif '720' in rez:
                                qual='720p'
                            else:
                                qual='SD'
                        except: qual='SD'
                        count +=1
                        self.sources.append({'source': 'openload', 'quality': qual, 'scraper': self.name, 'url': links,'direct': False})

                else:
                    if resolveurl.HostedMediaFile(link).valid_url():
                        host = link.split('//')[1].replace('www.','')
                        host = host.split('/')[0].split('.')[0].title()
                        rez = 'DVD'
                        count +=1
                        self.sources.append({'source': host,'quality': rez,'scraper': self.name,'url': link,'direct': False})


            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
