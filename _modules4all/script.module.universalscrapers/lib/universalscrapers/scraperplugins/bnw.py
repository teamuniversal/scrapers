# -*- coding: utf-8 -*-
# Universal Scrapers

import requests,re
import xbmc,xbmcaddon,time 
from ..scraper import Scraper
from BeautifulSoup import BeautifulSoup
from ..common import clean_title,clean_search,random_agent,send_log,error_log

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

class bnw(Scraper):
    name = "BnwMovies"
    domains = ['http://www.bnwmovies.com']
    sources = []

    def __init__(self):
        self.base_link = 'http://www.bnwmovies.com'
        self.search_link = "/?s="
        self.start_time = ''
        

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            if dev_log=='true':
                self.start_time = time.time()             
            good_title = clean_search(title.lower())
            start_url= 'http://www.bnwmovies.com/%s.html' % (good_title.replace(" ", "-"))
            headers={'User-Agent':random_agent(),'Referer':start_url}
            count = 0 
            html2 = requests.get(start_url,headers=headers,timeout=10).content
            match2 = re.compile('<title >(.+?)</title>',re.DOTALL).findall(html2)
            for rel in match2:
                if year in rel:
                    Link = re.compile('<source.+?src="(.+?)"',re.DOTALL).findall(html2)[-1] 
                    playlink = Link
                    count +=1
                    self.sources.append(
                    {'source': 'bnw', 'quality': 'SD',
                     'scraper': self.name, 'url': playlink,
                     'direct': True})
            if dev_log=='true':
                end_time = time.time() - self.start_time
                send_log(self.name,end_time,count)        
            return self.sources
        except Exception, argument:        
            if dev_log == 'true':
                error_log(self.name,'Check Search')
            return self.sources

# Movie (Trail Riders) 1942             
