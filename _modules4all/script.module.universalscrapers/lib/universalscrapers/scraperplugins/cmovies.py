# -*- coding: utf-8 -*-
# Universal Scrapers
# 30/10/2018 -BUG

import re
import xbmc,xbmcaddon,time
from universalscrapers.scraper import Scraper
from universalscrapers.common import filter_host, clean_search, send_log, error_log
from universalscrapers.modules import client
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class cmovies(Scraper):
    domains = ['https://cmovies.cc']
    name = "Cmovies"
    sources = []

    def __init__(self):
        self.base_link = 'https://cmovies.cc'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      

            start_url = '%s/%s/' %(self.base_link,search_id.replace(' ', '-'))
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url                                  
            
            #headers={'User-Agent':random_agent()}
            #html = requests.get(start_url,headers=headers,timeout=5).content            
            
            #match = re.compile('class="span2 gallery-item".+?><a href="(.+?)">(.+?)</a></span>',re.DOTALL).findall(html) 
            #for item_url, name in match:
                #print 'scraperchk - scrape_movie - name: '+name
                #if year in name:
                    #print 'scraperchk - scrape_movie - item_url: '+item_url                                                           
                    #if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                        #print 'scraperchk - scrape_movie - Send this URL: ' + item_url                             
            self.get_source(start_url, title, year, start_time)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def get_source(self,start_url,title,year,start_time):
        try:
            #print 'PASSEDURL >>>>>>'+start_url
            count = 0
            OPEN = client.request(start_url, timeout=5)
            Endlinks = re.compile('<iframe.+?src="(.+?)"',re.DOTALL).findall(OPEN)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for link1 in Endlinks:
                #print 'scraperchk - scrape_movie - link: '+str(link1)
                link='https:'+link1
                #print link+'?<<<<<<<<<<<<<<<<<<<,,,'     
                if '1080' in link:
                    qual = '1080p'
                if '720' in link:
                    qual = '720p'
                else:
                    qual = 'SD'
                    count+=1
                    host = link.split('//')[1].replace('www.','')
                    host = host.split('/')[0].split('.')[0].title()
                    if not filter_host(host): continue
                    self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources