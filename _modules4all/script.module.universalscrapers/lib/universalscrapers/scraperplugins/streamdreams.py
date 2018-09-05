# -*- coding: utf-8 -*-
# Universal Scrapers
#checked 2/09/2018
import re, requests, time, urllib
import xbmcaddon, xbmc
from ..scraper import Scraper
from ..common import clean_title, filter_host, send_log, error_log
from ..modules import client, dom_parser, quality_tags

dev_log =xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")


class streamdreams(Scraper):
    domains = ['streamdreams.org']
    name = "StreamDreams"
    sources = []

    def __init__(self):
        self.base_link = 'https://streamdreams.org'
        self.search_url = self.base_link + '/?s=%s'
        self.sources = []

    def scrape_movie(self, title, year, imdb, debrid=False):
        try:
            start_time = time.time()
            search_id = title.replace(' ','+').lower()
            query = self.search_url % search_id
            #print query

            item_url = self._search(query, title, year)
            #print '##'+ item_url+'##'
            self.get_source(item_url, title, year, '', '', start_time)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, 'Check Search')
            return self.sources

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            search = title.replace(' ','-').lower()
            start_url = '%s/shows/%s?session=%s&episode=%s' % (self.base_link,search,season,episode)
            #print start_url
            self.get_source(start_url, title, year, season, episode, start_time)

            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, 'Check Search')
            return self.sources

    def _search(self, url, title, year):
        try:
            headers = {'User-Agent': client.agent()}
            r = client.request(url,headers=headers)
            #print r
            mov_link = client.parseDOM(r,'div', attrs= {'class':'thumbnail  same-height big-title-thumb'})
            #print mov_link
            for a_s in mov_link:
                #print a_s
                item_url = client.parseDOM(a_s,'a', ret = 'href')[0]
                #print item_url+'?????????????'    
                data = client.parseDOM(r, 'div', attrs={'class': 'caption thumb_caption'})
                for item in data:
                    name = client.parseDOM(item, 'div')[0]
                    rel = client.parseDOM(item, 'div')[1]
                    #print name+ ' '+ rel
                    #print '@#@(grabbed url) %s  (name) %s' % (item_url,name)
                    if not clean_title(title).lower() in clean_title(name).lower():
                        continue
                    if not year == rel:
                        continue
                    #print '@#@URL check> ' + item_url
                return item_url
        except:
            return

    def get_source(self, item_url, title, year, season, episode, start_time):
        try:
            count = 0
            headers = {'User-Agent': client.agent()}
            r = client.request(item_url,headers=headers)
            data = client.parseDOM(r, 'tr')
            for item in data:
                info = client.parseDOM(item,'td')
                for items in info:
                    #print'>>>>>>>>>>>>'+items
                    qual = client.parseDOM(items,'span', ret= 'class')[0] 
                    if 'quality' in qual:
                        qual=qual.replace('quality_','')
                        #print qual
                        links = client.parseDOM(item, 'a', ret='data-href')
                        for link in links:
                            #print link
                            count +=1
                            #print link + qual
                            host = link.split('//')[1].replace('www.','')
                            host = host.split('/')[0].split('.')[0].title() 
                            self.sources.append({'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False})
            if dev_log == 'true':
                end_time = time.time() - start_time
                send_log(self.name, end_time, count, title, year, season='', episode='')
        except:
            pass