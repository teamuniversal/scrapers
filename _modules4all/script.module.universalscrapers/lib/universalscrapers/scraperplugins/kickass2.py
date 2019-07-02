# -*- coding: utf-8 -*-
# Universal Scrapers
# checked 01/7/2019

import re
import urllib
import xbmc, xbmcaddon, time
from universalscrapers.common import clean_title, clean_search, send_log, error_log
from universalscrapers.scraper import Scraper
from universalscrapers.modules import client, quality_tags

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")            


class kickass2(Scraper):
    domains = ['kickass2.cc']
    name = "kickass2"
    sources = []

    def __init__(self):
        self.base_link = 'https://kickass2.online'
        self.search_link = 'https://kickass2.cc/usearch/{0}'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            if not debrid:
                return self.sources
            search_id = clean_search(title.lower())
            start_url = '%s/usearch/%s %s' % (self.base_link, urllib.quote_plus(search_id),year)
            #print start_url+'>>>>>>>>>>>>>>>>>>>'
            self.get_source(start_url, title, year, '', '', start_time)
            
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,argument)
            return self.sources
            
    def get_source(self,start_url,title,year,season,episode,start_time):
        try:
            #print 'URL PASSED OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK'+start_url
            count = 0
            headers = {'User-Agent': client.agent()}
            r = client.request(start_url, headers=headers)
            #print r
            Endlinks=re.compile('class="iaconbox center floatright".+?title="Torrent magnet link" href="(.+?)">.+?class="cellMainLink">(.+?)</a>.+?class="nobr center">(.+?)</span></td>',re.DOTALL).findall(r)
            #print 'scraperchk - scrape_movie - EndLinks: '+str(Endlinks)
            for Magnet, quality, size in Endlinks:
                Magnet=Magnet.replace('https://mylink.me.uk/?url=', '')
                qual = quality_tags.check_sd_url(quality)
                #print Magnet + '<><><><><>'
                count+=1
                self.sources.append({'source':'Torrent', 'quality':size+' '+qual, 'scraper':self.name, 'url':Magnet, 'direct':False, 'debridonly': True})
            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log=='true':
                error_log(self.name,argument)
            return[]