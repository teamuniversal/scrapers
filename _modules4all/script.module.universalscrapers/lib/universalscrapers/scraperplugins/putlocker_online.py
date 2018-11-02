# -*- coding: utf-8 -*-
# 30/10/2018 -BUG

import re, urllib
import xbmc, xbmcaddon, time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, filter_host, send_log, error_log
from universalscrapers.modules import client
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class putlocker_online(Scraper):
    domains = ['putlockeronlinefree.online']
    name = "Putlocker Online"
    sources = []

    def __init__(self):
        self.base_link = 'https://putlockeronlinefree.online'

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      

            start_url = '%s/search_movies?s=%s' %(self.base_link, urllib.quote_plus(search_id))
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url                                  
            html = client.request(start_url)
            match = re.compile('class="small-item".+?href="(.+?)".+?<b>(.+?)</b>.+?<b>(.+?)</b>.+?alt="(.+?)"',re.DOTALL).findall(html) 
            for item_url1, date,res,name in match:
                #print 'scraperchk - scrape_movie - name: '+name+ '  '+date
                item_url = self.base_link+item_url1
                #print 'scraperchk - scrape_movie - item_url: '+item_url+' '+res                                                           
                if clean_title(search_id).lower() == clean_title(name).lower():     
                                                                                        
                    #print 'scraperchk - scrape_movie - Send this URL: ' + item_url                             
                    self.get_source(item_url, title, year, start_time, res)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

    def get_source(self, item_url, title, year, start_time, res):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            OPEN = client.request(item_url, timeout=5)
            Endlinks = re.compile('class="movie_links"><li(.+?)<h3><b class="icon-share-alt"',re.DOTALL).findall(OPEN)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for block in Endlinks:
                link1 = re.compile('target="_blank" href="(.+?)"',re.DOTALL).findall(str(block))
                #print 'scraperchk - scrape_movie - link: >>>>>>>>>>>>>>>>'+str(link1)
                for link in link1:
                    count += 1
                    host = link.split('//')[1].replace('www.', '')
                    host = host.split('/')[0]
                    if not filter_host(host): continue
                    self.sources.append({'source': host, 'quality': res, 'scraper': self.name, 'url': link, 'direct':False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources