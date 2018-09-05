# -*- coding: utf-8 -*-
# Universal Scrapers checked 30/8/2018


import urlparse, urllib
import re

import xbmc,xbmcaddon,time
from universalscrapers.scraper import Scraper
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.modules import client
dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class movienolimit(Scraper):
    domains = ['movienolimit.to']
    name = "MovieNoLimit"
    sources = []

    def __init__(self):
        self.base_link = 'https://movienolimit.to'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()                                                   
            search_id = clean_search(title.lower())                                      
                                                                                        
            start_url = '%s/search?query=%s' % (self.base_link, urllib.quote_plus(search_id))
            #print 'scraperchk - scrape_movie - start_url:  ' + start_url
            headers = {'User-Agent': client.agent()}
            html = client.request(start_url, headers=headers)
            #print html           
            match = re.compile('class="movie-item view-tenth".+?href="(.+?)">.+?alt="(.+?)" />.+?data-title="Quality">(.+?)<',re.DOTALL).findall(html)  
            for link, name, qual in match:
                #print item_url1
                item_url = urlparse.urljoin(self.base_link, link)
                qual = qual.replace('&nbsp;','')
                #print 'scraperchk - scrape_movie - name: '+name
                #print 'scraperchk - scrape_movie - item_url: '+item_url
                if clean_title(search_id) == clean_title(name):
                    #print 'scraperchk - scrape_movie - Send this URL: ' + item_url                             
                    self.get_source(item_url, title, year, start_time, qual)
            print self.sources
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources

    def get_source(self,item_url,title,year,start_time,qual):
        try:
            #print 'PASSEDURL >>>>>>'+item_url
            count = 0
            headers={'User-Agent': client.agent()}
            OPEN = client.request(item_url, headers=headers)
            Endlinks = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(OPEN)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for link in Endlinks:
                #print 'scraperchk - scrape_movie - link: '+str(link)        
                count += 1
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year)
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)
            return self.sources

#movienolimit().scrape_movie('Upgrade', '2018', '')