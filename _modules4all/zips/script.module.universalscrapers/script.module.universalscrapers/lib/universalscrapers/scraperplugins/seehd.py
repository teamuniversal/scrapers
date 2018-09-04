# -*- coding: utf-8 -*-

import re
import xbmcaddon,time
import xbmc, urllib
from ..scraper import Scraper
from ..common import clean_title, get_rd_domains, send_log, error_log
from ..modules import cfscrape, client

dev_log = xbmcaddon.Addon('script.module.universalscrapers').getSetting("dev_log")

class seehd(Scraper):
    domains = ['http://www.seehd.pl']
    name = "SeeHD"
    sources = []

    def __init__(self):
        self.base_link = 'http://www.seehd.pl'
        self.search_link = '/search/%s/feed/rss2/'

    def scrape_movie(self, title, year, imdb, debrid = False):
        try:
            start_time = time.time()
            scraper = cfscrape.create_scraper()
            search_id = '%s %s' % (title, year)
            start_url = self.base_link + self.search_link % urllib.quote_plus(search_id)
            print '::::::::::::: START URL '+start_url
            
            headers={'User-Agent': client.agent()}
            html = scraper.get(start_url, headers=headers, timeout=15).content
            print '@#@ HTML: %s' % html

            items = client.parseDOM(html, 'item')
            for item in items:
                name = client.parseDOM(item, 'title')[0]
                name = client.replaceHTMLCodes(name)
                t = name.split(year)[0]

                if not clean_title(title) == clean_title(t):
                    continue
                if not year in name:
                    continue
                                                  
                self.get_source(item, title, year, "", "", debrid, start_time)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)

    def scrape_episode(self, title, show_year, year, season, episode, imdb, tvdb, debrid=False):
        try:
            start_time = time.time()
            scraper = cfscrape.create_scraper()
            hdlr = 'S%02dE%02d' % (int(season), int(episode))
            search_id = '%s %s' % (title, hdlr)
            start_url = self.base_link + self.search_link % urllib.quote_plus(search_id)

            headers = {'User-Agent': client.agent()}
            html = scraper.get(start_url, headers=headers, timeout=15).content

            items = client.parseDOM(html, 'item')
            for item in items:
                name = client.parseDOM(item, 'title')[0]
                name = client.replaceHTMLCodes(name)
                t = name.split(hdlr)[0]

                if not clean_title(title) == clean_title(t):
                    continue
                if not hdlr in name:
                    continue
                self.get_source(item, title, year, season, episode, debrid, start_time)
            return self.sources
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name, argument)

    def get_source(self,item_url, title, year, season, episode, debrid, start_time):
        try:
            count = 0
            headers = {'User-Agent': client.agent(),
                       'Referer': self.base_link}

            frames = []
            frames += client.parseDOM(item_url, 'iframe', ret='src')
            frames += client.parseDOM(item_url, 'a', ret='href')
            frames += client.parseDOM(item_url, 'source', ret='src')
            frames += client.parseDOM(item_url, 'enclosure', ret='url')
            #xbmc.log('@#@LINKS: %s' % frames, xbmc.LOGNOTICE)

            try:
                q = re.findall('<strong>Quality:</strong>([^<]+)', item_url, re.DOTALL)[0]
                if 'high' in q.lower():
                    qual = '720p'
                elif 'cam' in q.lower():
                    qual = 'CAM'
                else:
                    qual = 'SD'
            except:
                qual = 'SD'

            for link in frames:
                if 'http://24hd.org' in link: continue
                if 'seehd.pl/d/' in link:
                    scraper = cfscrape.create_scraper()
                    r = scraper.get(link, headers=headers, timeout=15).content
                    link = client.parseDOM(r, 'iframe', ret='src')[0]

                import resolveurl
                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].lower()

                if resolveurl.HostedMediaFile(link):
                    #xbmc.log('@#@NORMAL-LINKS: %s' % link, xbmc.LOGNOTICE)
                    count += 1
                    self.sources.append(
                        {'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False})

                if debrid is True:
                    rd_domains = get_rd_domains()
                    if host not in rd_domains: continue
                    #xbmc.log('@#@RD-LINKS: %s' % link, xbmc.LOGNOTICE)
                    count += 1
                    self.sources.append(
                        {'source': host, 'quality': qual, 'scraper': self.name, 'url': link, 'direct': False, 'debridonly': True})

            if dev_log=='true':
                end_time = time.time() - start_time
                send_log(self.name,end_time,count,title,year)
        except Exception, argument:
            if dev_log == 'true':
                error_log(self.name,argument)
